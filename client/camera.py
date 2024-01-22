import logging
import threading
from pygrabber.dshow_graph import FilterGraph, Mat
import cv2


class Camera(threading.Thread):
    def __init__(self, device_id: int, camera_name: str):
        threading.Thread.__init__(self)

        self.device_id = device_id
        self.camera_name = camera_name

        self.graph = FilterGraph()
        self.graph.add_video_input_device(device_id)
        self.graph.add_sample_grabber(self.img_cb)
        self.graph.add_null_render()

        self.graph.prepare_preview_graph()
        self.graph.run()

        self.image_grabbed: cv2.typing.MatLike | None = None
        self.image_done = threading.Event()

        self.run_thread = False
        self.cap = False

    def capture_2(self):
        self.cap = True

    def stop(self):
        self.run_thread = False

    def run(self):
        logging.info("starting %s", self.camera_name)
        self.run_thread = True
        while self.run_thread:
            if self.cap:
                self.capture()
                self.cap = False

    def img_cb(self, image: cv2.typing.MatLike):
        self.image_grabbed = image
        logging.info("Image Grabbed [%d] %s", self.device_id, self.camera_name)
        self.image_done.set()

    def capture(self):
        self.graph.grab_frame()

    def wait_image(self):
        self.image_done.wait(1000)
        return self.image_grabbed

    def save_image(self):
        frame_name = "{}_frame_{}.png".format(self.device_id, self.camera_name)
        img = self.wait_image()
        if img is not None:
            cv2.imwrite(frame_name, img)
            logging.info("Wrote %s", frame_name)
        else:
            logging.warn("wait image returned None")
