from camera import Camera

class CameraDefinition:

    def __init__(self, device_id: int, name: str):
        self.__device_id = device_id
        self.__name = name

    def to_camera(self) -> Camera:
        return Camera(self.__device_id, self.__name)
    
    def name(self) -> str:
        return self.__name
    
    def device_id(self) -> int:
        return self.__device_id
    
