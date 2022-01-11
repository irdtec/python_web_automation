#TUTORIAL FROM 
# https://www.youtube.com/watch?v=U6gbGk5WPws&list=PLzMcBGfZo4-n40rB1XaJ0ak1bemvlqumQ&index=3
# https://selenium-python.readthedocs.io/waits.html

import time
from types import WrapperDescriptorType
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support import expected_conditions as EC
import csv



PATH = "C:/Users/760006553/OneDrive - Genpact/Code Tests/Python Courses/Web_Automation/drivers/msedge/msedgedriver.exe"
driver = webdriver.Edge(executable_path=PATH)
driver.get("https://www.empleosmaquila.com/listaofertas.aspx")
jobList = []

def storeJobs():
    tblJobs = driver.find_element(By.ID,"Datagrid1")
    jobItems = tblJobs.find_elements_by_tag_name("tr")
    for job in jobItems:
        headers= job.find_elements_by_tag_name("td")
        if len(headers) ==  5:
            
            #fecha, empleo, empresa. link            
            jobList.append([
                headers[1].text, 
                headers[3].text,
                headers[4].text,
                headers[3].find_element_by_tag_name("a").get_attribute("href")                
            ])
            

def printJobs():
    #select table with content
    tblJobs = driver.find_element(By.ID,"Datagrid1")
    jobItems = tblJobs.find_elements_by_tag_name("tr")
    for job in jobItems:
        headers= job.find_elements_by_tag_name("td")
        if len(headers) ==  5:
            print(headers[3].text)


try:    
    ciudad= Select(driver.find_element(By.ID,"DropCiudad"))
    ciudad.select_by_visible_text('Ciudad Juarez')
    #wait for load
    time.sleep(5) 

   #determine PAGER loop
    pagerCount = 0
    pagination = len(driver.find_elements_by_css_selector(".pager > td > table > tbody > tr > td"))
    pagination = pagination - 2
    
    while pagerCount <= pagination:
        # printJobs()
        storeJobs()
        #click on the next pagination number
        page = driver.find_elements_by_css_selector(".pager > td > table > tbody > tr > td > a")
        page[pagerCount].click()
        pagerCount +=1        
        print("Pages found are:",pagination," --> Pager count is:",pagerCount)

    #save Job list on CSV
    with open('Jobs.csv','w',newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(jobList)
    print('SUCCESSFUL FINISH')
except:
    driver.close()
    driver.quit()
    print('ERRORS OCURRED ON CODE')
finally:
    # print(jobList)
    time.sleep(5)    
    driver.close()
    driver.quit()


