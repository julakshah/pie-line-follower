import threading
import serial
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import numpy as np
import pandas as pd
import time
import csv
from matplotlib.widgets import Button, Slider


class followMan:
    """a class to handle the arduino connection and data collection
    Args:
        port_string: a string of the arduino port address.
        calibrating: a boolean representing if we're collecting calibration
          data or not

    Instance attributes:
        self.running: whether we're running the program
        self.calibrating: whether the program is running calibration routine"""

    def __init__(self, port_string, calibrating=False):
        # establish arduino connnection
        self.arduino = self.get_arduino(port_string)
        self.running = True
        self.calibrating = calibrating

    def get_arduino(self, port_string):
        """Create serial port connection to arduino"""
        arduino = serial.Serial(port=port_string, baudrate=9600, timeout=1)
        return arduino

    def dataWrite(self):
        """write the data from serial port to the desired csv file"""
        with open("followerData.csv", "w", newline="") as csvfile:
            # create file writer object
            writer = csv.writer(csvfile, delimiter=",")
            # create csv headings for pandas
            if self.calibrating:
                writer.writerow(["ls", "rs"])
            else:
                writer.writerow(["ls", "rs", "lm", "rm"])
            while self.running:
                # collect data while it's running
                serial_data = self.arduino.readline().decode("utf-8")
                serial_data = serial_data.strip("\r\n'")
                if serial_data != "":
                    sensor_vals = serial_data.split()
                    if self.calibrating:
                        writer.writerow([sensor_vals[0], sensor_vals[1]])
                    else:
                        line_data = serial_data.split()
                        print(line_data)
                        writer.writerow(
                            [
                                sensor_vals[0],
                                sensor_vals[1],
                                sensor_vals[2],
                                sensor_vals[3],
                            ]
                        )


def plotting(calibrating):
    """A function to plot the data on matplotlib graphs
    Args:
      calibrating: a boolean to say whether to plot as if calibrating or
        to plot overlayed data"""
    df = pd.read_csv("followerData.csv")

    fig, ax = plt.subplots()
    if calibrating:
        # plots the calibration data (2 inputs)
        ax.plot(df["ls"], linewidth=2, label="Left Sensor")
        ax.plot(df["rs"], linewidth=2, label="Right Sensor")
        ax.legend(fontsize=14)
        plt.title("Calibration Data")
        plt.ylabel("Sensor Value (0-1023)")
        plt.savefig("sensor_calib.png")
        plt.show()
    else:
        # plots the sensor data ontop of motor data where motors are scaled by 40x
        ax.plot(df["ls"], linewidth=2, label="Left Sensor")
        ax.plot(df["rs"], linewidth=2, label="Right Sensor")
        ax.plot(df["lm"] * 40, linewidth=2, label="Left Motor")
        ax.plot(df["rm"] * 40, linewidth=2, label="Right Motor")
        ax.legend(fontsize=14)
        plt.title("Motor input overlayed with sensor output")
        plt.savefig("motor_input_over_sensor.png")
        plt.show()


def main():
    cali = False
    # follower = followMan("/dev/cu.usbmodemB43A4536DECC2", calibrating=cali)

    # dataThread = threading.Thread(target=follower.dataWrite)
    # dataThread.start()
    # dataThread.join()

    # follower.running = False
    # time.sleep(0.2)

    plotting(cali)


if __name__ == "__main__":
    main()
