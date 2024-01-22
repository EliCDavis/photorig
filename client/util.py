from camera_definition import CameraDefinition
from pygrabber.dshow_graph import FilterGraph


def get_available_cameras() -> list[CameraDefinition]:
    devices = FilterGraph().get_input_devices()

    available_cameras = []
    for device_index, device_name in enumerate(devices):
        available_cameras.append(CameraDefinition(device_index, device_name))

    return available_cameras