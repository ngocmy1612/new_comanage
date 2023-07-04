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
from framework_sample import *
from MN_functions import driver, data, Logging, TestCase_LogResult

n = random.randint(1,1000)
m = random.randint(1,10000)

domain_hr = "tg01.hanbiro.net/ncomanage"
folder_name = "QA Team"

chrome_path = os.path.dirname(Path(__file__).absolute())+"\\chromedriver.exe"
json_file = os.path.dirname(Path(__file__).absolute())+"\\MN_groupware_auto.json"
driver.maximize_window()

def access_hr():
    driver.get("http://" + domain_hr + "/login")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "gw_id")))
    userID = driver.find_element_by_name("gw_id")
    userID.send_keys("automationtest")
    print("- Input user ID")
    password = driver.find_element_by_name("gw_pass")
    password.send_keys("automationtest1!")
    print("- Input user password")
    driver.find_element_by_xpath(data["TIMECARD"]["sign_in"]).click()
    print("- Click button Sign in")
    Waits.Wait10s_ElementLoaded(data["TIMECARD"]["notify"][0])
    print("=> Log in successfully")
    time.sleep(2)
    driver.refresh()

def co_manage():
    Logging("=================================================NEW CO-MANAGE =======================================================")
    gw_project = Waits.Wait20s_ElementLoaded("//a[contains(@href,'/ncomanage/groupware')]")
    time.sleep(3)
    gw_project.click()

    try:
        admin_account = Waits.Wait20s_ElementLoaded(data["COMANAGE"]["admin_account"])
        admin_account = True
        Logging("ADMIN ACCOUNT")
    except:
        admin_account = False
        Logging("USER ACCOUNT")

    return admin_account

def kanban(admin_account):
    Waits.Wait20s_ElementLoaded(data["COMANAGE"]["wait_page"][0])
    Commands.ClickElement(data["COMANAGE"]["project_list1"])
    time.sleep(3)

    try:
        project = Commands.Wait10s_ClickElement(data["COMANAGE"]["project1"])
        Logging("- Open Kanban project")
        project = True
    except:
        Logging("- No project")
        Commands.ClickElement(data["COMANAGE"]["all_project"])
        if admin_account == True:
            create_project()
            project = True
        else:
            project = False
    
    return project

def create_project():
    Commands.ClickElement(data["COMANAGE"]["create_project1"])
    Waits.Wait10s_ElementLoaded(data["COMANAGE"]["wait_alert"])
    pro_name = "Project: " + str(n)
    Commands.InputElement(data["COMANAGE"]["project_name1"], pro_name)
    Commands.ClickElement(data["COMANAGE"]["confirm"])

    infor = Waits.Wait10s_ElementLoaded(data["COMANAGE"]["infor"]+ str(pro_name) +"')]")
    if infor.is_displayed():
        Logging(">> Create new project Successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["create_project"]["pass"])
        infor.click()
        time.sleep(3)
        project_content()
        Commands.ClickElement(data["COMANAGE"]["tab_board"])
    else:
        Logging(">> Create new project Fail")
        Logging(">>>> Cannot continue excution")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["create_project"]["fail"])
        pass

def project_content():
    Commands.ClickElement(data["COMANAGE"]["setting"])
    print("- Setting")
    Waits.Wait10s_ElementLoaded(data["COMANAGE"]["wait_page"][1])
    time.sleep(2)
    Commands.ClickElement(data["COMANAGE"]["roster"])
    print("- View Roster")
    Commands.Wait10s_ClickElement(data["COMANAGE"]["add_leader1"])
    time.sleep(3)

    Commands.InputEnterElement(data["COMANAGE"]["search_leader1"], "auto")
    time.sleep(2)
    Commands.ClickElement(data["COMANAGE"]["select_user"][0])
    Commands.ClickElement(data["COMANAGE"]["select_user"][1])
    Commands.ClickElement(data["COMANAGE"]["select_user"][2])
    Commands.ClickElement(data["COMANAGE"]["add_user"])
    Commands.ClickElement(data["COMANAGE"]["save_button"])
    time.sleep(3)

