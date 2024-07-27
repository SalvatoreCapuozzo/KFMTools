from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import shutil
import sys
from pathlib import Path

folder_path = ""
image_path = ""
path = ""
index = 0
folder_size = 0
newWindow = None
image_width = 0
image_height = 0
topx, topy, botx, boty = 0,0,0,0
pressed = 0
topx_array, topy_array, botx_array, boty_array = [], [], [], []
rect_id = None
incremental_id = 0
rects = []
texts = []
obj_texts = []
obj_buttons = []
objects_list = []
images_list = []
CURRENT_DIR = os.path.dirname(__file__) #os.getcwd()
variable = None
focusVariable = None
imgNameVariable = None
counter = None
l = None
classes_list = []
frame_width = 720
frame_height = 540

def get_correct_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parents[4]#sys.executable
    else:
        base_path = os.path.abspath(CURRENT_DIR)

    return os.path.join(base_path, relative_path)

with open(get_correct_path("config/classes_list.txt"), "r") as class_file:
    classes_list = [line.replace("\n","") for line in class_file.readlines()]

colors_list = []

with open(get_correct_path("config/colors_list.txt"), "r") as color_file:
    colors_list = [line.replace("\n","") for line in color_file.readlines()]

focus_list = []

with open(get_correct_path("config/focuses_list.txt"), "r") as focus_file:
    focus_list = [line.replace("\n","") for line in focus_file.readlines()]

class_name = classes_list[0]
focus_value = focus_list[0]

def is_valid(x):
    return x[0] != "."

#def display_selected(choice):
#    choice = imgNameVariable.get()

def changeImageName():
    full_file_path = path.split("/")
    folder_base_name = os.path.basename(os.path.dirname(folder_path))
    #labels_path = get_correct_path("labels")
    #images_path = get_correct_path("images")
    #focus_labels_path = get_correct_path("focus_labels")
    labels_path = os.path.join(os.path.dirname(folder_path),"labels")
    images_path = os.path.join(os.path.dirname(folder_path),"images")
    focus_labels_path = os.path.join(os.path.dirname(folder_path),"focus_labels")

    if image_path[:5] == "micro":
        file_name = folder_base_name+"_"+image_path[:-4]+".txt" #image_path[:-4]+".txt"
        focus_file_name = folder_base_name+"_"+image_path[:-4]+"_focus.txt"
        img_file_name = folder_base_name+"_"+image_path
    else:
        file_name = image_path[:-4]+".txt"
        focus_file_name = image_path[:-4]+"_focus.txt"
        img_file_name = image_path

    if os.path.join(folder_path,full_file_path[-1],image_path) != os.path.join(images_path,img_file_name):
        shutil.copyfile(os.path.join(folder_path,full_file_path[-1],image_path), os.path.join(images_path,img_file_name))

    if image_path[:5] == "micro":
        os.remove(os.path.join(folder_path,full_file_path[-1],image_path))

