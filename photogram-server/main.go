package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/gorilla/mux"
	"github.com/urfave/cli/v2"
)

type CameraConfig struct {
	Name string `json:"name"`
}

type ClientConfig struct {
	Cameras []CameraConfig `json:"cameras"`
}

type ClientInstance struct {
	Client   ClientConfig
	LastSeen time.Time
}

type PhotogrametryServer struct {
	Port    string
	Host    string
	Clients map[string]ClientInstance
	Lock    sync.RWMutex
}

func (ps *PhotogrametryServer) serve() error {
	r := mux.NewRouter()
	r.Path("/client-ping/{id}").
		Methods("POST").
		HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			vars := mux.Vars(r)
			id, ok := vars["id"]
			if !ok {
				http.Error(w, "need id", http.StatusBadRequest)
				return
			}

			client := &ClientConfig{}
			err := json.NewDecoder(r.Body).Decode(client)
			if err != nil {
				http.Error(w, err.Error(), http.StatusBadRequest)
				return
			}

			ps.Lock.Lock()
			defer ps.Lock.Unlock()
			ps.Clients[id] = ClientInstance{
				Client:   *client,
				LastSeen: time.Now(),
			}

			w.WriteHeader(http.StatusOK)
		})

	r.Path("/status").
		Methods("GET").
		HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			ps.Lock.RLock()
			defer ps.Lock.RUnlock()
			json.NewEncoder(w).Encode(ps.Clients)
		})

	addr := fmt.Sprintf("%s:%s", ps.Host, ps.Port)
	log.Printf("Serving over http://%s\n", addr)
	return http.ListenAndServe(addr, r)
}

func main() {
	app := &cli.App{
		Name:  "Photogrametry Server",
		Usage: "Server for conducting multiple clients to take images at the same time",
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:  "port",
				Usage: "port to start server on",
				Value: "8080",
			},
			&cli.StringFlag{
				Name:  "host",
				Value: "localhost",
			},
		},
		Action: func(ctx *cli.Context) error {
			server := PhotogrametryServer{
				Port:    ctx.String("port"),
				Host:    ctx.String("host"),
				Clients: make(map[string]ClientInstance),
			}
			return server.serve()
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
