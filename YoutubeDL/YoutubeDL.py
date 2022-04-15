from __future__ import unicode_literals
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import yt_dlp
import os
import threading




window = Tk()
window.geometry('430x320')
window.title('INotepad.cloud - Phần mềm Youtube DL')
window.iconbitmap('G:\Coder\Build Project\Apps\YoutubeDL\Apps\icon.ico')
window.resizable(0, 0)

listData = []
urls = []
message = ""
driver = None
fileIn = ""
folderName = ""
def readFile(rdfile):
    f = open(rdfile, "r")
    for x in f:
        if x != '\n':
            urls.append(x.strip())
    f.close()
def addTreeView(data):
    count =0
    for record in data:
        my_tree.insert(parent='',index='end',iid=count,text="Parent",values=(count+1,record))
        count +=1
    if(count>0):
        btnDownload["state"] = "normal"
def delTreeview():
    for i in my_tree.get_children():
        my_tree.delete(i)
def fileIn():
    fileIn = filedialog.askopenfilename()
    readFile(fileIn)
    addTreeView(urls)
    print(urls)
def folderOut():
    global folderName
    folderName = filedialog.askdirectory()
    labelFileOut.set('Folder: '+folderName)
 
def downLoad_video(urls):
    if len(urls) == 0:
        print("============================================================================================================")
        print('Finished keyword jumping to next one...')
        btnDownload["state"] = "disabled"
        return []
    url = urls.pop()
    labelMessage.set('Download: '+ url)
  
    if(folderName == ""):
        ydl_opts = {
            'ratelimit': 50000000
        }
    else:
        ydl_opts = {
            'outtmpl': os.path.join(folderName, '%(title)s.%(ext)s'),
            'ratelimit': 50000000
        }
        
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
            
    downLoad_video(urls)
    
def thread_func(name):
    print('Thread %s: starting',name)
    labelMessage.set('Đang tiến hành downloads')
    downLoad_video(urls)
    labelMessage.set('Đã downloads xong video')
    print('Thread %s: finished',name)

def proccessDownload():
    tx = threading.Thread(target=thread_func,args=(1,))
    tx.start()
    

    
btnIn = Button(window,text="File In",command=fileIn)
btnIn.grid(row=1,column=0)
btnOut = Button(window,text="Folder Out",command=folderOut)
btnOut.grid(row=1,column=1)

#table treeview
my_tree = ttk.Treeview(window)

#define our columms
my_tree['columns'] = ("STT","Url")

#Formate our columms
my_tree.column("#0",width=0,stretch=NO)
my_tree.column("STT",anchor=W,width=30)
my_tree.column("Url",anchor=W,width=300)

#create headings
my_tree.heading("#0",text="Label",anchor=W)
my_tree.heading("STT",text="STT",anchor=W)
my_tree.heading("Url",text="Url",anchor=W)

labelFileOut = StringVar()
lblFileOut = Label(window,textvariable=labelFileOut).grid(row=3,columnspan=3)

btnDownload = Button(window,text="Downloads",command=proccessDownload)
btnDownload["state"] = "disabled"


btnDownload.grid(row=1,column=2)
#add Data
my_tree.grid(row=4,columnspan =3,sticky=tk.W)
labelMessage = StringVar()
lblmessage = Label(window,textvariable=labelMessage).grid(row=5,columnspan=3)

def on_closing():
    try:
        driver.quit()
    finally:
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()