#APERTURA FINESTRA LABELING
def master(folder_path): 
    global rect_id, index, folder_size, newWindow, image_width, image_height, canvas, variable, focusVariable, image_path, incremental_id, classes_list, colors_list, focus_list, l, images_list, imgNameVariable

    pathList = sorted(os.listdir(folder_path))
    pathList = list(filter(is_valid, pathList))
    folder_size = len(pathList)
    attempt = 0
    incremental_id = 0
    images_list = pathList

    try:
        image_path = pathList[index]
        while image_path[-4:] != ".png" and image_path[-4:] != ".jpg" and image_path[-5:] != ".jpeg":
            index = (index+1)%folder_size
            attempt += 1
            if attempt > 20:
                raise Exception("There is no valid image in this folder")
            image_path = pathList[index]

        path = os.path.join(folder_path,image_path)
    except Exception as e:
        print(e)
        #l.config(text=e)

    changeImageName()

    pathList = sorted(os.listdir(folder_path))
    pathList = list(filter(is_valid, pathList))
    folder_size = len(pathList)
    attempt = 0
    incremental_id = 0
    images_list = pathList

    try:
        image_path = pathList[index]
        while image_path[-4:] != ".png" and image_path[-4:] != ".jpg" and image_path[-4:] != ".jpeg":
            index = (index+1)%folder_size
            attempt += 1
            if attempt > 20:
                raise Exception("There is no valid image in this folder")
            image_path = pathList[index]

        path = os.path.join(folder_path,image_path)
    except Exception as e:
        print(e)
        l.config(text=e)

    pathList = sorted(os.listdir(folder_path))
    pathList = list(filter(is_valid, pathList))
    folder_size = len(pathList)
    attempt = 0
    incremental_id = 0
    images_list = pathList

    try:
        #CREAZIONE DELLA FINESTRA
        if newWindow is not None:
            newWindow.destroy()
        newWindow = tk.Toplevel()
        newWindow.geometry("+%d+%d" %(0,0))
        full_file_path = path.split("/")
        file_name = full_file_path[-1][:-4]
        newWindow.title("Images Labeler - " + file_name)
        newWindow.geometry("1520x960")

        image = Image.open(path)
        resize_image = image.resize((frame_width, frame_height)) #1280,960 - 1200,900 - 400,300 - 800,600 - 960,720
        img = ImageTk.PhotoImage(resize_image)
        image_width = img.width()
        image_height = img.height()
        
        canvas = tk.Canvas(newWindow, width=img.width(), height=img.height(),
                    borderwidth=0, highlightthickness=0)
        #canvas.pack(expand=True)
        canvas.place(x=5,y=60)
        canvas.img = img
        canvas.create_image(0, 0, image=img, anchor=tk.NW)

        color = 'white'
        
        btn = tk.Button(newWindow, text='Save labels (S)', width=15, height=3, font=('Helvetica 8'), command = save)
        cancFirstBtn = tk.Button(newWindow, text='Cancel first (F)', width=15, height=3, font=('Helvetica 8'), command = cancelFirst)
        backBtn = tk.Button(newWindow, text='Cancel last (L)', width=15, height=3, font=('Helvetica 8'), command = cancelLast)
        prevBtn = tk.Button(newWindow, text='Previous image (A)', width=15, height=3, font=('Helvetica 8'), command = prevImage)
        nextBtn = tk.Button(newWindow, text='Next image (D)', width=15, height=3, font=('Helvetica 8'), command = nextImage)
        deleteBtn = tk.Button(newWindow, text='Delete image (X)', width=15, height=3, font=('Helvetica 8'), command = deleteImage)
        btn.place(x=10, y=15)
        cancFirstBtn.place(x=130, y=15)
        backBtn.place(x=250, y=15)
        prevBtn.place(x=370, y=15)
        nextBtn.place(x=490, y=15)
        deleteBtn.place(x=610, y=15)
        #canvas.bind('<Button-1>', get_mouse_posn)
        canvas.bind('<B1-Motion>', update_sel_rect)
        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<ButtonRelease>", on_release)
        newWindow.bind('<KeyPress>', on_key_press)

        idx = 0
        if variable != None:
            idx = classes_list.index(variable.get())
        variable = tk.StringVar(newWindow)
        variable.set(classes_list[idx])
        w = tk.OptionMenu(newWindow, variable, *classes_list)
        w.place(x=740, y=2)
        var = variable.get()
        color = colors_list[classes_list.index(var)]
        rect_id = canvas.create_rectangle(topx, topy, topx, topy, dash=(2,2), fill='', outline=color)

        focusVariable = tk.StringVar(newWindow)
        focusVariable.set(focus_list[0])
        w2 = tk.OptionMenu(newWindow, focusVariable, *focus_list)
        w2.place(x=740, y=26)

        imgNameVariable = tk.StringVar(newWindow)
        imgNameVariable.set(images_list[index])
        imgNameVariable.trace_add("write", selectedImage)
        t1 = tk.OptionMenu(newWindow, imgNameVariable, *images_list)
        t1.place(x=900,y=15)

        load()
    except Exception as e:
        l.config(text=e)

