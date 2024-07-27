from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import messagebox
from zipfile import ZipFile 
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
c_obj_buttons = []
w_obj_buttons = []
m_obj_buttons = []
objects_list = []
CURRENT_DIR = os.path.dirname(__file__) #os.getcwd()
variable = None
imgNameVariable = None
counter = None
l = None
classes_list = []
images_list = []
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

class_name = classes_list[0]

def is_valid(x):
    return x[0] != "."

#APERTURA FINESTRA LABELING
def master(folder_path): 
    global rect_id, index, folder_size, newWindow, image_width, image_height, canvas, variable, image_path, incremental_id, classes_list, colors_list, l, imgNameVariable, images_list

    session_name = os.path.basename(folder_path)
    #zip_file = os.path.join(folder_path,session_name+".zip")
    pred_labels_folder = os.path.join(folder_path,session_name+"_DetectionOutput","labels")
    gt_labels_folder = os.path.join(folder_path,"labels")
    images_folder = os.path.join(folder_path,"images")

    """
    if not os.path.exists(images_folder):
        # loading the temp.zip and creating a zip object 
        with ZipFile(zip_file, 'r') as zObject: 
            # Extracting all the members of the zip  
            # into a specific location. 
            zObject.extractall(path=images_folder)
    """

    
    pathList = sorted(os.listdir(images_folder))
    pathList = list(filter(is_valid, pathList))
    folder_size = len(pathList)
    attempt = 0
    incremental_id = 0
    #image_width = img.width()
    #image_height = img.height()
    images_list = pathList

    try:
        image_path = pathList[index]
        while image_path[-4:] != ".png" and image_path[-4:] != ".jpg" and image_path[-4:] != ".jpeg":
            index = (index+1)%folder_size
            attempt += 1
            if attempt > 20:
                raise Exception("There is no valid image in this folder")
            image_path = pathList[index]

        path = os.path.join(images_folder,image_path)
    except Exception as e:
        print(e)
        l.config(text=e)

    try:
        #CREAZIONE DELLA FINESTRA
        if newWindow is not None:
            newWindow.destroy()
        newWindow = tk.Toplevel()
        newWindow.geometry("+%d+%d" %(0,0))
        full_file_path = path.split("/")
        file_name = full_file_path[-1][:-4]
        newWindow.title("Labeling - " + file_name)
        newWindow.geometry("1520x960")

        image = Image.open(path)
        resize_image = image.resize((frame_width, frame_height)) #1280,960
        img = ImageTk.PhotoImage(resize_image)
        image_width = img.width()
        image_height = img.height()
        
        canvas = tk.Canvas(newWindow, width=img.width(), height=img.height(),
                    borderwidth=0, highlightthickness=0)
        #canvas.pack(expand=True)
        canvas.place(x=0,y=60)
        canvas.img = img
        canvas.create_image(0, 0, image=img, anchor=tk.NW)

        color = 'white'
        
        btn = tk.Button(newWindow, text='Save analysis (S)', width=15, height=3, font=('Helvetica 8'), command = save)
        backBtn = tk.Button(newWindow, text='Cancel last (W)', width=15, height=3, font=('Helvetica 8'), command = cancel)
        prevBtn = tk.Button(newWindow, text='Previous image (A)', width=15, height=3, font=('Helvetica 8'), command = prevImage)
        nextBtn = tk.Button(newWindow, text='Next image (D)', width=15, height=3, font=('Helvetica 8'), command = nextImage)
        btn.place(x=10, y=15)
        backBtn.place(x=150, y=15)
        prevBtn.place(x=290, y=15)
        nextBtn.place(x=430, y=15)
        #canvas.bind('<Button-1>', get_mouse_posn)
        canvas.bind('<B1-Motion>', update_sel_rect)
        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<ButtonRelease>", on_release)
        newWindow.bind('<KeyPress>', on_key_press)

        variable = tk.StringVar(newWindow)
        variable.set(classes_list[0])
        w = tk.OptionMenu(newWindow, variable, *classes_list)
        w.place(x=640, y=15)
        var = variable.get()
        color = colors_list[classes_list.index(var)]
        rect_id = canvas.create_rectangle(topx, topy, topx, topy, dash=(2,2), fill='', outline=color)

        imgNameVariable = tk.StringVar(newWindow)
        imgNameVariable.set(images_list[index])
        imgNameVariable.trace_add("write", selectedImage)
        t1 = tk.OptionMenu(newWindow, imgNameVariable, *images_list)
        t1.place(x=960,y=15)

        load()
    except Exception as e:
        l.config(text=e)

