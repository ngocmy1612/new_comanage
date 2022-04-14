import re, sys, json, unittest, os, pyperclip
import time, random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from random import choice, randrange
from pathlib import Path

from MN_functions import driver, data, Logging, TestCase_LogResult

n = random.randint(1,1000)
m = random.randint(1,10000)

domain_hr = "global3.hanbiro.com/ncomanage"

chrome_path = os.path.dirname(Path(__file__).absolute())+"\\chromedriver.exe"
json_file = os.path.dirname(Path(__file__).absolute())+"\\MN_groupware_auto.json"
driver.maximize_window()

def access_hr():
    driver.get("http://" + domain_hr + "/login")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "gw_id")))
    userID = driver.find_element_by_name("gw_id")
    userID.send_keys("ngocmy")
    print("- Input user ID")
    password = driver.find_element_by_name("gw_pass")
    password.send_keys("123456a!")
    print("- Input user password")
    driver.find_element_by_xpath(data["TIMECARD"]["sign_in"]).click()
    print("- Click button Sign in")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["TIMECARD"]["notify"][0])))
    print("=> Log in successfully")
    time.sleep(2)

def co_manage():
    Logging("=================================================NEW CO-MANAGE =======================================================")
    gw_project = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'/ncomanage/groupware')]")))
    time.sleep(3)
    gw_project.click()

    try:
        admin_account = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[@id='app']//nav/a[contains(@href,'/ncomanage/groupware/co-manage/admin')]")))
        admin_account = True
        Logging("ADMIN ACCOUNT")
    except:
        admin_account = False
        Logging("USER ACCOUNT")

    return admin_account

def kanban(admin_account):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='app']//div[@class='content-dashboard']")))
    project_list = driver.find_element_by_xpath("//a[contains(@href,'/ncomanage/groupware/co-manage/project-list/normal')]")
    project_list.click()
    time.sleep(3)

    try:
        project = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='wrap-content-project']//div[text()='Kanban']/../preceding-sibling::div//div/a"))).click()
        Logging("- Open Kanban project")
        project = True
    except:
        Logging("- No project")
        driver.find_element_by_xpath("//a//span[contains(.,'All Projects')]").click()
        if admin_account == True:
            create_project()
            project = True
        else:
            project = False
    
    return project

def create_project():
    driver.find_element_by_xpath("//div[@class='mail-sidebar-body']//button[contains(.,'Create Project')]").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='alert-dialog-title']")))
    pro_name = "Project: " + str(n)
    project_name = driver.find_element_by_xpath("//input[@placeholder='Project Name']")
    project_name.send_keys(pro_name)

    driver.find_element_by_xpath("//button[contains(.,'Confirm')]").click()

    infor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='mail-sidebar-body']//nav/a/span[contains(.,'"+ str(pro_name) +"')]")))
    if infor.is_displayed():
        Logging(">> Create new project Successfully")
        infor.click()
        time.sleep(3)
        project_content()
        driver.find_element_by_xpath("//ul[@id='myTab5']/li/a[contains(.,'Boards')]").click()
    else:
        Logging(">> Create new project Fail")
        Logging(">>>> Cannot continue excution")
        pass

def project_content():
    driver.find_element_by_xpath("//div[@id='wrap-content-project']//ul[@id='myTab5']/li[contains(.,'Setting')]/a").click()
    print("- Setting")
    
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='item-field']/div")))
    time.sleep(2)
    driver.find_element_by_xpath("//ul[@id='myTab5']/li/a[contains(.,'View Roster')]").click()
    print("- View Roster")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class,'title-field') and contains(.,'Leader')]/button"))).click()
    time.sleep(3)

    search_leader = driver.find_element_by_xpath("//form[@id='org-form-search']//input")
    search_leader.send_keys("auto")
    search_leader.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element_by_xpath("//ul[@class='line']/li[1]//a//input").click()
    driver.find_element_by_xpath("//ul[@class='line']/li[2]//a//input").click()
    driver.find_element_by_xpath("//ul[@class='line']/li[3]//a//input").click()
    driver.find_element_by_xpath("//div[@class='card-body']//button[text()='Add']").click()
    driver.find_element_by_xpath("//button[text()='Save']").click()
    time.sleep(3)

