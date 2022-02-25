from cgitb import text
from glob import glob
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import colorizer

sourcePath = ''
targetPath = ''
destPath = ''

def openFile(pathType: int):
    path = fd.askopenfilename()
    updatePath(pathType, path)

def openDirectory(pathType: int):
    path = fd.askdirectory()
    updatePath(pathType, path)

def updatePath(pathnum, value):
    global sourcePath
    global targetPath
    global destPath

    if pathnum == 0:
        sourcePath = value
    elif pathnum == 1:
        targetPath = value
    else:
        destPath = value

def printPath():
    print(sourcePath)
    print(targetPath)
    print(destPath)

def colorize():
    global sourcePath
    global targetPath
    global destPath
    colorizer.color_transfer(sourcePath, targetPath, destPath)


window = tk.Tk()

window.title('Colorizer v1')

inputLabel = tk.Label(text="Input Image")
inputLabel.pack()

inputButton = ttk.Button(window, text='Select input', command=lambda: openFile(0))
inputButton.pack(fill=tk.X)

targetLabel = tk.Label(text="Target Image")
targetLabel.pack(fill=tk.X)

targetButton = ttk.Button(window, text='Select target', command=lambda:openFile(1))
targetButton.pack(fill=tk.X)


destLabel = tk.Label(text="destination Path")
destLabel.pack()

destButton = ttk.Button(window, text='Select target', command=lambda:openDirectory(2))
destButton.pack(fill=tk.X)

submitButton = ttk.Button(window, text='COLORIZE', command=lambda:colorize())
submitButton.pack(fill=tk.X)

window.mainloop()



