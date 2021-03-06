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
from selenium.webdriver.common.keys import Keys
import time


window = Tk()
window.geometry('430x330')
window.title('INotepad.cloud - Phần mềm Views')
window.iconbitmap('.\icon.ico')
# window.resizable(0, 0)
window.minsize(430, 360)

listData = []
page = 0
urls = []
message = ""
driver = None
def comment_page(driver, comment):
    print(">>>>comment_page: START")
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
def views_page(driver,urls,comment,page):
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
    time.sleep(5)
    video = driver.find_element_by_id('movie_player')
    if(txtPlay == 'Play (k)'):
        print(">>>>>>>>>>> Video Click English")
        video.click()
        # driver.find_element_by_xpath('//*[@id="player"]').click()
    if(txtPlay == 'Phát (k)'):
        print(">>>>>>>>>>> Video Click Vietnam")
        video.click()
        # print(">>>>>>>>>> Press space")
        # video.send_keys(Keys.SPACE)
    duration = driver.find_element_by_class_name("ytp-time-duration").text
    hasDuration = (duration!="")
    print(">>>>>duration: ",duration)
    if(duration != ""):
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
                print(">>>>>progress video:",t1)
                driver.find_element_by_xpath('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[6]/div[1]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div[1]/ytd-toggle-button-renderer[1]').click()
            print(">>>>>Like video:",t1)
            #comment video
            if(varComment.get() == 1):
                print("Page current: ",page)
                if(int(page)!=0):
                    comment_page(driver,comment)
                    page = int(page) - 1
                    print("Page update: ",page)
            time.sleep(t2)
            print(">>>>>Next Video:",t2+t1)
    views_page(driver,urls,random_comment(),page)
def listProfile():
    listProfile = []
    arrProfile = open("profile.txt", "r")
    for x in arrProfile:
        if x != '\n':
            itemProfile = x.split('\\\\')
            listProfile.append(itemProfile[len(itemProfile)-1].strip())
    arrProfile.close()
    return listProfile
    
listProfile()
def getProfile():
    strProfile = ""
    arrProfile = open("profile.txt", "r")
    for x in arrProfile:
        if x != '\n':
            itemProfile = x.split('\\\\')
            if(itemProfile[len(itemProfile)-1].strip() == combobox_profile.get()):
                strProfile = x.strip()
    arrProfile.close()
    print(">>>>>>>getProfile",strProfile)
    return strProfile
    
def autoBrowser():
    # configProfile = open("profile.txt", "r")
    # txtProfile = configProfile.read()
    # configProfile.close()
    txtProfile = getProfile()
    print(">>>>>>>file",txtProfile)
    #'C:\\Users\\TruyenTDM\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\r19tqcue.truyenccm'
    profile = webdriver.FirefoxProfile(txtProfile)
    
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
        if(int(number_page.get()) != 0):
            page = int(number_page.get())
        else:
            page = len(urls)
    except ValueError:
        print(">>>>>>>not number")
        page = len(urls)
    views_page(driver,urls,random_comment(),page)
    driver.close()

def thread_func(name):
    print('Thread %s: starting',name)
    labelMessage.set('Đang khởi động trình duyệt')
    autoBrowser()
    labelMessage.set('Đã xem xong video')
    print('Thread %s: finished',name)

def proccessWatch():
    if(varReverse.get() == 1):
        urls.reverse()
    tx = threading.Thread(target=thread_func,args=(1,))
    tx.start()
    
filter_watch = ttk.Combobox(window, width = 20, state='readonly')
  
# Adding combobox drop down list
filter_watch['values'] = ('see', 
                          'seen',
                          'all')
filter_watch.current(2) 

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
btnApply = Button(window,text="Apply",command=applyData)

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
varReverse = IntVar()
varComment = IntVar()
chkHeadless = Checkbutton(window, variable=varHeadless, text="Headless",onvalue=1,offvalue=0)
chkHeadless.select()
chkMute = Checkbutton(window, variable=varMute, text="Mute audio",onvalue=1,offvalue=0)
chkMute.select()
chkReverse = Checkbutton(window, variable=varReverse, text="Reverse",onvalue=1,offvalue=0)
chkComment = Checkbutton(window, variable=varComment, text="Comment",onvalue=1,offvalue=0)
chkComment.select()
btnWatch = Button(window,text="Watch",command=proccessWatch)
btnWatch["state"] = "disabled"


#add Data
labelMessage = StringVar()
num = StringVar(window, value='6')
number_page = Entry(window,width=15,textvariable=num)

#profile

profiles = listProfile()

combobox_profile = ttk.Combobox(window, width = 20, state='readonly')
  
# Adding combobox drop down list
combobox_profile['values'] = profiles
combobox_profile.current(0) 

filter_watch.grid(row=1,column=0)
filter_date.grid(row=1,column=1)
btnApply.grid(row=1,column=2)
btnWatch.grid(row=1,column=3)

chkHeadless.grid(row=2,column=0)
chkMute.grid(row=2,column=1)
chkReverse.grid(row=2,column=2)


Label(window,text="Comments").grid(row=3,column=0)
chkComment.grid(row=3,column=2)
number_page.grid(row=3,column=1)

Label(window,text="Profiles").grid(row=4,column=0)
combobox_profile.grid(row=4,column=1)

my_tree.grid(row=5,columnspan =5,sticky=tk.W)

lblmessage = Label(window,textvariable=labelMessage).grid(row=6,columnspan=5)

def on_closing():
    try:
        driver.quit()
    finally:
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()