def run_project(admin_account):
    print("########### KANBAN PROJECT ###########")
    project = kanban(admin_account)
    if project == True:
  
        insert_work()
        work_list()

        #drag_drop()
        #write_work()
    
    else:
        pass
    
    print("########### SCRUM PROJECT ###########")
    project1 = scrum_project(admin_account)
    if project1 == True:
        new_work()

    
    else:
        pass
    

def comanage():
    admin_account = co_manage()
    if admin_account == True:
        run_project(admin_account)
    else:
        run_project(admin_account)

    time.sleep(3)

############################################ Kanban project

def insert_work():
    #Insert work
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='wrap-content-project']//div[@class='co-manage-board']//div//div[@class='column-field']")))
    search = driver.find_element_by_xpath("//*[@id='wrap-content-project']//div[@class='content-search']//input")
    search_value = search.get_attribute("value")
    value = int(len(search_value))
    #Logging(value)

    if value > 0:
        search.clear()
        search.send_keys(Keys.ENTER)
        Logging("- Clear search")
    else:
        Logging(" ")

    time.sleep(3)
    insert_work_name = data["COMANAGE"]["insert_ticket"] + str(m)
    insert_work = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='wrap-content-project']//div[@class='co-manage-board']//textarea")))
    insert_work.send_keys(insert_work_name)
    Logging("- Input work name")
    insert_work.send_keys(Keys.RETURN)
    Logging("- Insert Work")

    #Search work
    time.sleep(3)
    search = driver.find_element_by_xpath("//*[@id='wrap-content-project']//div[@class='content-search']//input")
    search.send_keys(insert_work_name)
    search.send_keys(Keys.ENTER)
    Logging("- Search work")
    time.sleep(5)
    driver.find_element_by_xpath("//*[@id='wrap-content-project']//div[@class='column-field'][1]//div[contains(@class,'MuiCardContent-root')]/div[1]").click()
    Logging("- View ticket")
    time.sleep(3)
    detail = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='co-manage-work-detail']//div[@class='work-input-container']")))
    if detail.is_displayed():
        Logging("=> View work successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["view_work"]["pass"])

        title_work = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='co-manage-work-detail']//div[@class='work-input-container']/textarea")))
        if insert_work_name == title_work.text:
            Logging("=> Insert work successfully")
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["insert_work"]["pass"])
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["search_work"]["pass"])
        else:
            Logging("=> Insert work fail")
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["insert_work"]["fail"])
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["search_work"]["fail"])
    else:
        Logging("=> View work fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["view_work"]["fail"])

    update_work()
    driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//button[2]").click()
    Logging("- Close detail work")
    time.sleep(2)
    search = driver.find_element_by_xpath("//*[@id='wrap-content-project']//div[@class='content-search']//input")
    search.clear()
    search.send_keys(Keys.ENTER)
    Logging("- Clear search work")

def update_work():
    try:
        update_status()   
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass
    try:
        update_assigned_to()
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass
    try:
        update_work_type()
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass
    try:
        update_priority()
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass

    try:
        update_CC()
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass

    try:
        update_date()
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass

    try:
        update_description()
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass
    
    try:
        write_comment() 
        Logging("")
    except:
        Logging(">>>> Cannot continue excution")
        pass

def update_status():
    #Select status
    start_status = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Status')]/following-sibling::div/button[@id='dropdownMenuButton']")
    #Logging(start_status.text)
    start_status.click()
    Logging("- Update status")
    status_list = int(len(driver.find_elements_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Status')]/following-sibling::div/div/a")))
    
    
    list_status = []
    i=0
    for i in range(status_list):
        i += 1
        status = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Status')]/following-sibling::div/div/a" + "[" + str(i) + "]/span")
        if status.text != start_status.text:
            list_status.append(status.text)
        else:
            continue

    Logging("- Total of status: " + str(len(list_status)))
    #Logging(list_status)

    x = random.choice(list_status)
    time.sleep(1)
    status_label = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Status')]/following-sibling::div/div/a[contains(., '" + str(x) + "')]")
    status_label.click()
    Logging("- Select status")

    time.sleep(3)
    start_status_update = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Status')]/following-sibling::div/button[@id='dropdownMenuButton']")
    if start_status_update.text == str(x):
        Logging("=> Update status successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_status"]["pass"])
    else:
        Logging("=> Update status fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_status"]["fail"])

def update_work_type():
    #Select work type
    start_work_type = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Work type')]/following-sibling::div//button[@id='dropdownMenuButton']")
    #Logging(start_work_type.text)
    start_work_type.click()
    Logging("- Update Work type")
    work_type_list = int(len(driver.find_elements_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Work type')]/following-sibling::div//div/a")))
    
    list_work_type = []
    i=0
    for i in range(work_type_list):
        i += 1
        work_type = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Work type')]/following-sibling::div//div/a" + "[" + str(i) + "]//span")
        if work_type.text != start_work_type.text:
            list_work_type.append(work_type.text)
        else:
            continue

    Logging("- Total of work type: " +  str(len(list_work_type)))
    #Logging(list_work_type)

    x = random.choice(list_work_type)
    time.sleep(1)
    work_type_label = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Work type')]/following-sibling::div//div/a//span[contains(., '" + str(x) + "')]")
    work_type_label.click()
    Logging("- Select work type")

    time.sleep(3)
    start_work_type_update = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='co-manage-work-detail']//div/span[contains(.,'Work type')]/following-sibling::div//button[@id='dropdownMenuButton']")))
    if start_work_type_update.text == str(x):
        Logging("=> Update work type successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_work_type"]["pass"])
    else:
        Logging("=> Update work type fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_work_type"]["fail"])