def run_project(admin_account):
    print("########### KANBAN PROJECT ###########")
    project = kanban(admin_account)
    if project == True:
        insert_work()
        work_list()
    else:
        pass
    
    print("########### SCRUM PROJECT ###########")
    project1 = scrum_project(admin_account)
    if project1 == True:
        new_work()
        #work_list()
        add_folder(folder_name)
        delete_folder(folder_name)
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
    Waits.Wait20s_ElementLoaded(data["COMANAGE"]["wait_page"][2])
    search = driver.find_element_by_xpath(data["COMANAGE"]["search_work1"])
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
    Commands.InputEnterElement(data["COMANAGE"]["insert_work"], insert_work_name)
    Logging("- Insert Work")

    #Search work
    time.sleep(3)
    Commands.InputEnterElement(data["COMANAGE"]["search_work1"], insert_work_name)
    Logging("- Search work")
    time.sleep(5)
    Commands.ClickElement(data["COMANAGE"]["view_ticket1"])
    Logging("- View ticket")
    time.sleep(3)
    detail = Waits.Wait20s_ElementLoaded(data["COMANAGE"]["detail_ticket"])
    if detail.is_displayed():
        Logging("=> View work successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["view_work"]["pass"])

        title_work = Waits.Wait20s_ElementLoaded(data["COMANAGE"]["title_work"])
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
    Commands.ClickElement(data["COMANAGE"]["close"])
    Logging("- Close detail work")
    time.sleep(2)
    search = driver.find_element_by_xpath(data["COMANAGE"]["search_work1"])
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
    start_status = driver.find_element_by_xpath(data["COMANAGE"]["start_status1"])
    start_status.click()
    Logging("- Update status")
    status_list = int(len(driver.find_elements_by_xpath(data["COMANAGE"]["status_list1"])))
    
    
    list_status = []
    i=0
    for i in range(status_list):
        i += 1
        status = driver.find_element_by_xpath(data["COMANAGE"]["status1"] + "[" + str(i) + "]/span")
        if status.text != start_status.text:
            list_status.append(status.text)
        else:
            continue

    Logging("- Total of status: " + str(len(list_status)))
    #Logging(list_status)

    x = random.choice(list_status)
    time.sleep(1)
    status_label = driver.find_element_by_xpath(data["COMANAGE"]["status_label"] + str(x) + "')]")
    status_label.click()
    Logging("- Select status")

    time.sleep(3)
    start_status_update = driver.find_element_by_xpath(data["COMANAGE"]["start_status_update"])
    if start_status_update.text == str(x):
        Logging("=> Update status successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_status"]["pass"])
    else:
        Logging("=> Update status fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_status"]["fail"])

def update_work_type():
    #Select work type
    start_work_type = driver.find_element_by_xpath(data["COMANAGE"]["start_work_type1"])
    #Logging(start_work_type.text)
    start_work_type.click()
    Logging("- Update Work type")
    work_type_list = int(len(driver.find_elements_by_xpath(data["COMANAGE"]["work_type_list1"])))
    
    list_work_type = []
    i=0
    for i in range(work_type_list):
        i += 1
        work_type = driver.find_element_by_xpath(data["COMANAGE"]["work_type1"]+ str(i) + "]//span")
        if work_type.text != start_work_type.text:
            list_work_type.append(work_type.text)
        else:
            continue

    Logging("- Total of work type: " +  str(len(list_work_type)))
    #Logging(list_work_type)

    x = random.choice(list_work_type)
    time.sleep(1)
    work_type_label = driver.find_element_by_xpath(data["COMANAGE"]["work_type_label"] + str(x) + "')]")
    work_type_label.click()
    Logging("- Select work type")

    time.sleep(3)
    start_work_type_update = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["start_work_type_update"])))
    if start_work_type_update.text == str(x):
        Logging("=> Update work type successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_work_type"]["pass"])
    else:
        Logging("=> Update work type fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_work_type"]["fail"])

def update_assigned_to():
    #Select assigned to
    start_assign = driver.find_element_by_xpath(data["COMANAGE"]["start_assign1"])
    #Logging(start_assign.text)
    start_assign.click()
    Logging("- Assigned to")
    time.sleep(3)
    assign_list = int(len(driver.find_elements_by_xpath(data["COMANAGE"]["assign_list1"])))

    list_assign = []
    i=0
    for i in range(assign_list):
        i += 1
        assign = driver.find_element_by_xpath(data["COMANAGE"]["assign"] + str(i) + "]/span")
        if assign.text != start_assign.text:
            list_assign.append(assign.text)
        else:
            continue

    Logging("- Total of assign: " + str(len(list_assign)))
    #Logging(list_assign)

    x = random.choice(list_assign)
    time.sleep(1)
    assign_label = driver.find_element_by_xpath(data["COMANAGE"]["assign_label"] + str(x) + "')]")
    assign_label.click()
    Logging("- Select user")
    
    time.sleep(3)
    start_assign_update = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["start_assign_update"])))
    if start_assign_update.text == str(x):
        Logging("=> Update assigned to successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_assigned_to"]["pass"])
    else:
        Logging("=> Update assigned to fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_assigned_to"]["fail"])

