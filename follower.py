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

    def __init__(self, port_string, calibrating=False):
        # establish arduino connnection
        self.arduino = self.get_arduino(port_string)
        if calibrating:
            self.running = True
        else:
            self.running = True
        self.calibrating = calibrating

        # setup pid values
        self.kp = None
        self.ki = None
        self.kd = None

        with open("init_vals.csv", "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            k_vals = reader.__next__()
            self.kp = float(k_vals[0])
            self.ki = float(k_vals[1])
            self.kd = float(k_vals[2])

        self.arduino.write
        self.arduino.write(f"p={self.kp}".encode("utf-8"))
        self.arduino.write(f"i={self.ki}".encode("utf-8"))
        self.arduino.write(f"d={self.kd}".encode("utf-8"))

    def get_arduino(self, port_string):
        """Create serial port connection to arduino"""
        arduino = serial.Serial(port=port_string, baudrate=9600, timeout=1)
        return arduino

    def setup_gui(self):
        fig = plt.figure()
        kp_line = fig.add_axes([0.2, 0.6, 0.65, 0.03])
        kp_slider = Slider(
            ax=kp_line, label="kp", valmin=0, valmax=9.99, valinit=self.kp
        )
        ki_line = fig.add_axes([0.2, 0.4, 0.65, 0.03])
        ki_slider = Slider(
            ax=ki_line, label="ki", valmin=0, valmax=9.99, valinit=self.ki
        )
        kd_line = fig.add_axes([0.2, 0.2, 0.65, 0.03])
        kd_slider = Slider(
            ax=kd_line, label="kd", valmin=0, valmax=9.99, valinit=self.kd
        )

        def save_k_vals():
            with open("init_vals.csv", "w") as csvfile:
                writer = csv.writer(csvfile, delimiter=",")
                writer.writerow([self.kp, self.ki, self.kd])

        def kp_update(val):
            print(kp_slider.val)
            val = int(kp_slider.val * 100)
            self.kp = val / 100
            self.arduino.write(f"p={val}".encode("utf-8"))
            save_k_vals()

        def ki_update(val):
            print(ki_slider.val)
            val = int(ki_slider.val * 100)
            self.ki = val / 100
            self.arduino.write(f"i={val}".encode("utf-8"))
            save_k_vals()

        def kd_update(val):
            print(kd_slider.val)
            val = int(kd_slider.val * 100)
            self.kd = val / 100
            self.arduino.write(f"d={val}".encode("utf-8"))
            save_k_vals()

        kp_slider.on_changed(kp_update)
        ki_slider.on_changed(ki_update)
        kd_slider.on_changed(kd_update)

        self.running = True

        plt.show()

    def dataWrite(self):
        print("opened datawrite")
        with open("followerData.csv", "w", newline="") as csvfile:
            print("opened datawrite file")
            writer = csv.writer(csvfile, delimiter=",")
            if self.calibrating:
                writer.writerow(["ls", "rs"])
            else:
                writer.writerow(["ls", "rs", "lm", "rm"])
            while self.running:
                print("in running loop")
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
    df = pd.read_csv("followerData.csv")

    fig, ax = plt.subplots()
    if calibrating:
        ax.plot(df["ls"], linewidth=2, label="Left Sensor")
        ax.plot(df["rs"], linewidth=2, label="Right Sensor")
        ax.legend(fontsize=14)
        plt.title("Calibration Data")
        plt.ylabel("Sensor Value (0-1023)")
        plt.savefig("sensor_calib.png")
        plt.show()
    else:
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
    # follower.setup_gui()  # this is blocking
    # time.sleep(0.2)

    # follower.running = False
    # time.sleep(0.2)

    plotting(cali)


if __name__ == "__main__":
    main()
