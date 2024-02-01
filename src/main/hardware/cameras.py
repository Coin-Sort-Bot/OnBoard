import asyncio
import re
import subprocess
from threading import Thread

import cv2
import logging
from concurrent.futures import ThreadPoolExecutor
import atexit

from pkg_resources._vendor.jaraco.context import suppress

logger = logging.getLogger(__name__)


class Camera:
    """
    Class for a single camera.
    """

    class FailedToMountCamera(Exception):
        """
        Exception for when the camera fails to mount.
        """

        pass

    def __init__(self, port: int | str):
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
        try:
            self.camera.read()
            return_value, image = self.camera.read()
            is_success, im_buf_arr = cv2.imencode(".jpg", image)
        except cv2.error:
            is_success = False
        except AttributeError:
            is_success = False

        if not is_success:
            raise Camera.FailedToMountCamera(
                f"Failed to mount camera on port {self.port}"
            )

        logger.info(f"Mounted camera on port {self.port}")

    def unmount(self):
        """
        Unmount the camera.
        """
        if self.camera is not None:
            self.camera.release()
        logger.info(f"Unmounted camera on port {self.port}")

    async def capture(self, count=1) -> bytes | list[bytes]:
        """
        Capture an image or more from the camera.

        Arguments:
            count: The number of images to capture. Defaults to 1.
        """
        images = []
        for i in range(count):
            return_value, image = self.camera.read()
            is_success, im_buf_arr = cv2.imencode(".jpg", image)
            byte_im = im_buf_arr.tobytes()
            images.append(byte_im)
            logger.info(f"Captured image {i + 1} from camera on port {self.port}")

        logger.info(f"Captured {count} images from camera on port {self.port}")
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
        cameras = subprocess.run(
            ("v4l2-ctl", "--list-devices", "-d", "/dev/videoX"), capture_output=True
        )
        cameras = re.findall(
            r"Digital Microscope: Digital Mic \(usb-[\d:.-]+\):\n\t\/dev\/(video\d)\n\t\/dev\/(video\d)",
            cameras.stdout.decode(),
        )
        logger.debug("Cameras found: %s", cameras)

        self.camera1 = Camera(f"/dev/{cameras[0][0]}")
        self.camera2 = Camera(f"/dev/{cameras[1][0]}")

        atexit.register(self.unmount)
        logger.info("Initialized cameras")

    def __del__(self):
        """
        Delete the camera.
        """
        self.unmount()
        logger.info("Destructing cameras instance")

    def mount(self):
        """
        Mount the cameras.
        """
        while True:
            try:
                logger.debug("Attempting to mount cameras")
                if not self.camera1.camera:
                    self.camera1.mount()
                    logger.debug("Camera 1 mounted")
                if not self.camera2.camera:
                    self.camera2.mount()
                    logger.debug("Camera 2 mounted")
                break
            except Camera.FailedToMountCamera:
                logger.warning("Failed to mount cameras, retrying")
                continue

        logger.info("Mounted cameras")

    def unmount(self):
        """
        Unmount the cameras.
        """
        self.camera1.unmount()
        self.camera2.unmount()
        logger.info("Unmounted cameras")