def update_priority():
    #Select priority
    start_priority = driver.find_element_by_xpath(data["COMANAGE"]["start_priority1"])
    #Logging(start_priority.text)
    start_priority.click()
    Logging("- Update priority")
    time.sleep(2)
    priority_list = int(len(driver.find_elements_by_xpath(data["COMANAGE"]["priority_list1"])))
    
    list_priority = []
    i=0
    for i in range(priority_list):
        i += 1
        priority = driver.find_element_by_xpath(data["COMANAGE"]["priority1"] + str(i) + "]/span")
        if priority.text != start_priority.text:
            list_priority.append(priority.text)
        else:
            continue

    Logging("- Total of priority: "+ str(len(list_priority)))
    #Logging(list_priority)

    x = random.choice(list_priority)
    time.sleep(2)
    priority_label = driver.find_element_by_xpath(data["COMANAGE"]["priority_label"] + str(x) + "']")
    time.sleep(2)
    priority_label.click()
    Logging("- Select priority")
    
    time.sleep(3)
    start_priority_update = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["start_priority_update"])))
    if start_priority_update.text == str(x):
        Logging("=> Update priority successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_priority"]["pass"])
    else:
        Logging("=> Update priority fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["update_priority"]["fail"])

def update_CC():
    driver.find_element_by_xpath(data["COMANAGE"]["cc_button"]).click()
    time.sleep(2)
    CC_list = int(len(driver.find_elements_by_xpath(data["COMANAGE"]["CC_list"])))
    x = randrange(1, CC_list +1)
    select_cc = driver.find_element_by_xpath(data["COMANAGE"]["select_cc"]+ str(x) +"]/div/input/following-sibling::label")
    select_cc.click()
    print("- Select CC")
    driver.find_element_by_xpath(data["COMANAGE"]["cc_button"]).click()
    print("- Close CC box")
    time.sleep(2)

def update_date():
    driver.find_element_by_xpath(data["COMANAGE"]["start_date1"]).click()
    Logging("- Start date")
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='react-datepicker__week']//div[@aria-disabled='false'][1]"))).click()
    Logging("- Select start date")
    time.sleep(2)
    driver.find_element_by_xpath(data["COMANAGE"]["end_date1"]).click()
    Logging("- End date")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='react-datepicker__week']//div[@aria-disabled='false'][2]"))).click()
    Logging("- Select end date")

def update_description():
    try:
        content = driver.find_element_by_xpath(data["COMANAGE"]["content"])
        content.click()
        print("- Click to add description")
        time.sleep(2)
        insert_work = driver.find_element_by_xpath(data["COMANAGE"]["insert_work1"])
        insert_work.send_keys(data["COMANAGE"]["input_description"])
        Logging("- Input Description")
        driver.find_element_by_xpath(data["COMANAGE"]["save_des"]).click()
        Logging("- Save Description")
    except:
        hover_description = driver.find_element_by_xpath(data["COMANAGE"]["hover_description"])
        hover_1 = ActionChains(driver).move_to_element(hover_description)
        hover_1.perform()
        edit_button = driver.find_element_by_xpath(data["COMANAGE"]["edit_button"])
        edit_button.click()
        time.sleep(2)
        insert_work = driver.find_element_by_xpath(data["COMANAGE"]["insert_work1"])
        insert_work.clear()
        insert_work.send_keys(data["COMANAGE"]["input_description"])
        Logging("- Input Description")
        driver.find_element_by_xpath(data["COMANAGE"]["save_des"]).click()
        Logging("- Save Description")

