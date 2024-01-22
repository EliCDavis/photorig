import logging
import cv2
import threading
import datetime
import argparse

# Commands
from list_cameras_command import list_cameras_command
from list_formats_command import list_formats_command
from run_client_command import run_client_command

nextTimeToTakePhoto = None


class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID

    def run(self):
        logging.info("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)


def camPreview(previewName, camID):
    global nextTimeToTakePhoto

    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    cam.set(cv2.CAP_PROP_FPS, 30.0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    img_counter = 0
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    lastTaken = None

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(1)
        if key == 27:  # exit on ESC
            break
        elif key % 256 == 32:  # SPACE pressed
            nextTimeToTakePhoto = datetime.datetime.now() + datetime.timedelta(0, 3)

        if nextTimeToTakePhoto is not None and nextTimeToTakePhoto < datetime.datetime.now() and nextTimeToTakePhoto is not lastTaken:
            img_name = "1opencv_cam_{}_frame_{}.png".format(camID, img_counter)
            cv2.imwrite(img_name, frame)
            logging.info("{} written!".format(img_name))
            img_counter += 1
            lastTaken = nextTimeToTakePhoto

    cam.release()
    cv2.destroyWindow(previewName)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d [%(levelname)-8s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    parser = argparse.ArgumentParser(
        prog='photorig',
        description='Utilities for running a home made photogrametry rig')

    subparsers = parser.add_subparsers(
        title="commands", help='available commands', dest='subparser_name', required=True)

    # List Cameras Command
    parser_list_cameras = subparsers.add_parser(
        'list-cameras', help='List all available video cameras')
    parser_list_cameras.set_defaults(func=list_cameras_command)

    # List Formats Command
    parser_list_formats = subparsers.add_parser(
        'list-formats', help='List all available formats for a specific camera')
    parser_list_formats.add_argument(
        'camera_index', type=int, help='index of camera to list formats')
    parser_list_formats.set_defaults(func=list_formats_command)

    # Run Client Command
    parser_run = subparsers.add_parser('run', help='run the client')
    parser_run.add_argument(
        '--config', type=argparse.FileType('r'), help='path to config file')
    parser_run.set_defaults(func=run_client_command)

    args = parser.parse_args()
    args.func(args)
