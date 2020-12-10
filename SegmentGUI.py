from tkinter import filedialog, Tk, Label, Button, StringVar, OptionMenu, Entry, END, E, W
import ENSC424projectClass
import ntpath
import os
import shutil

OPTIONS = [
"Bear",
"Wolf",
"Deer",
"Beaver"
]

class Application:
    def __init__(self, master):
        self.master = master
        master.title("AI Video Segmentation")
        #Allowing automatic sizing when expanding the windows
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)
        master.grid_columnconfigure(3, weight=1)
        master.grid_columnconfigure(4, weight=1)

        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(1, weight=1)
        master.grid_rowconfigure(2, weight=1)
        master.grid_rowconfigure(3, weight=1)
        master.grid_rowconfigure(4, weight=1)
        master.grid_rowconfigure(5, weight=1)
        master.grid_rowconfigure(6, weight=1)
        master.grid_rowconfigure(7, weight=1)
        master.grid_rowconfigure(8, weight=1)

        #setting up predetermined classes for object detection
        self.class_lbl = Label(master, text="Choose animal of interest")
        self.class_lbl.grid(row=1, column=2)

        self.variable = StringVar(master)
        self.variable.set(OPTIONS[0])

        self.w = OptionMenu(master, self.variable, *OPTIONS)
        self.w.grid(row=3, column=2)

        #creates the text box for adding video input
        self.File_lbl = Label(master, text="Select Video File to segment")
        self.File_lbl.grid(row=4, column=2)

        # set the text box for video input to write and edit
        self.ent = Entry(master, font=5, state='readonly')
        self.ent.grid(row=5, column=1,columnspan = 2, sticky = W+E)

        #connecting browsefile funtion to video input text box
        self.b1 = Button(master, text="Browse", font=40, command=self.browsefile)
        self.b1.grid(row=5, column=4,sticky=W)

        #creates the text box for the output destination
        self.Folder_lbl = Label(master, text="Select Save Folder")
        self.Folder_lbl.grid(row=6, column=2)

        #set the text box for output destination to write and edit
        self.ent2 = Entry(master, font=5, state='readonly')
        self.ent2.grid(row=7, column=1,columnspan = 2, sticky = W+E)

        #connecting browsedirection function to output destination
        self.b2 = Button(master, text="Browse", font=40, command=self.browsedirect)
        self.b2.grid(row=7, column=4,sticky=W)

        #creates the open button and binds the ok function to it
        self.button = Button(master, text="OK", command=self.ok)
        self.button.grid(row=8, column=2)


    #opens browse menu and looks through files of type .mp4 or anyother types of video
    def browsefile(self):
        filename = filedialog.askopenfilename(filetypes=(("mp4 file", "*.mp4"), ("All files", " *.* "),))
        self.ent.config(state='normal')
        self.ent.insert(END, filename)
        self.ent.config(state='readonly')

    #opens the browse menu and saves the folder location
    def browsedirect(self):
        directory = filedialog.askdirectory()
        self.ent2.config(state='normal')
        self.ent2.insert(END, directory)
        self.ent2.config(state='readonly')

    #runs through the OpenCv and Video Segmentation code
    def ok(self):
        print("Searching for " + self.variable.get() + "s in file " + self.ent.get())
        #creates python object for our Video Segmentation Program
        Video = ENSC424projectClass.media_interpret()
        #sets up the video and images folder
        Video.setupFold()
        #Gets the file path for the video input
        file=self.ent.get()
        file.encode('unicode_escape')
        print(file)
        #sends video to video segmentation and extract properties of video
        Video.readVideo(file)
        #extracts the file names and prepare the names of the output video and text files
        (filename, ext) = os.path.splitext(ntpath.basename(file))
        temp_filename = filename + "_segmented.txt"
        filename = filename+"_segmented.avi"
        #determines the output location based on user input
        filepath = self.ent2.get() + "/"+filename
        filepath.encode('unicode_escape')
        #runs iterative loop to run through video frames and cuts irrelevant frames to output video
        Video.image_runthrough(self.variable.get(), vidName=filepath)
        #using information from image_runthrough creates text file in the same location as video output
        Video.output_interest_timestamp(temp_filename, self.ent2.get()+"/")
        #returns resources take for the video segmentation
        Video.proper_end()
        #exits the GUI application
        self.master.quit()


def main():
    """Creates the GUI application window and fills it based on Application class"""
    root = Tk()
    #fills the GUI application window with widgets tied to video segmenation program
    GUI = Application(root)
    #loops operating the GUI which keeps it reponsive
    root.mainloop()

if __name__ == "__main__":
    #when this program is run by itself call the main function
    main()