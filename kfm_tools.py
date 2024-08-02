
import tkinter as tk
import os
from images_labeler import images_labeler
from camera_viewer import camera_viewer
from results_analyzer import results_analyzer

root = tk.Tk()
root.title("KFM Tools")

# specify size of window.
root.geometry("450x150")
root.geometry("+%d+%d" %(0,0))

b0 = tk.Button(root, text = "Open Images Labeler", command = lambda: images_labeler())
b1 = tk.Button(root, text = "Open Camera Viewer", command = lambda: camera_viewer())
b2 = tk.Button(root, text = "Open Results Analyzer", command = lambda: results_analyzer())
l = tk.Label(root, text="Built by Salvatore Capuozzo, DIETI, University of Naples Federico II - Version 1.0.0")
l.config(font =("Courier", 6))

b0.pack()
b1.pack()
b2.pack()
l.place(x=5, y=132)

tk.mainloop()