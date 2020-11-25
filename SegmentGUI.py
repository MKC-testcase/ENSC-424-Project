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



        self.class_lbl = Label(master, text="Choose animal of interest")
        self.class_lbl.grid(row=1, column=2)

        self.variable = StringVar(master)
        self.variable.set(OPTIONS[0])

        self.w = OptionMenu(master, self.variable, *OPTIONS)
        self.w.grid(row=3, column=2)

        self.File_lbl = Label(master, text="Select Video File to segment")
        self.File_lbl.grid(row=4, column=2)

        self.ent = Entry(master, font=5, state='readonly')
        self.ent.grid(row=5, column=1,columnspan = 2, sticky = W+E)

        self.b1 = Button(master, text="Browse", font=40, command=self.browsefile)
        self.b1.grid(row=5, column=4,sticky=W)

        self.Folder_lbl = Label(master, text="Select Save Folder")
        self.Folder_lbl.grid(row=6, column=2)

        self.ent2 = Entry(master, font=5, state='readonly')
        self.ent2.grid(row=7, column=1,columnspan = 2, sticky = W+E)

        self.b2 = Button(master, text="Browse", font=40, command=self.browsedirect)
        self.b2.grid(row=7, column=4,sticky=W)

        self.button = Button(master, text="OK", command=self.ok)
        self.button.grid(row=8, column=2)



    def browsefile(self):
        filename = filedialog.askopenfilename(filetypes=(("mp4 file", "*.mp4"), ("All files", " *.* "),))
        self.ent.config(state='normal')
        self.ent.insert(END, filename)
        self.ent.config(state='readonly')

    def browsedirect(self):
        directory = filedialog.askdirectory()
        self.ent2.config(state='normal')
        self.ent2.insert(END, directory)
        self.ent2.config(state='readonly')

    def ok(self):
        print("Searching for " + self.variable.get() + "s in file " + self.ent.get())
        Video = ENSC424projectClass.media_interpret()
        Video.setupFold()
        file=self.ent.get()
        file.encode('unicode_escape')
        print(file)
        Video.readVideo(file)
        (filename, ext) = os.path.splitext(ntpath.basename(file))
        temp_filename = filename + ".txt"
        filename = filename+"_segmented.avi"
        filepath = self.ent2.get() + "/"+filename
        filepath.encode('unicode_escape')
        Video.image_runthrough(self.variable.get(), vidName=filepath)
        #Video.output_interest_timestamp(temp_filename)
        Video.proper_end()
        self.master.quit()


def main():
    root = Tk()
    GUI = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()