#CLASSI
class LabeledObject:
    def __init__(self,class_id,top_x,top_y,bot_x,bot_y,status):
        self.top_x = top_x
        self.top_y = top_y 
        self.bot_x = bot_x
        self.bot_y = bot_y
        self.class_id = class_id
        self.status = status
    
    def __str__(self):
        return str(self.class_id) + " - " +str(self.class_id)+  " - ["+str(self.top_x)+","+str(self.top_y)+","+str(self.bot_x)+","+str(self.bot_y)+"] "+str(self.status)

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
    elif key == 'w':
        cancel()

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
def set_as(status,obj_text,obj):
    objects_list[objects_list.index(obj)].status = status
    obj.status = status

    obj_text.config(text = "[ID: "+str(objects_list.index(obj))+"] C: "+str(obj.class_id)+", "+str(status))
    obj_texts[objects_list.index(obj)].config(text = "[ID: "+str(objects_list.index(obj))+"] C: "+str(obj.class_id)+", "+str(status))

def on_release(event):
    global topy, topx, botx, boty, pressed, incremental_id
    
    pressed = 0
    color = 'white'
    #class_id = variable.get()
    counter.stop()

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

        status = "FN"
        obj = LabeledObject(class_id,topx, topy, botx, boty, status)
        objects_list.append(obj)

        rect_id = canvas.create_rectangle(topx, topy, botx, boty, dash=(2,2), fill='', outline=color,width=3)
        rects.append(rect_id)
        
        text = "[ID: "+str(incremental_id)+"] C: "+str(class_id)
        text_id = canvas.create_text(topx, topy, text=text, fill="black", font=('Helvetica 12 bold'))
        texts.append(text_id)
        print(str(class_name) + " - topx = " + str(topx) + " topy = " + str(topy) + " botx = " + str(botx) + " boty = " + str(boty))
        
        obj_text = tk.Label(newWindow, text=text+", "+status)
        obj_text.config(font =("Courier", 10))
        obj_text.place(x=frame_width, y=(incremental_id)*25+55)
        obj_texts.append(obj_text)

        incremental_id += 1
        
    else:
        messagebox.showerror("Error", "Select the class before proceeding")

def cancel():
    global topy, topx, botx, boty, incremental_id
    fn_count = 0
    for o in objects_list:
        if o.status == "FN":
            fn_count += 1
    if len(rects) == 0:
        messagebox.showerror("Error", "The image is already empty")
    elif fn_count == 0:
        messagebox.showerror("Error", "You cannot cancel predictions. If they are wrong, put them as false positive (FP)")
    else:
        topx = topx_array.pop()
        botx = botx_array.pop()
        topy = topy_array.pop()
        boty = boty_array.pop()

        canvas.coords(rect_id, 0, 0, 0, 0)
        canvas.delete(rects.pop())
        canvas.delete(texts.pop())
        obj_text = obj_texts.pop()
        obj_text.destroy()

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

