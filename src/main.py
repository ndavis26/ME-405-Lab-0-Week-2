"""! @file main.py
Measures an experimental and theoretical RC circuit response and plots
both onto one graph.

This is done using the Group 20 Arduino in serial port COM8 which holds
the necessary main.py to generate the RC circuit experimental response.

@author Nathaniel Davis
@author Sebastian Bessoudo
@author reference:Spluttflob-lab0example.py
@date 2024-1-29
"""

import math
import tkinter
import serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    Resets the target arduino and formats the time and voltage data
    from the arduino into a list to be plotted.
    Also generates a theoretical response for an RC circuit which is plotted onto
    the same graph.
    
    @param plot_axes The function that plots the given data onto the generated axes
    @param plot_canvas The function that displays the plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    
    """
    times = [t*10 for t in range(500)]
    boing = [3.3*(1-math.exp((-t/1000)/(100000*3.3*0.000001))) for t in times]
    
    ser = serial.Serial('COM8', timeout = 8)
    ser.write(b'\x04')
    data = ser.readlines()
    timeExp = []
    voltExp = []
    for line in data:
        seb = line.decode('utf-8')
        if ',' in seb:
            seb2 = seb.strip().split(',')
            sebtime = seb2[0].split(" ")
            sebvolt = seb2[1].split(" ")
            timeExp.append(int(sebtime[0]))
            voltExp.append(float(sebvolt[1]))
        else:
            continue    

    # Draw the plot. Of course, the axes must be labeled. A grid is optional
    plot_axes.plot(times, boing)
    plot_axes.plot(timeExp, voltExp, linestyle = 'dotted')
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()


def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot. 
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel))

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    tk_matplot(plot_example,
               xlabel="Time (ms)",
               ylabel="Voltage (V)",
               title="Experimental vs. Theoretical RC Circuit Response")

