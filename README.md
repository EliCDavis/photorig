# Photorig

At home economical photogrametry rig

## Rig

### Parts List

* 2x  - 2020 V Aluminum Extrusion 250mm
* 4x  - 2020 V Aluminum Extrusion 700mm
* 12x - 2020 Series L-Shape Interior Inside Corner Connector Joint Bracket with Screws
* 6x  - 20mm V Gantry Plate Kit 
* 6x  - Webcams atleast 1080p with a 1/4" screw hole
* 6x  - 1/4" Mount Screws
* nx  - Rubber Washers

## Client

### Setup

```bash
pip install numpy
pip install matplotlib
pip install opencv-contrib-python
pip install pygrabber
```

### Usage 

#### List Cameras

Lists out all cameras connected to the system.

```bash
python client list-cameras
```

#### List Formats

Lists out all formats available for a specific camera connected to the system.

```bash
python client list-formats [camera_index]
```

#### Run

Config

```jsonc

{
    // Optional field to explicitly set the ID of the client in respect to the 
    // photogrametry server. If set, it is the user's resonsibility to ensure
    // client-ids stay unique across the system.
    //
    // If unset, the client-id is randomly generated at runtime
    "client-id": "local",

    // Optional list of names of devices to ignore
    "ignore-device-names": [

        // Any device named "OBS Virtual Camera" will be ignored
        "OBS Virtual Camera"
    ]
}
```

## Server

### Setup

```bash
go install photogram-server
```

### Usage



