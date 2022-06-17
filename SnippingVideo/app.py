from __future__ import unicode_literals
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import scrolledtext
import os
import threading
import datetime
import subprocess

window = Tk()
window.geometry('500x250')
window.title('INotepad.cloud - Phần mềm Spinning Video')
window.iconbitmap('.\icon.ico')
# window.resizable(0, 0)
window.minsize(500, 250)

folderFirstIn = ""
folderFirstOut = ""
folderEndIn = ""
folderEndOut = ""

timeFirst = StringVar(window, value='00:00:10')
timeEnd = StringVar(window, value='15')

def fnFolderFirstIn():
    global folderFirstIn
    folderFirstIn = filedialog.askdirectory()
    setMessageText('FIRST: Set Folder IN: '+folderFirstIn)
def fnFolderFirstOut():
    global folderFirstOut
    folderFirstOut = filedialog.askdirectory()
    setMessageText('FIRST: Set Folder OUT: '+folderFirstOut)
    
def fnFolderEndIn():
    global folderEndIn
    folderEndIn = filedialog.askdirectory()
    setMessageText('END: Set Folder IN: '+folderEndIn)
def fnFolderEndOut():
    global folderEndOut
    folderEndOut = filedialog.askdirectory()
    setMessageText('END: Set Folder OUT: '+folderEndOut)
def setMessageText(newStr):
    my_message.configure(state='normal')
    my_message.insert(1.0,"\n")
    my_message.insert(1.0," "+newStr)
    my_message.insert(1.0,datetime.datetime.now())
    my_message.configure(state=DISABLED)

def fnConfigEnd(folderOut,strTime):
    txtConfigEnd = "@echo off"+"\n"
    txtConfigEnd += "set /a time="+strTime+"\n"
    txtConfigEnd += "for /f \"tokens=*\" %%a in ('bin\\ffprobe -show_format -i %1 ^| find \"duration\"') do set _duration=%%a"+"\n"
    txtConfigEnd += "set _duration=%_duration:~9%"+"\n"
    txtConfigEnd += "for /f \"delims=. tokens=1*\" %%b in ('echo %_duration%') do set /a \"_durS=%%b\""+"\n"
    txtConfigEnd += "for /f \"delims=. tokens=2*\" %%c in ('echo %_duration%') do set \"_durMS=%%c\""+"\n"
    txtConfigEnd += "rem following line is seconds to cut"+"\n"
    txtConfigEnd += "set /a \"_durS-=%time%\""+"\n"
    txtConfigEnd += "set \"_newduration=%_durS%.%_durMS%\""+"\n"
    txtConfigEnd += "set \"_output=%~n1\""+"\n"
    txtConfigEnd += "md output"+"\n"
    txtConfigEnd += "bin\\ffmpeg -ss 0 -i %1 -t %_newduration% -c copy \""+folderOut+"\\%_output%.mp4\""
    return txtConfigEnd
    
def fnCutEnd(folderIn):
    txtCutEnd = "@echo off"+"\n"
    txtCutEnd += "for %%i in (\""+folderIn+"\\*.mp4\") do ("+"\n"
    txtCutEnd += "call config_end.bat \"%%i\")"
    return txtCutEnd

def fnCutFirst(folderIn,folderOut,strTime):
    txtCutFirst = "for %%a in (\""+folderIn+"\\*.mp4\") do bin\\ffmpeg -ss "+strTime+" -i  \"%%a\" -codec copy \""+folderOut+"\\%%~na.mp4\""
    return txtCutFirst

# Proccess
def fnApplyFirst():
    print(">>>>FIRST: START")
    isTrueIn = False
    isTrueOut = False
    if folderFirstIn=="":
        isTrueIn = False
        setMessageText("ERROR Folder IN is Null")
    else:
        isTrueIn = True
    if folderFirstOut=="":
        isTrueOut = False
        setMessageText("ERROR Folder OUT is Null")
    else:
        isTrueOut = True
    
    if isTrueIn and isTrueOut: 
        setMessageText("Apply success")
        strFolderIn = folderFirstIn.replace("/", "\\");
        strFolderOut = folderFirstOut.replace("/", "\\");
        # cut_first.bat
        wf_cut_first = open("cut_first.bat", "r+")
        wf_cut_first.truncate(0)
        wf_cut_first.write(fnCutFirst(strFolderIn,strFolderOut,time_first.get()));
        wf_cut_first.close()
        
        btnCutFirst["state"] = "normal"
        
def fnProccessFirstCut():
    print(">>>>FIRST: START")
    subprocess.call([r'cut_first.bat'])

def fnApplyEnd():
    print(">>>>END: START")
    isTrueIn = False
    isTrueOut = False
    if folderEndIn=="":
        isTrueIn = False
        setMessageText("ERROR Folder IN is Null")
    else:
        isTrueIn = True
    if folderEndOut=="":
        isTrueOut = False
        setMessageText("ERROR Folder OUT is Null")
    else:
        isTrueOut = True
    
    if isTrueIn and isTrueOut: 
        setMessageText("Apply success")
        strFolderIn = folderEndIn.replace("/", "\\");
        strFolderOut = folderEndOut.replace("/", "\\");
        # config_end.bat
        wf_config_end = open("config_end.bat", "r+")
        wf_config_end.truncate(0)
        wf_config_end.write(fnConfigEnd(strFolderOut,time_end.get()));
        wf_config_end.close()
        # cut_end.bat
        wf_cut_end = open("cut_end.bat", "r+")
        wf_cut_end.truncate(0)
        wf_cut_end.write(fnCutEnd(strFolderIn));
        wf_cut_end.close()
        
        btnCutEnd["state"] = "normal"
    
def fnProccessEndCut():
    print("END>>>>Proccess Cut:")
    subprocess.call([r'cut_end.bat'])
    

    
btnFirstIn = Button(window,text="Folder In",command=fnFolderFirstIn)
btnFirstOut = Button(window,text="Folder Out",command=fnFolderFirstOut)
time_first = Entry(window,width=15,textvariable=timeFirst)
btnApplyFirst = Button(window,text="Apply",command=fnApplyFirst)
btnCutFirst = Button(window,text="Cut First",command=fnProccessFirstCut)
btnCutFirst["state"] = "disabled"

btnEndIn = Button(window,text="Folder In",command=fnFolderEndIn)
btnEndOut = Button(window,text="Folder Out",command=fnFolderEndOut)
time_end = Entry(window,width=15,textvariable=timeEnd)
btnApplyEnd = Button(window,text="Apply",command=fnApplyEnd)
btnCutEnd = Button(window,text="Cut End",command=fnProccessEndCut)
btnCutEnd["state"] = "disabled"

my_message = scrolledtext.ScrolledText(window, width=60, height=10)
my_message.configure(state=DISABLED)

btnFirstIn.grid(row=1,column=0)
btnFirstOut.grid(row=1,column=1)
time_first.grid(row=1,column=2)
btnApplyFirst.grid(row=1,column=3)
btnCutFirst.grid(row=1,column=4)

btnEndIn.grid(row=2,column=0)
btnEndOut.grid(row=2,column=1)
time_end.grid(row=2,column=2)
btnApplyEnd.grid(row=2,column=3)
btnCutEnd.grid(row=2,column=4)

my_message.grid(row=3,columnspan=5)
window.mainloop()