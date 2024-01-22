from util import get_available_cameras
import logging


def list_cameras_command(args):
    logging.info("Discovered Cameras:")
    cams = get_available_cameras()
    for cam in cams:
        logging.info("\t%d - %s" % (cam.device_id(), cam.name()))
