import os
import time
import numpy as np
from PIL import Image
import glob
from donkeycar.utils import rgb2gray


class BaseCamera:

    def run_threaded(self):
        return self.frame

class MockCamera(BaseCamera):
    '''
    Fake camera. Returns only a single static frame
    '''
    def __init__(self, image_w=160, image_h=120, image_d=3, image=None):
        if image is not None:
            self.frame = image
        else:
            self.frame = np.array(Image.new('RGB', (image_w, image_h)))

    def update(self):
        pass

    def shutdown(self):
        pass



class TelloCamera(BaseCamera):
    '''
    Tello camera.
    '''
    def __init__(self, image_w=160, image_h=120, image_d=3, image=None):
        import parts.tello as tello
        import cv2
        self.running = True
        self.frame = None
        self.image_w = image_w
        self.image_h = image_h

        self.drone = tello.Tello('', 8889)
        time.sleep(0.5)

        frame = self.drone.read() 
        while frame is None or frame.size == 0:
            frame = self.drone.read() 

        self.frame = cv2.resize(frame, dsize=(self.image_w, self.image_h) ) 

        self.drone.send_command('takeoff')

    def update(self):
        import cv2
        while self.running:
            frame = self.drone.read()
            self.frame = cv2.resize(frame, dsize=(self.image_w, self.image_h) ) 

    def shutdown(self):
        self.running = False
        self.drone.send_command('streamoff')
        time.sleep(0.5)
        self.drone.send_command('land')
        time.sleep(4.0)
        del self.drone
