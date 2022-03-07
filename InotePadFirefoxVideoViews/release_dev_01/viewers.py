from tkinter import *
import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import time, datetime
import requests
import random

window = Tk()
window.geometry('400x300')
window.title('Phần mềm')
window.resizable(0, 0)

listData = []
def addTreeView(data):
    count =0
    for record in data:
        my_tree.insert(parent='',index='end',iid=count,text="Parent",values=(count+1,record['keyword'],record['url']))
        count +=1
def delTreeview():
    for i in my_tree.get_children():
        my_tree.delete(i)

def applyData():
    fn_watch = filter_watch.get()
    fn_date = filter_date.get()
    url = "https://www.inotepad.cloud/queryVideo?watch="+fn_watch+"&filter="+fn_date+"&auth=0"
    print(">>>> url ",url)
    resData = requests.get(url).json()
    listData.clear()
    listData.extend(resData['data'])
    delTreeview()
    addTreeView(listData)
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
    for elements in listData:
        driver.get(elements['url'])
        txtPlay = driver.find_element_by_class_name("ytp-play-button").get_attribute('title')
        time.sleep(2)
        if(txtPlay == 'Play (k)'):
            driver.find_element_by_xpath('//*[@id="player"]').click()
        
        duration = driver.find_element_by_class_name("ytp-time-duration").text
        print(">>>>>duration: ",duration)
        try:
            x = time.strptime(duration, '%M:%S')
            timer = datetime.timedelta(minutes=x.tm_min, seconds=x.tm_sec).total_seconds()
            print(">>>>>timer try:",timer)
        except:
            timer = 300
            print(">>>>>timer except:",timer)
        finally:
            if(25>timer): 
                startNum = timer
            else:
                startNum = 25
            t1 = random.randint(startNum, timer)
            t2 = timer - t1
            print("t1:",t1," t2:",t2)
            time.sleep(t1)
            hasLike = len(driver.find_elements_by_class_name("style-default-active"))
            print('>>>>>hasLike',hasLike)
            requests.post('https://www.inotepad.cloud/videoSuccess', json={"_id": elements['_id']})
            print(">>>update views")
            if(hasLike==0):
                driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]').click()
            print(">>>>>Like video:",t1)
            time.sleep(t2)
            print(">>>>>Next Video:",t2+t1)
    driver.close()
    
filter_watch = ttk.Combobox(window, width = 20, state='readonly')
  
# Adding combobox drop down list
filter_watch['values'] = ('see', 
                          'seen',
                          'all')
filter_watch.current(2) 
filter_watch.grid(row=1,column=0)

filter_date = ttk.Combobox(window, width = 20, state='readonly')
  
# Adding combobox drop down list
filter_date['values'] = ('day', 
                         'yesterday',
                         'day7',
                         'week'
                         )

filter_date.current(0) 
filter_date.grid(row=1,column=1)

btnApply = Button(window,text="Apply",command=applyData)
btnApply.grid(row=1,column=2)

#table treeview
my_tree = ttk.Treeview(window)

#define our columms
my_tree['columns'] = ("STT","Keyword","Url")

#Formate our columms
my_tree.column("#0",width=0,stretch=NO)
my_tree.column("STT",anchor=W,width=30)
my_tree.column("Keyword",anchor=CENTER,width=180)
my_tree.column("Url",anchor=W,width=180)

#create headings
my_tree.heading("#0",text="Label",anchor=W)
my_tree.heading("STT",text="STT",anchor=W)
my_tree.heading("Keyword",text="Keyword",anchor=CENTER)
my_tree.heading("Url",text="Url",anchor=W)

varMute = IntVar()
varHeadless = IntVar()
chkHeadless = Checkbutton(window, variable=varHeadless, text="Headless",onvalue=1,offvalue=0)
chkHeadless.select()
chkMute = Checkbutton(window, variable=varMute, text="Mute audio",onvalue=1,offvalue=0)
chkMute.select()
btnWatch = Button(window,text="Watch",command=autoBrowser)

chkHeadless.grid(row=2,column=0)
chkMute.grid(row=2,column=1)
btnWatch.grid(row=1,column=4)
#add Data
my_tree.grid(row=3,columnspan =5,sticky=tk.W)

window.mainloop()