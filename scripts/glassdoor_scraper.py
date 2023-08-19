from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from dotenv import load_dotenv
import pandas as pd
import datetime
import time

import os
import boto3

load_dotenv()

# Uploading data to AWS S3 Bucket
s3 = boto3.client('s3', aws_access_key_id=os.environ.get("ACCESS_KEY"), aws_secret_access_key=os.environ.get("SECRET_KEY"))

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

# Get the last week number
week_num = str(datetime.date.today().isocalendar()[1] - 1)
year = str(datetime.date.today().year)

# Glassdoor Job Scraper
def get_jobs(keyword, num_pages, path):

    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1120, 1000)

    # Data Engineers job listings in the US posted last week (fromAge=7)
    url = "https://www.glassdoor.com/Job/united-states-" + keyword + "-jobs-SRCH_IL.0,13_IN1_KO14,27.htm?fromAge=7"
    driver.get(url)
        
    time.sleep(3)
    
    company_name = []
    company_rating = []
    job_title = []
    job_description = []
    location = []
    salary_estimate = []
    company_size = []
    company_type = []
    company_sector = []
    company_industry = []
    company_founded = []
    company_revenue = []

    # Set current page to 1
    current_page = 1     
    time.sleep(3)
       
    while current_page <= num_pages:   
        
        done = False
        while not done:
            
            try: 
                job_cards = driver.find_elements(By.XPATH,"//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")
                       
                for card in job_cards:
                    
                    card.click()
                    time.sleep(2)

                    # Closes the signup pop-up
                    try:
                        driver.find_element(By.XPATH,".//button[@class='e1jbctw80 ei0fd8p1 css-1n14mz9 e1q8sty40']").click()
                        time.sleep(2)
                    except NoSuchElementException:
                        time.sleep(2)
                        pass

                    # Expands the Description section by clicking on Show More
                    try:
                        driver.find_element(By.XPATH, "//div[@class='css-t3xrds e856ufb4']").click()
                        time.sleep(1)
                    except:
                        time.sleep(1)
                        pass

                    # Scrape the page
                    try:
                        company_name.append(driver.find_element(By.XPATH,'//div[@data-test="employerName"]').text)
                    except:
                        company_name.append("#N/A")
                        pass

                    try:
                        company_rating.append(driver.find_element(By.XPATH,'//span[@data-test="detailRating"]').text)
                    except:
                        company_rating.append("#N/A")
                        pass

                    try:
                        job_title.append(driver.find_element(By.XPATH,'//div[@data-test="jobTitle"]').text)
                    except:
                        job_title.append("#N/A")
                        pass

                    try:
                        job_description.append(driver.find_element(By.XPATH,'//div[@class="jobDescriptionContent desc"]').text)
                    except:
                        job_description.append("#N/A")
                        pass

                    try:
                        location.append(driver.find_element(By.XPATH,'//div[@data-test="location"]').text)
                    except:
                        location.append("#N/A")
                        pass

                    try:
                        salary_estimate.append(driver.find_element(By.XPATH,"//div[@class='css-1bluz6i e2u4hf13']").text)
                    except:
                        salary_estimate.append("#N/A")
                        pass
                    
                    try:
                        company_size.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Size']//following-sibling::*").text)
                    except:
                        company_size.append("#N/A")
                        pass
                    
                    try:
                        company_type.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Type']//following-sibling::*").text)
                    except:
                        company_type.append("#N/A")
                        pass
                        
                    try:
                        company_sector.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Sector']//following-sibling::*").text)
                    except:
                        company_sector.append("#N/A")
                        pass
                        
                    try:
                        company_industry.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Industry']//following-sibling::*").text)
                    except:
                        company_industry.append("#N/A")
                        pass
                        
                    try:
                        company_founded.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Founded']//following-sibling::*").text)
                    except:
                        company_founded.append("#N/A")
                        pass
                        
                    try:
                        company_revenue.append(driver.find_element(By.XPATH,"//div[@id='CompanyContainer']//span[text()='Revenue']//following-sibling::*").text)
                    except:
                        company_revenue.append("#N/A")
                        pass

                    done = True
            except:
                pass
                    
            # Moves to the next page         
            if done:
                print(str(current_page) + ' ' + 'out of' +' '+ str(num_pages) + ' ' + 'pages done')
                driver.find_element(By.XPATH,"//button[@class='nextButton job-search-opoz2d e13qs2072']").click()   
                current_page = current_page + 1
                time.sleep(3)
            
    driver.close()
    df = pd.DataFrame({'company': company_name, 
    'company_rating': company_rating,
    'location': location,
    'job_title': job_title,
    'job_description': job_description,
    'salary_estimate': salary_estimate,
    'company_size': company_size,
    'company_type': company_type,
    'company_sector': company_sector,
    'company_industry' : company_industry,
    'company_founded' : company_founded,
    'company_revenue': company_revenue})
    
    data_path = '../data/raw/'
    full_path = data_path + 'glassdoor-'+keyword+'-'+week_num+'-'+year+'.csv'
    df.to_csv(full_path, index=False) 

    csv_filename = 'glassdoor-'+keyword+'-'+week_num+'-'+year+'.csv'

    with open(full_path, 'rb') as f:
        s3.upload_fileobj(f, S3_BUCKET_NAME, csv_filename)


# Scrape last week job postings
path = "chromedriver"
get_jobs(keyword='data-engineer', num_pages=15, path=path) 

data_path = '../data/raw/'
full_path = data_path + 'glassdoor-'+'data-engineer'+'-'+week_num+'-'+year+'.csv'
csv_filename = 'glassdoor-'+'data-engineer'+'-'+week_num+'-'+year+'.csv'

with open(full_path, 'rb') as f:
    s3.upload_fileobj(f, S3_BUCKET_NAME, csv_filename)