def write_comment():
    #Comment
    driver.find_element_by_xpath(data["COMANAGE"]["write_comment"]).click()
    time.sleep(2)
    insert_comment = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["insert_comment"])))
    insert_comment.click()
    insert_comment.send_keys(data["COMANAGE"]["input_comment"])
    Logging("- Input comment")
    save_comment = driver.find_element_by_xpath(data["COMANAGE"]["save_comment1"])
    save_comment.click()
    Logging("- Save comment")
    try:
        comment_work = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["comment_work"])))
        if (data["COMANAGE"]["input_comment"]) == comment_work.text:
            Logging("=> Write comment Successfully")
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["write_comment"]["pass"])
        else:
            Logging("=> Wrong content comment")
    except:
        Logging("=> Write comment Fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["write_comment"]["fail"])

    driver.find_element_by_xpath(data["COMANAGE"]["edit_comment"]).click()
    print("- Click edit comment")
    time.sleep(2)
    insert_comment1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["insert_comment"])))
    insert_comment1.clear()
    time.sleep(2)
    insert_comment1.send_keys("This is comment after edit")
    save_comment1 = driver.find_element_by_xpath(data["COMANAGE"]["save_comment1"])
    save_comment1.click()
    print("- Save comment edit")
    
def work_list():
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["work_list1_page"])))

    driver.find_element_by_xpath(data["COMANAGE"]["work_list1"]).click()
    Logging("- Work List")
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["work_list_page"])))
    try:
        x = filters_worktype()
    except:
        pass

def filters_worktype():
    driver.find_element_by_xpath(data["COMANAGE"]["filter_work_type"]).click()
    Logging("- Search Work type")
    filter_work_list = int(len(driver.find_elements_by_xpath(data["COMANAGE"]["filter_work_list1"])))

    list_filter_work = []
    i=0

    for i in range(filter_work_list):
        i += 1
        filter_work = driver.find_element_by_xpath(data["COMANAGE"]["filter_work"] + str(i) + "]//span") 
        list_filter_work.append(filter_work.text)
    
    Logging("- Total filter Work type: "+ str(len(list_filter_work)))
    #Logging(list_filter_work)

    x = random.choice(list_filter_work)
    filter_work_select = driver.find_element_by_xpath(data["COMANAGE"]["filter_work_select"] + str(x) + "')]")
    filter_work_select.click()
    Logging("- Filter Work type")
    time.sleep(3)

    try:
        work_list = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["work_list2"])))
        if work_list.is_displayed():
            driver.find_element_by_xpath(data["COMANAGE"]["filter_work_type"]).click()
            time.sleep(2)
            work_list.click()
            try:
                sub_name = check_filter(x)
            except:
                Logging("- Check filter Fail")
                pass
    except:
        Logging("- No data found!")
        driver.find_element_by_xpath(data["COMANAGE"]["clear_filter"]).click()
        Logging("- Clear filter")

    return x

def check_filter(x):
    detail_work = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["detail_work1"])))
    time.sleep(2)
    if detail_work.is_displayed():
        Logging("=> View work list successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["view_work_list"]["pass"])
        time.sleep(2)
        type_text = driver.find_element_by_xpath(data["COMANAGE"]["type_text"])
        if type_text.text == str(x) == "Sub Task":
            Logging("=> Correct Work type")
        elif type_text.text == str(x):
            Logging("=> Correct Work type")
            driver.find_element_by_xpath(data["COMANAGE"]["create_sub"]).click()
            Logging("- Create Sub work")
            sub_name = "Auto Test: Sub work " + str(m)
            input_sub = driver.find_element_by_xpath(data["COMANAGE"]["input_sub"])
            #input_sub.click()
            input_sub.send_keys(sub_name)
            Logging("- Input Sub work name")
            driver.find_element_by_xpath(data["COMANAGE"]["save_sub"]).click()
            Logging("- Save Sub work")
            time.sleep(3)
            sub_work_title = driver.find_element_by_xpath(data["COMANAGE"]["sub_work_title"] + sub_name + "')]")
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

        driver.find_element_by_xpath(data["COMANAGE"]["filter_work_type"]).click()
        driver.find_element_by_xpath(data["COMANAGE"]["clear_filter"]).click()
    else:
        Logging("=> View work list fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["view_work_list"]["fail"])

    return sub_name

############################################ Scrum project

def create_scrum_project():
    driver.find_element_by_xpath(data["COMANAGE"]["create_project1"]).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["wait_alert"])))
    scrum_name = "Scrum Project: " + str(m)
    project_scrum = driver.find_element_by_xpath(data["COMANAGE"]["project_name1"])
    project_scrum.send_keys(scrum_name)
    driver.find_element_by_xpath(data["COMANAGE"]["more_project"]).click()
    driver.find_element_by_xpath(data["COMANAGE"]["advanced_project"]).click()
    print("- Scrum Project")
    Commands.ClickElement(data["COMANAGE"]["confirm"])

    infor_scrum = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["infor"]+ str(scrum_name) +"')]")))
    if infor_scrum.is_displayed():
        Logging(">> Create new Scrum project Successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["create_project"]["pass"])
        infor_scrum.click()
        time.sleep(3)
        project_content()
        driver.find_element_by_xpath(data["COMANAGE"]["backlog"]).click()
    else:
        Logging(">> Create new Scrum project Fail")
        Logging(">>>> Cannot continue excution")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["create_project"]["fail"])
        pass
    
