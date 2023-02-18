from tkinter import *
from tkinter import ttk
from pandastable import Table


class App(Tk):
    """
    This is an App for 
    """

    def __init__(self):
        """

        """
        super().__init__()
        # This is the Title of the GUI
        self.action = IntVar()
        self.title("Smart Inventory Management App")
        self.geometry("+0+0")
        # Main Frame
        frame = Frame(self)
        frame.pack()
        # Label for App
        Label(frame, text="Smart Inventory Management App", foreground='red', font=('Arial', 25)). \
            grid(row=0, column=1)
        # Function for Data Table Section
        tableFrame = LabelFrame(frame, text='CSVs')
        tableFrame.grid(row=1, column=0, rowspan=3, columnspan=3, padx=(20, 10), pady=(20, 10), sticky="nsew")
        self.pt = Table(tableFrame, editable=False, showtoolbar=True, showstatusbar=True, rows=25, cols=20)
        # pt.importCSV(r'C:\Users\RMartin10\PycharmProjects\Rasheedattempt\CSVs\adc.csv') # Initial data
        self.pt.setTheme("dark")
        self.pt.setRowColors(clr='red')
        self.pt.show()

        # Radio Buttons for App 
        Radiobutton(frame, text='Create List', value='0', variable=self.action).grid(row=5, column=0)
        Radiobutton(frame, text='Edit List', value='1', variable=self.action).grid(row=5, column=1)
        Radiobutton(frame, text='Stock Prediction Algorithm', value='2', variable=self.action).grid(row=5, column=2,
                                                                                                    padx=25)

        # Button
        Button(frame, text="Submit",
               width=10, command=self.submit_action).grid(row=12, column=1, pady=5,
                                                          padx=10, sticky="nsew")

    def submit_action(self) -> None:
        """

        :return:
        """
        # If else
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()
