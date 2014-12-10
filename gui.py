from Tkinter import Tk, Frame, BOTH

#Is (Frame) telling it to derive from the class frame that we imported?
class Window(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background = "black")
        self.parent = parent
        self.initUI()
        self.centerWindow()


    def initUI(self):
        self.parent.title("Example GUI")
        self.pack(fill=BOTH, expand = 1)

    def centerWindow(self):
        w = 640
        h = 320

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x = (screen_width - w) / 2
        y = (screen_height - h) / 2
        self.parent.geometry("%dx%d+%d+%d" % (w, h, x, y))


def main():

    root = Tk()
    app = Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()