def update_assigned_to():
    #Select assigned to
    start_assign = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Assigned to')]/following-sibling::div/button/span")
    #Logging(start_assign.text)
    start_assign.click()
    Logging("- Assigned to")
    time.sleep(3)
    assign_list = int(len(driver.find_elements_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Assigned to')]/following-sibling::div/div//div[2]/div/a")))

    list_assign = []
    i=0
    for i in range(assign_list):
        i += 1
        assign = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Assigned to')]/following-sibling::div/div//div[2]/div/a" + "[" + str(i) + "]/span")
        if assign.text != start_assign.text:
            list_assign.append(assign.text)
        else:
            continue

    Logging("- Total of assign: " + str(len(list_assign)))
    #Logging(list_assign)

    x = random.choice(list_assign)
    time.sleep(1)
    assign_label = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Assigned to')]/following-sibling::div/div//div[2]/div/a/span[contains(.,'" + str(x) + "')]")
    assign_label.click()
    Logging("- Select user")
    
    time.sleep(3)
    start_assign_update = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='co-manage-work-detail']//div/span[contains(.,'Assigned to')]/following-sibling::div/button/span")))
    if start_assign_update.text == str(x):
        Logging("=> Update assigned to successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_assigned_to"]["pass"])
    else:
        Logging("=> Update assigned to fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_assigned_to"]["fail"])

def update_priority():
    #Select priority
    start_priority = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Priority')]/following-sibling::div//button[@id='dropdownMenuButton']")
    #Logging(start_priority.text)
    start_priority.click()
    Logging("- Update priority")
    time.sleep(2)
    priority_list = int(len(driver.find_elements_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Priority')]/following-sibling::div/div/a")))
    
    list_priority = []
    i=0
    for i in range(priority_list):
        i += 1
        priority = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Priority')]/following-sibling::div/div/a" + "[" + str(i) + "]/span")
        if priority.text != start_priority.text:
            list_priority.append(priority.text)
        else:
            continue

    Logging("- Total of priority: "+ str(len(list_priority)))
    #Logging(list_priority)

    x = random.choice(list_priority)
    time.sleep(2)
    priority_label = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Priority')]/following-sibling::div/div/a/span[text()='" + str(x) + "']")
    time.sleep(2)
    priority_label.click()
    Logging("- Select priority")
    
    time.sleep(3)
    start_priority_update = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='co-manage-work-detail']//div/span[contains(.,'Priority')]/following-sibling::div//button[@id='dropdownMenuButton']")))
    if start_priority_update.text == str(x):
        Logging("=> Update priority successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_priority"]["pass"])
    else:
        Logging("=> Update priority fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_priority"]["fail"])