def scrum_project(admin_account):
    Commands.ClickElement(data["COMANAGE"]["all_project"])
    time.sleep(3)

    try:
        project1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, data["COMANAGE"]["project2"]))).click()
        Logging("- Open Scrum project")
        project1 = True
    except:
        Logging("- No project")
        Commands.ClickElement(data["COMANAGE"]["all_project"])
        if admin_account == True:
            create_scrum_project()
            project1 = True
        else:
            project1 = False
    
    return project1

def startsprint():
    driver.find_element_by_xpath("//div[@class='sprint-header-action']//button[contains(.,'Start Sprint')]").click()
    print("- Start Sprint")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='dialog-footer']/button[contains(.,'OK')]"))).click()
    time.sleep(3)

def addwork(sprint_name):
    name_work = "Automation Test of Scrum: " + str(n)
    driver.find_element_by_xpath("//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div[@class='sprint-add-more']/button").click()
    add_work = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sprint-add-more']//input")))
    add_work.send_keys(name_work)
    add_work.send_keys(Keys.ENTER)

    try:
        add_work_done = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
        Logging("=> Add new work Successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["insert_work"]["pass"])
        time.sleep(3)
        source1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'Backlog')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
        target1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sprint'][1]//div[contains(@class,'sprint-works')]")))
        action = ActionChains(driver)
        action.click_and_hold(source1).move_to_element(target1).move_by_offset(0, -100).release().perform()
        time.sleep(2)
        source2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'sprint-header-title') and contains(.,'"+ str(sprint_name) +"')]/../following-sibling::div//div[@title='"+ str(name_work) +"']")))
        source2.click()
        Logging("- View work at sprint")
        time.sleep(2)
        
        update_work()
    except:
        Logging("=> Add new work Fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["insert_work"]["fail"])
        Logging(">>>> Cannot continue excution")
        pass

def add_epic():
    epicname = "Epic auto " + str(n)
    subjectname = "Subject auto " + str(n)
    driver.find_element_by_xpath("//div[@class='sprint-left'] //li/span[text()='Epics']").click()
    Logging("- Add Epic")
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='sprint-left'] //div[@class='epic-header-center']/a[text()='Create new']").click()
    epic_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='MuiDialogContent-root'] //input[@placeholder='Epic name']")))
    epic_name.send_keys(epicname)
    Logging("- Input Epic name")
    subject_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='MuiDialogContent-root'] //input[@placeholder='Subject']")))
    subject_name.send_keys(subjectname)
    Logging("- Input Subject name")
    time.sleep(2)
    driver.find_element_by_xpath("//div[@class='dialog-footer'] //button[text()='Save']").click()
    Logging("- Save Epic")
    time.sleep(3)
    try:
        driver.find_element_by_xpath("//div[@class='sprint-left']//div[@class='epic-content-header-title']//span[@class='e-title' and contains(text(),'" + str(epicname) + "')]")
        Logging("=> Add Epic Successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["add_epic"]["pass"])
    except:
        Logging("=> Add Epic Fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["add_epic"]["fail"])

    driver.find_element_by_xpath("//div[@class='sprint-left']//div[@class='epic-header-right']").click()

def new_work():
    driver.find_element_by_xpath(data["COMANAGE"]["backlog"]).click()
    time.sleep(3)
    try:
        add_epic()
    except:
        pass
    
    count_sprint = int(len(driver.find_elements_by_xpath("//div[@class='sprint-right']//div[@class='sprint-container']/div")))
    if count_sprint > 2:
        get_name_sprint = driver.find_element_by_xpath("//div[@class='sprint'][1]//div[@class='sprint-header-title']//strong")
        sprint_name = get_name_sprint.text
        try:
            start_sprint = driver.find_element_by_xpath("//div[@class='sprint-right']//div[@class='sprint-container']/div[2]//div[@class='sprint-header-action']//button[text()='Start Sprint']")
            startsprint()
            addwork(sprint_name)
        except:
            addwork(sprint_name)

    elif count_sprint == 2:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='sprint-add-more']//button[contains(.,'Create sprint')]"))).click()
        print("- Create sprint")
        sprint_name = "Sprint: " + str(n)
        input_sprint_name = driver.find_element_by_xpath("//div[@class='sprint-add-more']//input")
        input_sprint_name.send_keys(sprint_name)
        driver.find_element_by_xpath("//div[@class='sprint-add-more']//button[contains(.,'Save')]").click()
        print("- Save Sprint")
        startsprint()
        addwork(sprint_name)
        
def add_folder(folder_name):
    search_folder = driver.find_element_by_xpath("//div[@class='content-search']//input")
    search_folder.send_keys(folder_name)
    search_folder.send_keys(Keys.ENTER)
    try:
        default_folder = driver.find_element_by_xpath("//div[@class='han-tree-folder']/a/span[contains(.,'" + str(folder_name) + "')]")
        if default_folder.is_displayed():
            print("- Folder was already")
            Commands.ClickElement(data["COMANAGE"]["all_project"])
            add_project(folder_name)
    except:
        driver.find_element_by_xpath("//div[contains(@class,'co-manage-project-list-left-menu')]//a[contains(.,'Add Folder')]").click()
        driver.find_element_by_xpath("//div[@id='wrap-content-project']//li[@class='button-group']/button").click()
        print("- Click button plus")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='alert-dialog-title']")))
        
        subject = driver.find_element_by_xpath("//input[@placeholder='Subject']")
        subject.send_keys(folder_name)
        Commands.ClickElement(data["COMANAGE"]["confirm"])
        print("- Save folder")
        time.sleep(2)
        Commands.ClickElement(data["COMANAGE"]["all_project"])
        try:
            add_project(folder_name)
            Logging("=> Add folder successfully")
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["add_folder"]["pass"])
        except:
            Logging("=> Add folder fail")
            TestCase_LogResult(**data["testcase_result"]["co_manage"]["add_folder"]["fail"])

