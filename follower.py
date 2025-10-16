import serial
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import csv
from matplotlib.widgets import Button, Slider


def main():
    # arduino = serial.Serial(
    #    port="/dev/cu.usbmodemB08184983AEC2", baudrate=9600, timeout=1
    # )
    kp = None
    ki = None
    kd = None

    with open("init_vals.csv", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        k_vals = reader.__next__()
        kp = float(k_vals[0])
        ki = float(k_vals[1])
        kd = float(k_vals[2])

    # setup gui
    fig = plt.figure()
    kp_line = fig.add_axes([0.2, 0.6, 0.65, 0.03])
    kp_slider = Slider(ax=kp_line, label="kp", valmin=0, valmax=9.99, valinit=kp)
    ki_line = fig.add_axes([0.2, 0.4, 0.65, 0.03])
    ki_slider = Slider(ax=ki_line, label="ki", valmin=0, valmax=9.99, valinit=ki)
    kd_line = fig.add_axes([0.2, 0.2, 0.65, 0.03])
    kd_slider = Slider(ax=kd_line, label="kd", valmin=0, valmax=9.99, valinit=kd)

    def save_k_vals():
        with open("init_vals.csv", "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            writer.writerow([kp, ki, kd])

    def kp_update(val):
        print(kp_slider.val)
        val = int(kp_slider.val * 100)
        kp = val / 100
        arduino.write(f"p={val}".encode("utf-8"))
        save_vals()

    def ki_update(val):
        print(ki_slider.val)
        val = int(ki_slider.val * 100)
        ki = val / 100
        arduino.write(f"i={val}".encode("utf-8"))
        save_vals()

    def kd_update(val):
        print(kd_slider.val)
        val = int(kd_slider.val * 100)
        kd = val / 100
        arduino.write(f"d={val}".encode("utf-8"))
        save_vals()

    kp_slider.on_changed(kp_update)
    ki_slider.on_changed(ki_update)
    kd_slider.on_changed(kd_update)

    # write initial k vals to arduino
    arduino.write(f"p={kp}".encode("utf-8"))
    arduino.write(f"i={ki}".encode("utf-8"))
    arduino.write(f"d={kd}".encode("utf-8"))

    # END: begin gui loop
    plt.show()


if __name__ == "__main__":
    main()
