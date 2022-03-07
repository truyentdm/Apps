from tkinter import *
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import time, datetime
import requests
import random
import threading


listData = []
urls = []
page = 0
window = Tk()
window.geometry('450x320')
window.title('INotepad.cloud - Phần mềm Check ASIN')
window.iconbitmap('icon.ico')
# window.resizable(0, 0)

def addTreeView(data):
    count =0
    fn_local = local.get()
    for record in data:
        my_tree.insert(parent='',index='end',iid=count,text="Parent",values=(count+1,record['Asin'],"https://www."+fn_local+"/dp/"+record['Asin']))
        count +=1
def delTreeview():
    for i in my_tree.get_children():
        my_tree.delete(i)

def applyData():        
    fn_namespace = namespace.get()
    resData = requests.get("https://www.inotepad.cloud/amzOpen?namespace="+fn_namespace).json()
    # print(resData)
    listData.clear()
    urls.clear()
    listData.extend(resData)
    urls.extend(resData)
    urls.reverse()
    delTreeview()
    addTreeView(listData)
    if(len(urls)>0):
        btnWatch["state"] = "normal"
        labelLen.set("Total: "+ str(len(listData)))

def views_page(driver,urls,listData,page):
    if len(urls) == 0:
        print("============================================================================================================")
        print('Finished keyword jumping to next one...')
        btnWatch["state"] = "disabled"
        return []

    if (int(len(listData) - len(urls)) == int(page)):
        return []
    # gettin a video link from the list
    itemObj = urls.pop()
    fn_local = local.get()
    fn_namespace = namespace.get()
    asin = itemObj['Asin']
    url = "https://www."+fn_local+"/dp/"+asin
    driver.get(url)
    print("amazon url:" + url)
    driver.implicitly_wait(1)
    labelMessage.set('Đang xem: '+ asin + ' Còn: '+ str(len(urls)))
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, window.scrollY - 500)")
    hasDog = len(driver.find_elements_by_css_selector("#g > a"))
    print(">>>>>>>>>hasDog",hasDog)
    if(hasDog>0):
        print(">>>>>>>>>Url error")
        requests.post('https://www.inotepad.cloud/addLogs', json={"namespace": fn_namespace,"detail": "ASIN: "+asin+" URL: "+url})
    time.sleep(5)
    views_page(driver,urls,listData,page)
    
def autoBrowser():
    configProfile = open("profile.txt", "r")
    txtProfile = configProfile.read()
    print(">>>>>>>file",txtProfile)
    #'C:\\Users\\TruyenTDM\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\r19tqcue.truyenccm'
    profile = webdriver.FirefoxProfile(txtProfile)
    configProfile.close()
    profile.set_preference("dom.webdriver.enabled", False)
    profile.set_preference('useAutomationExtension', False)
    profile.set_preference('intl.accept_languages', 'en-US, en')
    if(varMute.get() == 1):
        profile.set_preference("media.volume_scale", "0.0")
    profile.update_preferences()
    desired = DesiredCapabilities.FIREFOX
    options = Options()
    if(varHeadless.get() == 1):
        options.headless = True
    else:    
        options.headless = False
    driver = webdriver.Firefox(options=options,executable_path="geckodriver.exe",firefox_profile=profile, desired_capabilities=desired)
    print(">>>>>>>>>>>>>>type",type(driver))
    try:
        int(number_page.get())
        if(number_page.get() != 0):
            page = number_page.get()
        else:
            page = len(urls)
    except ValueError:
        print(">>>>>>>not number")
        page = len(urls)
    views_page(driver,urls,listData,page)
    driver.close()

def thread_func(name):
    print('Thread %s: starting',name)
    labelMessage.set('Đang khởi động trình duyệt')
    autoBrowser()
    labelMessage.set('Đã kiểm tra xong')
    print('Thread %s: finished',name)

def proccessWatch():
    try:
        int(number_page.get())
        if(number_page.get() != 0):
            page = number_page.get()
        else:
            page = len(urls)
    except ValueError:
        print(">>>>>>>not number")
        page = len(urls)
    
    labelProcess.set('Process: '+str(page))
    if(varReverse.get() == 1):
        urls.reverse()
    tx = threading.Thread(target=thread_func,args=(1,))
    tx.start()



namespace = ttk.Combobox(window, width = 20, state='readonly')
  
# Adding combobox drop down list
namespace['values'] = ('greattips3s', 
                       'groovybest',
                       'tipslittle')
namespace.current(0) 
namespace.grid(row=1,column=0)

local = ttk.Combobox(window, width = 20, state='readonly')
  
# Adding combobox drop down list
local['values'] = ('amazon.com', 
                   'amazon.ca',
                   'amazon.co.uk',
                  )

local.current(0) 
local.grid(row=1,column=1)

btnApply = Button(window,text="Apply",command= applyData)
btnApply.grid(row=1,column=2)

btnWatch = Button(window,text="Watch",command=proccessWatch)
btnWatch["state"] = "disabled"
btnWatch.grid(row=1,column=4)

#table treeview
my_tree = ttk.Treeview(window)

#define our columms
my_tree['columns'] = ("STT","ASIN","Url")

#Formate our columms
my_tree.column("#0",width=0,stretch=NO)
my_tree.column("STT",anchor=W,width=30)
my_tree.column("ASIN",anchor=CENTER,width=180)
my_tree.column("Url",anchor=W,width=180)

#create headings
my_tree.heading("#0",text="Label",anchor=W)
my_tree.heading("STT",text="STT",anchor=W)
my_tree.heading("ASIN",text="ASIN",anchor=CENTER)
my_tree.heading("Url",text="Url",anchor=W)

varMute = IntVar()
varHeadless = IntVar()
varReverse = IntVar()
chkHeadless = Checkbutton(window, variable=varHeadless, text="Headless",onvalue=1,offvalue=0)
chkHeadless.select()
chkMute = Checkbutton(window, variable=varMute, text="Mute audio",onvalue=1,offvalue=0)
chkMute.select()
chkReverse = Checkbutton(window, variable=varReverse, text="Reverse",onvalue=1,offvalue=0)

chkHeadless.grid(row=2,column=0)
chkMute.grid(row=2,column=1)
chkReverse.grid(row=2,column=2)

Label(window,text="Process").grid(row=3,column=0)
number_page = Entry(window,width=15)
number_page.grid(row=3,column=1)

labelLen = StringVar()
lblmessage = Label(window,textvariable=labelLen).grid(row=5,column=0)
labelMessage = StringVar()
lblmessage = Label(window,textvariable=labelMessage).grid(row=5,column=1)

labelProcess = StringVar()
lblprocess = Label(window,textvariable=labelProcess).grid(row=3,column=2)

my_tree.grid(row=4,columnspan =5,sticky=tk.W)
window.mainloop()