def add_project(folder_name):
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[@id='wrap-content-project']//div[@class='content-table']/div[1]/div/div[contains(@class,'custom-checkbox')]"))).click()
    project1 = driver.find_element_by_xpath("//*[@id='wrap-content-project']//div[@class='content-table']/div[1]//div[@class='column'][3]//a")
    project1_name = project1.text

    print("- Select project")
    time.sleep(3)
    driver.find_element_by_xpath("//*[@id='wrap-content-project']//li[@class='button-group'][3]").click()
    select_folder = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//*[@id='alert-dialog-title']/following-sibling::div//a/span[contains(.,'"+ str(folder_name) +"')]")))
    time.sleep(2)
    select_folder.click()
    print("- Select folder")
    driver.find_element_by_xpath("//button[text()='Confirm']").click()
    print("- Confirm select folder")
    time.sleep(3)

    folder_name_project1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[@id='wrap-content-project']//div[@class='content-table']/div[1]//div[@class='column'][8]/div")))
    time.sleep(2)
    if folder_name_project1.text == folder_name:
        Logging(">> Add project to folder Successfully")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["add_project"]["pass"])
    else:
        Logging(">> Add project to folder Fail")
        TestCase_LogResult(**data["testcase_result"]["co_manage"]["add_project"]["fail"])

def delete_folder(folder_name):
    time.sleep(3)
    driver.find_element_by_xpath("//div[contains(@class,'co-manage-project-list-left-menu')]//a[contains(.,'Add Folder')]").click()
    delete_fol = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='wrap-content-project']//div[@data-type='SplitPane']//div[@class='bd-b' and contains(.,'"+ str(folder_name) +"')]//button[2]")))
    time.sleep(2)
    driver.execute_script("arguments[0].scrollIntoView();", delete_fol)
    delete_fol.click()
    print("- Delete Folder")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@aria-labelledby,'alert-dialog-title')]//button[text()='Confirm']"))).click()
    print("- Confirm delete folder")
    #delete_fol.location_once_scrolled_into_view


access_hr()
comanage()