def load():
    global image_path, incremental_id
    folder_base_name = os.path.basename(folder_path)

    file_name = image_path[:-4]+".txt"
    gt_labels_path = os.path.join(folder_path,"labels",file_name)
    pred_labels_path = os.path.join(folder_path,folder_base_name+"_DetectionOutput","labels",file_name)
    labels_list = [pred_labels_path, gt_labels_path]
    for labels_path in labels_list:
        label_exists = os.path.exists(labels_path)
        if label_exists:
            file_path = labels_path
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
                        default_class = "C"
                        obj = LabeledObject(class_id,x_min,y_min,x_min+delta_width,y_min+delta_height,default_class)
                        objects_list.append(obj)
                        class_name = classes_list[class_id]
                        color = colors_list[class_id]
                        if labels_path == pred_labels_path:
                            rect_id = canvas.create_rectangle(x_min, y_min, x_min+delta_width, y_min+delta_height, dash=(2,2), fill='', outline=color,width=3)
                            rects.append(rect_id)
                        else:
                            rect_id = canvas.create_rectangle(x_min, y_min, x_min+delta_width, y_min+delta_height, dash=(1,11), fill='', outline="black",width=3)
                            rect_id = canvas.create_rectangle(x_min, y_min, x_min+delta_width, y_min+delta_height, dash=(1,11), fill='', outline=color,width=3, dashoffset=6)

                        if labels_path == pred_labels_path:
                            text = "[PredID: "+str(incremental_id)+"]"
                            text_id = canvas.create_text(x_min, y_min-10, text=text, fill="gray", font=('Helvetica 12 bold'))
                            texts.append(text_id)
                            
                            obj_text_str = "[PredID: "+str(incremental_id)+"] "+class_name+" (C: "+str(class_id)+")"
                            obj_text = tk.Label(newWindow, text=obj_text_str+", "+str(default_class))
                            obj_text.config(font =("Courier", 10))
                            obj_text.place(x=frame_width, y=(incremental_id)*25+55)
                            obj_texts.append(obj_text)
                            
                            c_obj_button = tk.Button(newWindow, text="C", highlightbackground="green", command=lambda s="C", o=obj_text, j=obj: set_as(s,o,j))
                            c_obj_button.place(x=1360, y=(incremental_id)*25+50)
                            c_obj_buttons.append(c_obj_button)

                            w_obj_button = tk.Button(newWindow, text="W", highlightbackground="red", command=lambda s="W", o=obj_text, j=obj: set_as(s,o,j))
                            w_obj_button.place(x=1410, y=(incremental_id)*25+50)
                            w_obj_buttons.append(w_obj_button)

                            m_obj_button = tk.Button(newWindow, text="FP", highlightbackground="blue", command=lambda s="FP", o=obj_text, j=obj: set_as(s,o,j))
                            m_obj_button.place(x=1460, y=(incremental_id)*25+50)
                            m_obj_buttons.append(m_obj_button)

                            incremental_id += 1
        else:
            print("Labels file "+labels_path+" does not exist")
    
def save():
    global image_width, image_height, image_path
    missing_count = 0
    for o in objects_list:
        if o.status == "?":
            missing_count += 1
    if missing_count == 0:
        folder_base_name = os.path.basename(folder_path)
        if not os.path.exists(os.path.join(folder_base_name,"analyzed_labels")):
            os.mkdir(os.path.join(folder_base_name,"analyzed_labels"))
        file_name = folder_base_name+"_"+image_path[:-4]+".txt"
        output_string = ""
        for obj in objects_list:
            x_min = min(obj.top_x,obj.bot_x)
            y_min = min(obj.top_y, obj.bot_y)
            x_max = max(obj.top_x,obj.bot_x)
            y_max = max(obj.top_y, obj.bot_y)
            delta_x = abs(x_max-x_min)
            delta_y = abs(y_max-y_min)
            status = obj.status
            curr_line = f"{obj.class_id} {(x_min+delta_x/2)/image_width} {(y_min+delta_y/2)/image_height} {delta_x/image_width} {delta_y/image_height} {status}"
            output_string += curr_line + "\n"
        
        with open(os.path.join(folder_base_name,"analyzed_labels",file_name), 'w') as output_file:
            output_file.write(output_string)
            output_file.close()

        messagebox.showinfo("Save complete", "The image has been analyzed")
    else:
        messagebox.showerror("Error", "There are some unanalyzed objects left")


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


def results_analyzer():
    #global window
    global counter
    window = tk.Tk()
    window.title("Results Analyzer")
    window.geometry('400x50')
    window.geometry("+%d+%d" %(0,0))
    counter = Counter(window, 0, 1000)

    #---------------------------MAIN---------------------------#
    #C = Canvas(window, bg="blue", height=250, width=300)
    button_via = tk.Button(master = window, text = 'Select session folder', width = 15, command=lambda:browse_folder())
    button_via.pack()
    l = tk.Label(window, text = "")
    l.pack()

    window.mainloop()
    ########################

#images_labeler()