#CLASSI
class LabeledObject:
    def __init__(self,class_id,top_x,top_y,bot_x,bot_y,focus_id):
        self.top_x = top_x
        self.top_y = top_y 
        self.bot_x = bot_x
        self.bot_y = bot_y
        self.class_id = class_id
        self.focus_id = focus_id
    
    def __str__(self):
        return str(self.class_id) + " - " +str(self.class_id)+  " - ["+str(self.top_x)+","+str(self.top_y)+","+str(self.bot_x)+","+str(self.bot_y)+"] " + str(self.focus_id)

class Counter():
    global rects, class_name

    def __init__(self, parent, end, start=0, increment=1, interval=5):
        self.parent = parent
        self.start_value = start
        self.end_value = end
        self.increment = -increment if (end - start) * increment < 0 else increment
        self.interval = interval
        self.value = start
        self.running = False

    def start(self):
        '''Start counter'''
        self.value = self.start_value
        self.running = True
        self.doit()

    def stop(self):
        '''Stop counter'''
        self.running = False

    def doit(self):
        '''Called periodically to incrementer counter and print value'''
        if self.running:
            #print('Counter value =', self.value)
            self.value += self.increment
            self.running = (self.end_value - self.value) * self.increment > 0
            
            if len(rects) > 0 and self.value < self.start_value-1:
                canvas.delete(rects.pop())
            #class_id = variable.get()
            #if not (class_id == "Select the class"):
            color = colors_list[classes_list.index(class_name)]
            #print(color)

            rect_id = canvas.create_rectangle(topx, topy, botx, boty, dash=(2,2), fill='', outline=color,width=3)
            rects.append(rect_id)

            if self.running:
                self.parent.after(self.interval, self.doit)

def update_sel_rect(event):
    global topy, topx, botx, boty
    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)
    return topx, topy, botx, boty

def on_key_press(event):
    key = event.char
    if key == 'd':
        nextImage()
    elif key == 'a':
        prevImage()
    elif key == 's':
        save()
    elif key == 'l':
        cancelLast()
    elif key == 'f':
        cancelFirst()
    elif key == 'x':
        deleteImage()

def on_press(event):
    global topy, topx, botx, boty, pressed, counter, class_name

    if not pressed:
        pressed = 1
        topx, topy = event.x, event.y
        botx, boty = event.x, event.y
        counter.start()
    color = 'white'
    class_name = variable.get()
    #if len(rects) > 0:
        #canvas.delete(rects.pop())

    if not (class_name == classes_list[0]):
        color = colors_list[classes_list.index(class_name)]
        print(color)

        #rect_id = canvas.create_rectangle(topx, topy, botx, boty, dash=(2,2), fill='', outline=color,width=3)
        #rects.append(rect_id)

def remove_obj(rect,text,obj_text,obj):
    canvas.delete(rect)
    canvas.delete(text)
    obj_text.destroy()
    #obj_button.destroy()
    rects.remove(rect)
    texts.remove(text)
    obj_texts.remove(obj_text)
    obj_buttons.remove(obj_buttons[objects_list.index(obj)])
    objects_list.remove(obj)


