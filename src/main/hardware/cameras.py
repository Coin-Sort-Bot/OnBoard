import cv2


class Camera:
    """
    Class for a single camera.
    """

    def __init__(self, port: int):
        """
        Initialize the camera.

        Arguments:
            port: The port the camera is connected to.
        """
        self.port = port
        self.camera = None

    def mount(self):
        """
        Mount the camera.
        """
        self.camera = cv2.VideoCapture(self.port)

    def unmount(self):
        """
        Unmount the camera.
        """
        self.camera.release()

    def capture(self, count=1) -> bytes | list[bytes]:
        """
        Capture an image or more from the camera.

        Arguments:
            count: The number of images to capture. Defaults to 1.
        """
        images = []
        for i in range(count):
            return_value, image = self.camera.read()
            cv2.imwrite("opencv" + str(i) + ".png", image)

        return images if count > 1 else images[0]


class Cameras:
    """
    Class for handling the USB cameras.

    These are the two USB webcams attached to the USB-2.0 ports on the PI.

    Attributes:
        camera1: The first camera.
        camera2: The second camera.
    """
    def __init__(self):
        """
        Initialize the cameras.
        """
        self.camera1 = Camera(0)
        self.camera2 = Camera(1)

    def mount(self):
        """
        Mount the cameras.
        """
        self.camera1.mount()
        # self.camera2.mount()

    def unmount(self):
        """
        Unmount the cameras.
        """
        self.camera1.unmount()
        # self.camera2.unmount()
