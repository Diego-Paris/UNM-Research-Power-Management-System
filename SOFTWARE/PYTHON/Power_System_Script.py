import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
import tkinter as tk
from tkinter import ttk
import serial

matplotlib.use("TkAgg")

# Establish lists
cnt = 0
dataArray = [0, 1]  # Allows to store the values before appending them to their designated lists
solarVoltList = []
windVoltList = []
solarCurrentList = []
windCurrentList = []

# Establish resistance value based on the model
solarResist = 115
windResist = 30

# Declare variables used to calculate the average
solarCurrent = 0
windCurrent = 0
solarVolts = 0
windVolts = 0

# Establish placeholders to store the average
solarVoltAverage = 0
solarCurrAverage = 0
windVoltAverage = 0
windCurrAverage = 0

# Holds x values to allow for easier control of x axis
xlist = []
cnt2 = 0

# Attempts connection with Arduino
try:
    arduinoData = serial.Serial("COM5", 9600)  # Declare COM port and baud rate in regards to Arduino
except:
    print("Could not connect to the Serial port")
    exit()

# Clears the serial port of any data
arduinoData.close()
arduinoData.open()

# Selects fonts and styles
LARGE_FONT = ("Verdana", 12)
MEDIUM_FONT = ("Verdana", 10)
style.use("ggplot")

# Declares figure and its subplots for graphing
f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(211)
a2 = f.add_subplot(212)


def read_from_serial():
    """
    Docstring: Reads from serial and stores into a list
    """
    global cnt
    global cnt2
    global dataArray
    global solarVoltList
    global windVoltList
    global solarCurrent
    global windCurrent
    global windCurrentList
    global solarCurrentList
    global solarVolts
    global windVolts

    # While there's no data coming in from the Arduino, do nothing
    while arduinoData.inWaiting() == 0:
        pass

    # Takes in the data from Arduino and decodes it
    arduinoString = arduinoData.readline().decode("utf-8")
    dataArray = arduinoString.split(',')  # Splits values in to a list
    solarVolts = float(dataArray[0])  # Assign solar voltage
    windVolts = float(dataArray[1])  # Assign wind voltage

    solarCurrent = solarVolts / solarResist  # Calculates current for solar
    windCurrent = windVolts / windResist  # Calculates current for wind

    cnt2 += 1  # Adds to counter

    print(solarVolts, "\t", windVolts)  # Print to console for debugging

    # Appends the value to its designated list
    solarVoltList.append(solarVolts)
    windVoltList.append(windVolts)
    solarCurrentList.append(solarCurrent)
    windCurrentList.append(windCurrent)
    xlist.append(cnt2)

    # Checks if the counter is greater than 20,
    # if so it will pop off the first values
    # and allow for a scrolling graph
    # - Comment this if statement out if you don't need it to scroll
    if (cnt2 > 20):
        solarVoltList.pop(0)
        windVoltList.pop(0)
        solarCurrentList.pop(0)
        windCurrentList.pop(0)
        xlist.pop(0)


count = 0


def animate(i):
    """
    Docstring: Animates graph every tick determined by i
    """

    global count

    try:
        read_from_serial()
    except:

        while count == 0:
            print("Ended Serial Connection")
            count += 1
        else:
            pass

    # Graphs plot for solar voltage
    a.clear()
    a.set_ylim(0, 12)
    a.plot(xlist, solarVoltList, label='Solar Voltage', color='orange')
    a.plot(xlist, solarCurrentList, label='Solar Current', color='red')  # place holder for solar current
    a.legend(bbox_to_anchor=(0, 1.35), loc='upper left', ncol=1)

    # Graphs plot for wind voltage
    a2.clear()
    a2.set_ylim(0, 12)
    a2.plot(xlist, windVoltList, label='Wind Voltage', color='blue')
    a2.plot(xlist, windCurrentList, label='Wind Current', color='green')  # place holder for wind current
    a2.legend(bbox_to_anchor=(0.60, 2.55), loc='upper left', ncol=1)


# Due to the scope of the project the portion below is focused on Object Oriented programming in order
# to allow for an interactive user interface, therefore it is beyond the scope of the project and therefore
# will not be commented over.
class Power_System(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self,default="name goes here.ico")
        tk.Tk.wm_title(self, "UNM Power Management Research Project")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def end_serial(self, cont):
        arduinoData.close()

    def resume_serial(self, cont):
        try:
            arduinoData.open()
        except:
            print("Serial Port is already open")

    def write_to_files(self, cont):
        global solarVoltAverage
        global solarCurrAverage
        global windVoltAverage
        global windCurrAverage
        solar_volt_sum = 0
        solar_curr_sum = 0
        wind_volt_sum = 0
        wind_curr_sum = 0
        seconds = 0

        for sVolt, sCurr, wVolt, wCurr in zip(solarVoltList, solarCurrentList, windVoltList, windCurrentList):
            with open('Values_Over_Time4.txt', mode='w') as f:
                f.write(
                    f'{sVolt:1.2f}' + ',' + f'{sCurr:1.2f}' + ',' + f'{wVolt:1.2f}' + ',' + f'{wCurr:1.2f}' + ',' + str(
                        seconds) + '\n')
            seconds += 1

        for sVolt, sCurr, wVolt, wCurr in zip(solarVoltList, solarCurrentList, windVoltList, windCurrentList):
            solar_volt_sum += sVolt
            solar_curr_sum += sCurr
            wind_volt_sum += wVolt
            wind_curr_sum += wCurr

        solarVoltAverage = solar_volt_sum / len(solarVoltList)
        solarCurrAverage = solar_curr_sum / len(solarCurrentList)
        windVoltAverage = wind_volt_sum / len(windVoltList)
        windCurrAverage = wind_curr_sum / len(windCurrentList)

        with open("testParamSolar4.txt", mode='w') as f:
            f.write(f'{solarVoltAverage:1.2f}' + ',' + f'{solarCurrAverage:1.2f}')

        with open("testParamWind4.txt", mode='w') as f:
            f.write(f'{windVoltAverage:1.2f}' + "," + f'{windCurrAverage:1.2f}')

        print("Wrote current values to respective files")


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="View Real Time Graphs",
                             command=lambda: controller.show_frame(PageOne))
        button1.pack()

        # button2 = ttk.Button(self, text="View Documentation",
        #                      command=lambda: controller.show_frame(PageTwo))
        # button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Real time Graph\nVoltage and Current over Time (seconds)", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Pause Test",
                             command=lambda: controller.end_serial(StartPage))
        button2.pack()

        button3 = ttk.Button(self, text="Resume Test",
                             command=lambda: controller.resume_serial(StartPage))
        button3.pack()

        button4 = ttk.Button(self, text="Write to files",
                             command=lambda: controller.write_to_files(StartPage))
        button4.pack()

        canvas = FigureCanvasTkAgg(f, self)

        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


# class PageTwo(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Documentation", font=LARGE_FONT)
#         label.pack(pady=10, padx=10)
#
#         button1 = ttk.Button(self, text="Back to Home",
#                              command=lambda: controller.show_frame(StartPage))
#         button1.pack()
#
#         label = tk.Label(self, text=' ', font=MEDIUM_FONT)
#         label.pack(pady=10, padx=10)


# Allows to store the system into an instance of the the Power_System class
app = Power_System()
# Animates the graphs
ani = animation.FuncAnimation(f, animate, interval=1000)
# Loops the app object
app.mainloop()
# Properly closes serial terminal
arduinoData.close()