def on_release(event):
    global topy, topx, botx, boty, pressed, incremental_id
    
    pressed = 0
    color = 'white'
    #class_id = variable.get()
    counter.stop()
    focus_value = focusVariable.get()

    if not (class_name == classes_list[0]):
        topx_array.append(topx)
        topy_array.append(topy)
        botx_array.append(botx)
        boty_array.append(boty)

        if len(rects) > 0:
            canvas.delete(rects.pop())

        class_id = classes_list.index(class_name)
        color = colors_list[classes_list.index(class_name)]
        print(color)
        focus_id = focus_list.index(focus_value)

        obj = LabeledObject(class_id,topx, topy, botx, boty, focus_id)
        objects_list.append(obj)

        rect_id = canvas.create_rectangle(topx, topy, botx, boty, dash=(2,2), fill='', outline=color,width=3)
        rects.append(rect_id)
        
        focus_id = focus_list.index(focus_value)
        text = "[ID: "+str(incremental_id)+"] C: "+str(class_id)+" - F: "+str(focus_id)
        text_id = canvas.create_text(topx, topy, text=text, fill="black", font=('Helvetica 12 bold'))
        texts.append(text_id)
        print(str(class_name) + " - topx = " + str(topx) + " topy = " + str(topy) + " botx = " + str(botx) + " boty = " + str(boty) + " focus = " + str(focus_value))
        
        obj_text = tk.Label(newWindow, text=text)
        obj_text.config(font =("Courier", 10))
        obj_text.place(x=frame_width+55, y=(incremental_id)*25+55)
        obj_texts.append(obj_text)
        obj_button = tk.Button(newWindow, text="X", command=lambda r=rect_id, t=text_id, o=obj_text, j=obj: remove_obj(r,t,o,j))
        obj_button.place(x=frame_width+5, y=(incremental_id)*25+50)
        obj_buttons.append(obj_button)
        incremental_id += 1
        
    else:
        messagebox.showerror("Error", "Select the class before proceeding")

def cancelFirst():
    global topy, topx, botx, boty, incremental_id
    
    if len(rects) == 0:
        messagebox.showerror("Error", "The image is already empty")
    else:
        if len(topx_array) != 0:
            topx = topx_array.pop(0)
            botx = botx_array.pop(0)
            topy = topy_array.pop(0)
            boty = boty_array.pop(0)

        canvas.coords(rect_id, 0, 0, 0, 0)
        canvas.delete(rects.pop(0))
        canvas.delete(texts.pop(0))
        obj_text = obj_texts.pop(0)
        obj_text.destroy()
        obj_button = obj_buttons.pop(0)
        obj_button.destroy()

        objects_list.pop(0)
        incremental_id -= 1

def cancelLast():
    global topy, topx, botx, boty, incremental_id
    
    if len(rects) == 0:
        messagebox.showerror("Error", "The image is already empty")
    else:
        if len(topx_array) != 0:
            topx = topx_array.pop()
            botx = botx_array.pop()
            topy = topy_array.pop()
            boty = boty_array.pop()

        canvas.coords(rect_id, 0, 0, 0, 0)
        canvas.delete(rects.pop())
        canvas.delete(texts.pop())
        obj_text = obj_texts.pop()
        obj_text.destroy()
        obj_button = obj_buttons.pop()
        obj_button.destroy()

        objects_list.pop()
        incremental_id -= 1

def selectedImage(*args):
    global index, imgNameVariable
    name = imgNameVariable.get()
    index = images_list.index(name)
    imgNameVariable.set(images_list[index])
    master(folder_path)

def nextImage():
    global index, folder_size, imgNameVariable
    index = (index+1)%folder_size
    imgNameVariable.set(images_list[index])
    master(folder_path)

def prevImage():
    global index, folder_size, imgNameVariable
    index = (index-1)%folder_size
    imgNameVariable.set(images_list[index])
    master(folder_path)

def deleteImage():
    labels_path = os.path.join(os.path.dirname(folder_path),"labels")
    images_path = os.path.join(os.path.dirname(folder_path),"images")

    folder_base_name = os.path.basename(folder_path)
    if image_path[:5] == "micro":
        file_name = folder_base_name+"_"+image_path[:-4]+".txt" #image_path[:-4]+".txt"
    else:
        file_name = image_path[:-4]+".txt"

    full_image_path = os.path.join(images_path, image_path)
    full_label_path = os.path.join(labels_path, file_name)

    try:
        os.remove(full_image_path)
        os.remove(full_label_path)
    except Exception as e:
        print(e)

    master(folder_path)
    

