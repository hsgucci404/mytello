"""
actuators.py
Classes to control the motors and servos. These classes 
are wrapped in a mixer class before being used in the drive loop.
"""

import time

import donkeycar as dk

import socket


class MockController(object):
    def __init__(self):
        pass

    def run(self, pulse):
        pass

    def shutdown(self):
        pass

class TelloController(object):
    def __init__(self):
        import socket
        self.tello_ip='192.168.10.1'
        self.tello_port=8889
        self.tello_address = (self.tello_ip, self.tello_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # socket for sending cmd

    def run(self, throttle=0.0, steering=0.0, move_leftright=0.0, move_updown=0.0):
        a = b = c = d = 0
        a = int( move_leftright * 100 )      # a : move left/right
        b = int( throttle * 100 )              # b : move forward/back
        c = int( move_updown * 100 )          # c : move up/down
        d = int( steering * 100 )              # d : turn cw/ccw
        command = f"rc {a} {b} {c} {d}"
        self.socket.sendto(command.encode('utf-8'), self.tello_address )

    def shutdown(self):
        self.socket.close()

