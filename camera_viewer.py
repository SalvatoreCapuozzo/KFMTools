import os
import numpy as np
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import sys
from pathlib import Path

newWindow = None
l = None
CURRENT_DIR = os.path.dirname(__file__) #os.getcwd()

def get_correct_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parents[4]#sys.executable
    else:
        base_path = os.path.abspath(CURRENT_DIR)

    return os.path.join(base_path, relative_path)

def master(folder_path): 
    global newWindow, l
    files = os.listdir(folder_path)
    files = sorted(files)

    full_image = np.array([])
    cols_num = 12
    rows_num = 16
    image_height = 0
    image_width = 0

    folder_name = os.path.basename(folder_path)

    try:
        i = 0
        cols_array = []
        for file in files:
            if file[0] != ".":
                full_path = os.path.join(folder_path, file)
                # load the image
                image = Image.open(full_path)
                # convert image to numpy array
                data = np.asarray(image)

                image_height = data.shape[0]
                image_width = data.shape[1]

                col_idx = int(file.split('_')[1])
            
                if np.any(full_image):
                    full_image = np.concatenate([full_image, data], axis=0)
                else:
                    full_image = data

                if (i+1) % rows_num == 0:
                    col = full_image.copy()
                    cols_array.append(col)
                    full_image = np.array([])
                i += 1
                print(str(i)+"/"+str(cols_num*rows_num))

        #full_image = np.reshape(full_image, (image_height*cols_num,image_width*rows_num,3))
        print("Completing...")
        j = 0
        for col in cols_array:
            if np.any(full_image):
                full_image = np.concatenate([full_image, col], axis=1)
            else:
                full_image = col
            j += 1
            print(str(j)+"/"+str(len(cols_array)))

        im = Image.fromarray(full_image)
        print("Saving " + folder_name + ".jpeg...")
        path = folder_name+".jpeg"
        im = im.resize((9600,9600),Image.LANCZOS)
        im.save(os.path.join(CURRENT_DIR,path), optimize=True, quality=85)

        if newWindow is not None:
            newWindow.destroy()
        newWindow = Toplevel()
        newWindow.geometry("+%d+%d" %(0,0))
        #full_file_path = path.split("/")
        file_name = path[:-5]
        newWindow.title("Camera Viewer - " + file_name)
        newWindow.geometry("960x960")

        image = Image.open(os.path.join(CURRENT_DIR,path))
        resize_image = image.resize((840, 840))
        img = ImageTk.PhotoImage(resize_image)
        image_width = img.width()
        image_height = img.height()
        
        canvas = Canvas(newWindow, width=img.width(), height=img.height(),
                    borderwidth=0, highlightthickness=0)
        canvas.pack(expand=True)
        canvas.img = img
        canvas.create_image(0, 0, image=img, anchor=NW)
    except Exception as e:
        l.config(text=e)

def browse_folder():
    global folder_path
    folder_path = filedialog.askdirectory(initialdir=".")
    if folder_path == "":
        messagebox.showerror("Error", "Select a folder")
    else:
        master(folder_path)

def camera_viewer():
    global l
    window = Tk()
    window.title("Camera Viewer")
    window.geometry('400x50')
    window.geometry("+%d+%d" %(0,0))

    button_via = Button(master = window, text = 'Select images folder', width = 15, command=lambda:browse_folder())
    button_via.pack()
    l = Label(window, text = "")
    l.pack()

    window.mainloop()