def update_CC():
    driver.find_element_by_xpath("//*[@id='cc-dropdown']//div[contains(@class,'work-cc-add-button')]").click()
    time.sleep(2)
    CC_list = int(len(driver.find_elements_by_xpath("//*[@id='cc-dropdown']//form/div[contains(@class,'scroll-container')]/div")))
    x = randrange(1, CC_list +1)
    select_cc = driver.find_element_by_xpath("//*[@id='cc-dropdown']//form/div[contains(@class,'scroll-container')]/div["+ str(x) +"]/div/input/following-sibling::label")
    select_cc.click()
    print("- Select CC")
    driver.find_element_by_xpath("//*[@id='cc-dropdown']//div[contains(@class,'work-cc-add-button')]").click()
    print("- Close CC box")
    time.sleep(2)

def update_date():
    driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Start Date')]//following-sibling::div//input").click()
    Logging("- Start date")
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='react-datepicker__week']//div[contains(., '16')]"))).click()
    Logging("- Select start date")
    driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'End Date')]//following-sibling::div//input").click()
    Logging("- End date")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='react-datepicker__week']//div[contains(., '19')]"))).click()
    Logging("- Select end date")

def update_description():
    try:
        content = driver.find_element_by_xpath("//*[@id='description']//span[text()='Click to add description']")
        content.click()
        print("- Click to add description")
        time.sleep(2)
        insert_work = driver.find_element_by_xpath("//*[@id='description']//div[@class='han-react-quill']//div[contains(@class,'fr-view')]/div")
        insert_work.send_keys(data["COMANAGE"]["input_description"])
        Logging("- Input Description")
        driver.find_element_by_xpath("//*[@id='description']//div[@class='group-button-field']/button[contains(.,'Save')]").click()
        Logging("- Save Description")
    except:
        hover_description = driver.find_element_by_xpath("//*[@id='description']/div[@class='work-description']")
        hover_1 = ActionChains(driver).move_to_element(hover_description)
        hover_1.perform()
        edit_button = driver.find_element_by_xpath("//*[@id='description']//div[@class='co-manage-han-copy'][1]//i[@class='copy-content']")
        edit_button.click()
        time.sleep(2)
        insert_work = driver.find_element_by_xpath("//*[@id='description']//div[@class='han-react-quill']//div[contains(@class,'fr-view')]/div")
        insert_work.clear()
        insert_work.send_keys(data["COMANAGE"]["input_description"])
        Logging("- Input Description")
        driver.find_element_by_xpath("//*[@id='description']//div[@class='group-button-field']/button[contains(.,'Save')]").click()
        Logging("- Save Description")

def write_comment():
    #Comment
    driver.find_element_by_xpath("//*[@class='co-manage-work-comment ']//div[contains(@class,'work-description')]/div/div").click()
    time.sleep(2)
    insert_comment = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='co-manage-work-comment ']//div[contains(@class,'han-react-quill')]//div[contains(@class,'fr-wrapper')]/div/div")))
    insert_comment.click()
    insert_comment.send_keys(data["COMANAGE"]["input_comment"])
    Logging("- Input comment")
    save_comment = driver.find_element_by_xpath("//*[@class='co-manage-work-comment ']//div[contains(@class,'group-button-field')]//button/span[text()='Save']")
    save_comment.click()
    Logging("- Save comment")
    try:
        comment_work = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='img']//div[contains(@class,'description-field')]/div")))
        if (data["COMANAGE"]["input_comment"]) == comment_work.text:
            Logging("=> Write comment Successfully")
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["write_comment"]["pass"])
        else:
            Logging("=> Wrong content comment")
    except:
        Logging("=> Write comment Fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["write_comment"]["fail"])

    driver.find_element_by_xpath("//div[@class='co-manage-work-comment ']//div[@class='han-svg']/button[2]").click()
    print("- Click edit comment")
    time.sleep(2)
    insert_comment1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='co-manage-work-comment ']//div[contains(@class,'han-react-quill')]//div[contains(@class,'fr-wrapper')]/div/div")))
    insert_comment1.clear()
    time.sleep(2)
    insert_comment1.send_keys("This is comment after edit")
    save_comment1 = driver.find_element_by_xpath("//*[@class='co-manage-work-comment ']//div[contains(@class,'group-button-field')]//button/span[text()='Save']")
    save_comment1.click()
    print("- Save comment edit")
    
