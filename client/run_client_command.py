import logging
import time
import json
import string
import random

from camera_definition import CameraDefinition
from camera import Camera
from util import get_available_cameras


def random_client_id() -> str:
    return ''.join(random.choices(string.ascii_uppercase, k=5))


def countdown(seconds: int):
    for i in range(seconds):
        logging.info("%d..." % (seconds - i))
        time.sleep(1)


def ignore_camera(config, camera: CameraDefinition) -> bool:
    if "ignore-device-names" not in config:
        return False

    for name_to_ignore in config["ignore-device-names"]:
        if name_to_ignore == camera.name():
            return True

    return False


def client_id(config) -> str:
    if "client-id" in config:
        return config["client-id"]
    return random_client_id()


def run_client_command(args):
    config = json.load(args.config)

    cams = get_available_cameras()
    opened_cams: list[Camera] = []
    for cam in cams:
        if ignore_camera(config, cam):
            logging.info("IGNORING: " + cam.name())
            continue

        logging.info("OPENING:  " + cam.name())
        cam = cam.to_camera()
        cam.start()
        opened_cams.append(cam)

    input("Press ENTER to grab photos")

    countdown(3)

    for cam in opened_cams:
        cam.capture()

    logging.info("Waiting images")
    for cam in opened_cams:
        cam.save_image()

    logging.info("Done")
    for cam in opened_cams:
        cam.stop()
