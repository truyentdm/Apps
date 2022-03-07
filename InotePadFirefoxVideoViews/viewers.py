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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


window = Tk()
window.geometry('430x300')
window.title('INotepad.cloud - Phần mềm Views')
window.iconbitmap('G:\Coder\Build Project\Apps\InotePadFirefoxVideoViews\icon.ico')
window.resizable(0, 0)

listData = []
urls = []
message = ""
driver = None
def comment_page(driver, comment):
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
    time.sleep(1)

    # finding comment box and submiting our comment on it
    comment_box = EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#placeholder-area'))
    WebDriverWait(driver, 4).until(comment_box)
    comment_box1 = driver.find_element_by_css_selector('#placeholder-area')
    ActionChains(driver).move_to_element(
        comment_box1).click(comment_box1).perform()
    add_comment_onit = driver.find_element_by_css_selector(
        '#contenteditable-root')
    add_comment_onit.send_keys(comment)
    driver.find_element_by_css_selector('#submit-button').click()
    print("done")

    time.sleep(5)
    driver.execute_script("window.scrollTo(0, window.scrollY - 500)")

# comment section
def random_comment():
    # You can edit these lines if you want to add more comments===================================
    resData = requests.get("https://www.inotepad.cloud/commentArray").json()
    comments = resData['comment']
    r = random.randint(0, len(comments)-1)
    print(">>>>comment:",comments[r])
    return comments[r]
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
    urls.clear()
    listData.extend(resData['data'])
    urls.extend(resData['data'])
    urls.reverse()
    if(len(urls)>0):
        btnWatch["state"] = "normal"
    delTreeview()
    addTreeView(listData)
def views_page(driver,urls,comment):
    if len(urls) == 0:
        print("============================================================================================================")
        print('Finished keyword jumping to next one...')
        btnWatch["state"] = "disabled"
        return []

    # gettin a video link from the list
    itemObj = urls.pop()
    url = itemObj['url']
    driver.get(url)
    print("Video url:" + url)
    driver.implicitly_wait(1)
    labelMessage.set('Đang xem video: '+ itemObj['url'])
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
        requests.post('https://www.inotepad.cloud/videoSuccess', json={"_id": itemObj['_id']})
        print(">>>update views")
        if(hasLike==0):
            driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]').click()
        print(">>>>>Like video:",t1)
        #comment video
        if(varComment.get() == 1):
            comment_page(driver,comment)
        time.sleep(t2)
        print(">>>>>Next Video:",t2+t1)
    views_page(driver,urls,random_comment())
    
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
    views_page(driver,urls,random_comment())
    driver.close()

def thread_func(name):
    print('Thread %s: starting',name)
    labelMessage.set('Đang khởi động trình duyệt')
    autoBrowser()
    labelMessage.set('Đã xem xong video')
    print('Thread %s: finished',name)

def proccessWatch():
    tx = threading.Thread(target=thread_func,args=(1,))
    tx.start()
    
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
                         'week',
                         'month',
                         'day30'
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
varComment = IntVar()
chkHeadless = Checkbutton(window, variable=varHeadless, text="Headless",onvalue=1,offvalue=0)
chkHeadless.select()
chkMute = Checkbutton(window, variable=varMute, text="Mute audio",onvalue=1,offvalue=0)
chkMute.select()
chkComment = Checkbutton(window, variable=varComment, text="Comment",onvalue=1,offvalue=0)
chkComment.select()
btnWatch = Button(window,text="Watch",command=proccessWatch)
btnWatch["state"] = "disabled"

chkHeadless.grid(row=2,column=0)
chkMute.grid(row=2,column=1)
chkComment.grid(row=2,column=2)
btnWatch.grid(row=1,column=4)
#add Data
my_tree.grid(row=3,columnspan =5,sticky=tk.W)
labelMessage = StringVar()
lblmessage = Label(window,textvariable=labelMessage).grid(row=4,columnspan=5)


def on_closing():
    try:
        driver.quit()
    finally:
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()