def work_list():
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='wrap-content-project']//div[@class='co-manage-board']//div//div[@class='column-field']")))

    driver.find_element_by_xpath("//*[@id='myTab5']/li/a[text()='Work List']").click()
    Logging("- Work List")
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "//*[@class='work-list']//div[contains(@class,'content-table')]/div")))
    try:
        x = filters_worktype()
    except:
        pass

def filters_worktype():
    driver.find_element_by_xpath("//*[@class='work-list']//div[contains(@class,'dropdown')]/button[contains(.,'Work type')]").click()
    Logging("- Search Work type")
    filter_work_list = int(len(driver.find_elements_by_xpath("//*[@class='work-list']//div[contains(@class,'dropdown')]/button[contains(.,'Work type')]/following-sibling::div/form/a")))

    list_filter_work = []
    i=0

    for i in range(filter_work_list):
        i += 1
        filter_work = driver.find_element_by_xpath("//*[@class='work-list']//div[contains(@class,'dropdown')]/button[contains(.,'Work type')]/following-sibling::div/form/a" + "[" + str(i) + "]//span") 
        list_filter_work.append(filter_work.text)
    
    Logging("- Total filter Work type: "+ str(len(list_filter_work)))
    #Logging(list_filter_work)

    x = random.choice(list_filter_work)
    filter_work_select = driver.find_element_by_xpath("//*[@class='work-list']//div[contains(@class,'dropdown')]/button[contains(.,'Work type')]/following-sibling::div/form/a//span[contains(., '" + str(x) + "')]")
    filter_work_select.click()
    Logging("- Filter Work type")
    time.sleep(3)

    try:
        work_list = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "//*[@class='work-list']//div[contains(@class,'content-table')]/div//div[@class='subject']")))
        if work_list.is_displayed():
            driver.find_element_by_xpath("//*[@class='work-list']//div[contains(@class,'dropdown')]/button[contains(.,'Work type')]").click()
            time.sleep(2)
            work_list.click()
            try:
                sub_name = check_filter(x)
            except:
                Logging("- Check filter Fail")
                pass
    except:
        Logging("- No data found!")
        driver.find_element_by_xpath("//*[@class='work-list']//div[contains(@class,'dropdown')]/button[contains(.,'Work type')]/following-sibling::div/form/div/button[contains(.,'Clear')]").click()
        Logging("- Clear filter")

    return x