def load():
    global image_path, incremental_id
    rects.clear()
    texts.clear()
    obj_texts.clear()
    objects_list.clear()
    incremental_id = 0

    folder_base_name = os.path.basename(os.path.dirname(folder_path))
    labels_path = os.path.join(os.path.dirname(folder_path),"labels")
    images_path = os.path.join(os.path.dirname(folder_path),"images")
    focus_labels_path = os.path.join(os.path.dirname(folder_path),"focus_labels")
    #labels_path = get_correct_path("labels")
    #images_path = get_correct_path("images")
    #focus_labels_path = get_correct_path("focus_labels")
    if not os.path.exists(labels_path):
        os.mkdir(labels_path)
    if not os.path.exists(images_path):
        os.mkdir(images_path)
    if not os.path.exists(focus_labels_path):
        os.mkdir(focus_labels_path)

    if image_path[:5] == "micro":
        file_name = folder_base_name+"_"+image_path[:-4]+".txt" #image_path[:-4]+".txt"
        focus_file_name = folder_base_name+"_"+image_path[:-4]+"_focus.txt"
        if not os.path.exists(os.path.join(labels_path,file_name)):
            file_name = image_path[:-4]+".txt"
            focus_file_name = image_path[:-4]+"_focus.txt"
    else:
        file_name = image_path[:-4]+".txt"
        focus_file_name = image_path[:-4]+"_focus.txt"
    
    #print(file_name)
    print(os.path.join(labels_path,file_name))
    focus_exists = os.path.exists(os.path.join(focus_labels_path,focus_file_name))
    label_exists = os.path.exists(os.path.join(labels_path,file_name))
    if label_exists:
        if focus_exists:
            file_path = os.path.join(focus_labels_path,focus_file_name)
        else:
            file_path = os.path.join(labels_path,file_name)
        with open(file_path, 'r') as input_file:
            obj_lines = input_file.readlines()
            for line in obj_lines:
                if line != "":
                    obj_list = line.replace("\n","").split(" ")
                    class_id = int(obj_list[0])
                    x_center = int(float(obj_list[1])*float(image_width))
                    y_center = int(float(obj_list[2])*float(image_height))
                    delta_width = int(float(obj_list[3])*float(image_width))
                    delta_height = int(float(obj_list[4])*float(image_height))
                    x_min = x_center - delta_width/2
                    y_min = y_center - delta_height/2
                    if focus_exists:
                        focus_id = int(obj_list[5])
                    else:
                        focus_id = 0
                    obj = LabeledObject(class_id,x_min,y_min,x_min+delta_width,y_min+delta_height,focus_id)
                    objects_list.append(obj)
                    class_name = classes_list[class_id]
                    color = colors_list[class_id]
                    rect_id = canvas.create_rectangle(x_min, y_min, x_min+delta_width, y_min+delta_height, dash=(2,2), fill='', outline=color,width=3)
                    rects.append(rect_id)

                    text = "[ID: "+str(incremental_id)+"] C: "+str(class_id)+" - F: "+str(focus_id)
                    text_id = canvas.create_text(x_min, y_min, text=text, fill="black", font=('Helvetica 12 bold'))
                    texts.append(text_id)
                    
                    obj_text = tk.Label(newWindow, text=text)
                    obj_text.config(font =("Courier", 10))
                    obj_text.place(x=frame_width+55, y=(incremental_id)*25+55)
                    obj_texts.append(obj_text)
                    
                    obj_button = tk.Button(newWindow, text="X", command=lambda r=rect_id, t=text_id, o=obj_text, j=obj: remove_obj(r,t,o,j))
                    obj_button.place(x=frame_width+5, y=(incremental_id)*25+50)
                    obj_buttons.append(obj_button)
                    incremental_id += 1
    
