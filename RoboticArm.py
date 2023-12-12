import serial
import math
import time
import numpy as np
from Servo import Servo

class RoboticArm:
    def __init__(self, port, baud_rate):
        self.ser = serial.Serial(port, baud_rate)
        time.sleep(2)
        self.servos = [
            Servo(-90, 90, 148, 480),  # Base servo
            Servo(0, 180, 160, 460),     # Second servo
            Servo(-124, 126, 516, 80),  # Third servo
            Servo(0, 10, 160, 300)      # Gripper servo
        ]
        self.L1_mm = 112.71
        self.L2_mm = 177.8
        self.L3_mm = 152.40

    def inverse_kinematics(self, x, y, z):
        xprime = math.sqrt(x**2 + y**2)
        theta1 = math.degrees(math.atan2(-y, x))
        theta2 = math.degrees(math.acos(((z-self.L1_mm)**2 + xprime**2 + self.L2_mm**2 - self.L3_mm**2) / (2 * self.L2_mm * math.sqrt((z-self.L1_mm)**2 + xprime**2))) + math.atan2(z-self.L1_mm, xprime))
        theta3 = math.degrees(-math.acos(((z-self.L1_mm)**2 + xprime**2 - self.L2_mm**2 - self.L3_mm**2) / (2*self.L2_mm*self.L3_mm)))
        return [theta1, theta2, theta3]

    def send_command(self, x, y, z, grip, special_case = False):
        angles = self.inverse_kinematics(x, y, z)
        if special_case:
          angles[0] = 90
          angles[1] = 180 - angles[1]
          angles[2] = -angles[2]
        pulse_lengths = [servo.calculate_pulse_length(angle) for servo, angle in zip(self.servos, angles + [grip])]
        command = ' '.join(str(pl) for pl in pulse_lengths) + '\n'
        self.ser.write(command.encode())

    def close(self):
        self.ser.close()