def check_filter(x):
    detail_work = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='wrap-content-project']//div[@class='co-manage-work-detail']/div//textarea")))
    time.sleep(2)
    if detail_work.is_displayed():
        Logging("=> View work list successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["view_work_list"]["pass"])
        time.sleep(2)
        type_text = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//div/span[contains(.,'Work type')]/following-sibling::div//button[@id='dropdownMenuButton']//span")
        if type_text.text == str(x) == "Sub Task":
            Logging("=> Correct Work type")
        elif type_text.text == str(x):
            Logging("=> Correct Work type")
            driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//button[contains(.,'Create Sub Work')]").click()
            Logging("- Create Sub work")
            sub_name = "Auto Test: Sub work " + str(m)
            input_sub = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//button[contains(.,'Create Sub Work')]/../../../following-sibling::div//input[@type='text']")
            #input_sub.click()
            input_sub.send_keys(sub_name)
            Logging("- Input Sub work name")
            driver.find_element_by_xpath("//*[@class='work-input-container']//button[1]").click()
            Logging("- Save Sub work")
            time.sleep(3)
            sub_work_title = driver.find_element_by_xpath("//*[@class='co-manage-work-detail']//h6[contains(.,'Subtasks')]/following-sibling::ul/li//span[contains(.,'" + sub_name + "')]")
            if sub_work_title.is_displayed:
                sub_work_title.click()
                Logging("=> Create sub-work successfully")
                TestCase_LogResult(**data["testcase_result"]["co_manage"]["sub-work"]["pass"])
                #copied_to_clipboard(sub_name)
            else:
                Logging("=> Create sub-work fail")
                TestCase_LogResult(**data["testcase_result"]["co_manage"]["sub-work"]["fail"])
        else:
            Logging("=> Wrong Work type")

        driver.find_element_by_xpath("//*[@class='work-list']//div[contains(@class,'dropdown')]/button[contains(.,'Work type')]").click()
        driver.find_element_by_xpath("//*[@class='work-list']//div[contains(@class,'dropdown')]/button[contains(.,'Work type')]/following-sibling::div/form/div/button[contains(.,'Clear')]").click()
    else:
        Logging("=> View work list fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["view_work_list"]["fail"])

    return sub_name

############################################ Scrum project

def create_scrum_project():
    driver.find_element_by_xpath("//div[@class='mail-sidebar-body']//button[contains(.,'Create Project')]").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='alert-dialog-title']")))
    scrum_name = "Scrum Project: " + str(m)
    project_scrum = driver.find_element_by_xpath("//input[@placeholder='Project Name']")
    project_scrum.send_keys(scrum_name)
    driver.find_element_by_xpath("//div[@class='co-manage-new-folder']//span[text()='More']").click()
    driver.find_element_by_xpath("//div[@class='template']//h6[contains(.,'Advanced Project')]").click()
    print("- Scrum Project")
    driver.find_element_by_xpath("//button[contains(.,'Confirm')]").click()

    infor_scrum = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='mail-sidebar-body']//nav/a/span[contains(.,'"+ str(scrum_name) +"')]")))
    if infor_scrum.is_displayed():
        Logging(">> Create new Scrum project Successfully")
        infor_scrum.click()
        time.sleep(3)
        project_content()
        driver.find_element_by_xpath("//ul[@id='myTab5']/li/a[contains(.,'Backlog')]").click()
    else:
        Logging(">> Create new Scrum project Fail")
        Logging(">>>> Cannot continue excution")
        pass
    
def scrum_project(admin_account):
    driver.find_element_by_xpath("//a//span[contains(.,'All Projects')]").click()
    time.sleep(3)

    try:
        project1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='wrap-content-project']//div[text()='Scrum']/../preceding-sibling::div//div/a"))).click()
        Logging("- Open Scrum project")
        project1 = True
    except:
        Logging("- No project")
        driver.find_element_by_xpath("//a//span[contains(.,'All Projects')]").click()
        if admin_account == True:
            create_scrum_project()
            project1 = True
        else:
            project1 = False
    
    return project1