def save():
    global image_width, image_height, image_path
    #labels_path = get_correct_path("labels")
    #images_path = get_correct_path("images")
    #focus_labels_path = get_correct_path("focus_labels")
    labels_path = os.path.join(os.path.dirname(folder_path),"labels")
    images_path = os.path.join(os.path.dirname(folder_path),"images")
    focus_labels_path = os.path.join(os.path.dirname(folder_path),"focus_labels")
    if not os.path.exists(labels_path):
        os.mkdir(labels_path)
    if not os.path.exists(images_path):
        os.mkdir(images_path)
    if not os.path.exists(focus_labels_path):
        os.mkdir(focus_labels_path)
    
    file_name = image_path[:-4]+".txt"
    focus_file_name = image_path[:-4]+"_focus.txt"
    img_file_name = image_path
    
    #if image_path[:5] == "micro":
    #    file_name = folder_base_name+"_"+image_path[:-4]+".txt" #image_path[:-4]+".txt"
    #    focus_file_name = folder_base_name+"_"+image_path[:-4]+"_focus.txt"
    #    img_file_name = folder_base_name+"_"+image_path
    #else:
    #    file_name = image_path[:-4]+".txt"
    #    focus_file_name = image_path[:-4]+"_focus.txt"
    #    img_file_name = image_path
    
    #path_string = full_file_path[-1].split(".")
    output_string = ""
    focus_output_string = ""
    for obj in objects_list:
        x_min = min(obj.top_x,obj.bot_x)
        y_min = min(obj.top_y, obj.bot_y)
        x_max = max(obj.top_x,obj.bot_x)
        y_max = max(obj.top_y, obj.bot_y)
        delta_x = abs(x_max-x_min)
        delta_y = abs(y_max-y_min)
        curr_line = f"{obj.class_id} {(x_min+delta_x/2)/image_width} {(y_min+delta_y/2)/image_height} {delta_x/image_width} {delta_y/image_height}"
        output_string += curr_line + "\n"
        focus_output_string += curr_line + f" {obj.focus_id}\n"
    
    with open(os.path.join(labels_path,file_name), 'w') as output_file:
        output_file.write(output_string)
        output_file.close()

    with open(os.path.join(focus_labels_path,focus_file_name), 'w') as focus_output_file:
        focus_output_file.write(focus_output_string)
        focus_output_file.close()
    
    #if os.path.join(folder_path,full_file_path[-1],image_path) != os.path.join(images_path,img_file_name):
    #    shutil.copyfile(os.path.join(folder_path,full_file_path[-1],image_path), os.path.join(images_path,img_file_name))

    #if image_path[:5] == "micro":
    #    os.remove(os.path.join(folder_path,full_file_path[-1],image_path))

    if len(objects_list) == 0:
        if os.path.exists(os.path.join(labels_path,file_name)):
            os.remove(os.path.join(labels_path,file_name))
        if os.path.exists(os.path.join(focus_labels_path,focus_file_name)):
            os.remove(os.path.join(focus_labels_path,focus_file_name))
        if os.path.exists(os.path.join(images_path,img_file_name)):
            os.remove(os.path.join(images_path,img_file_name))

    messagebox.showinfo("Save complete", "N."+str(len(rects))+" objects saved in label file "+img_file_name + ".\nnow you can close the program, move to the next image or continue adding labels.")


#APERTURA ESPLORA RISORSE PER PRENDERE L'IMMAGINE
def browse_folder():
    global folder_path
    folder_path = filedialog.askdirectory(initialdir=".")
    if folder_path == "":
        messagebox.showerror("Error", "Select a folder")
    else:
        master(folder_path)

#def browse_file():
#    path = filedialog.askopenfilename(filetypes = (("jpg files", "*.jpg"), ("png files", "*.png"), ("All files", "*")))
#    if path=="":
#        messagebox.showerror("Error", "Select a folder")
#    else:
#        master(path)


def images_labeler():
    #global window
    global counter
    window = tk.Tk()
    window.title("Images Labeler")
    window.geometry('400x50')
    window.geometry("+%d+%d" %(0,0))
    counter = Counter(window, 0, 1000)

    #---------------------------MAIN---------------------------#
    #C = Canvas(window, bg="blue", height=250, width=300)
    button_via = tk.Button(master = window, text = 'Select images folder', width = 15, command=lambda:browse_folder())
    button_via.pack()
    l = tk.Label(window, text = "")
    l.pack()

    window.mainloop()
    ########################

#images_labeler()