def new_work():
    driver.find_element_by_xpath("//ul[@id='myTab5']/li/a[contains(.,'Backlog')]").click()
    
    count_sprint = int(len(driver.find_elements_by_xpath("//div[@class='sprint-right']//div[@class='sprint-container']/div")))
    if count_sprint > 2:
        print("Đã có sẵn sprint")
        try:
            start_sprint = driver.find_element_by_xpath("//div[@class='sprint-right']//div[@class='sprint-container']/div[2]//div[@class='sprint-header-action']//button[text()='Start Sprint']")
            driver.find_element_by_xpath("//div[@class='sprint-header-action']//button[contains(.,'Start Sprint')]").click()
            print("- Start Sprint")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='dialog-footer']/button[contains(.,'OK')]"))).click()
            time.sleep(3)

            name_work = "Automation Test of Scrum: " + str(n)
            driver.find_element_by_xpath("//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div[@class='sprint-add-more']/button").click()
            add_work = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sprint-add-more']//input")))
            add_work.send_keys(name_work)
            add_work.send_keys(Keys.ENTER)

            add_work_done = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
            print("=> Add new work successfully")
            time.sleep(3)

            source1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
            target1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-works-empty')]/div/span")))
            action = ActionChains(driver)
            action.click_and_hold(source1).move_to_element(target1).move_by_offset(0, -100).release().perform()
            time.sleep(2)
            source2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'"+ str(sprint_name) +"')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
            source2.click()
            print("- View work at Sprint")
            time.sleep(2)
            
            update_work()
        except:
            name_work = "Automation Test of Scrum: " + str(n)
            driver.find_element_by_xpath("//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div[@class='sprint-add-more']/button").click()
            add_work = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sprint-add-more']//input")))
            add_work.send_keys(name_work)
            add_work.send_keys(Keys.ENTER)

            add_work_done = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
            print("=> Add new work successfully")
            time.sleep(3)

            add_work_done = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
            print("=> Add new work successfully")
            time.sleep(3)

            source1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
            target1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-works-empty')]/div/span")))
            action = ActionChains(driver)
            action.click_and_hold(source1).move_to_element(target1).move_by_offset(0, -100).release().perform()
            time.sleep(2)
            source2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'"+ str(sprint_name) +"')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
            source2.click()
            print("- View work at Sprint")
            time.sleep(2)
            
            update_work()

    elif count_sprint == 2:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sprint-add-more']//button[contains(.,'Create sprint')]"))).click()
        print("- Create sprint")
        sprint_name = "Sprint: " + str(n)
        input_sprint_name = driver.find_element_by_xpath("//div[@class='sprint-add-more']//input")
        input_sprint_name.send_keys(sprint_name)
        driver.find_element_by_xpath("//div[@class='sprint-add-more']//button[contains(.,'Save')]").click()
        print("- Save Sprint")
        driver.find_element_by_xpath("//div[@class='sprint-header-action']//button[contains(.,'Start Sprint')]").click()
        print("- Start Sprint")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='dialog-footer']/button[contains(.,'OK')]"))).click()
        time.sleep(3)

        name_work = "Automation Test of Scrum: " + str(n)
        driver.find_element_by_xpath("//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div[@class='sprint-add-more']/button").click()
        add_work = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sprint-add-more']//input")))
        add_work.send_keys(name_work)
        add_work.send_keys(Keys.ENTER)

        add_work_done = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
        print("=> Add new work successfully")
        time.sleep(3)
        
        

        source1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
        target1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-works-empty')]/div/span")))
        action = ActionChains(driver)
        action.click_and_hold(source1).move_to_element(target1).move_by_offset(0, -100).release().perform()
        time.sleep(2)
        source2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'"+ str(sprint_name) +"')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
        source2.click()
        print("- View work at Sprint")
        time.sleep(2)
        
        update_work()





def drag_work():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sprint-add-more']//button[contains(.,'Create sprint')]"))).click()
    print("- Create sprint")
    sprint_name = "Sprint: " + str(n)
    input_sprint_name = driver.find_element_by_xpath("//div[@class='sprint-add-more']//input")
    input_sprint_name.send_keys(sprint_name)
    driver.find_element_by_xpath("//div[@class='sprint-add-more']//button[contains(.,'Save')]").click()
    print("- Save Sprint")
    driver.find_element_by_xpath("//div[@class='sprint-header-action']//button[contains(.,'Start Sprint')]").click()
    print("- Start Sprint")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='dialog-footer']/button[contains(.,'OK')]"))).click()
    time.sleep(3)

    name_work = "Automation Test of Scrum: " + str(n)
    driver.find_element_by_xpath("//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div[@class='sprint-add-more']/button").click()
    add_work = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sprint-add-more']//input")))
    add_work.send_keys(name_work)
    add_work.send_keys(Keys.ENTER)

    add_work_done = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
    print("=> Add new work successfully")
    time.sleep(3)
    
    

    source1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
    target1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-works-empty')]/div/span")))
    action = ActionChains(driver)
    action.click_and_hold(source1).move_to_element(target1).move_by_offset(0, -100).release().perform()
    time.sleep(2)
    source2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'"+ str(sprint_name) +"')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
    source2.click()
    print("- View work at Sprint")
    time.sleep(2)
    
    update_work()

#test again



#Trương Mỹ Ngọc test diff





access_hr()
comanage()
