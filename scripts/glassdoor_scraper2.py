from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Because Glassdoor stops showing job listing informations avisiting 20 pages, we need to scrape another time starting from page 21 to the end page 30.

def get_jobs(keyword, num_pages, path):

    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    # Initializing the webdriver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    # In the parameter "IP21" in the url makes the link go to the 21st page
    url = "https://www.glassdoor.com/Job/united-states-"+keyword+"-jobs-SRCH_IL.0,13_IN1_KO14,27_IP21.htm?includeNoSalaryJobs=true&jobType=fulltime"
    driver.get(url)
        
    time.sleep(5)
    
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
                        driver.find_element(By.XPATH,".//span[@class='SVGInline modal_closeIcon']").click()
                        time.sleep(2)
                    except NoSuchElementException:
                        time.sleep(2)
                        pass

                    # Expands the Description section by clicking on Show More
                    try:
                        driver.find_element(By.XPATH, "//div[@class='css-t3xrds e856ufb4']").click()
                        time.sleep(1)
                    except:
                        time.sleep(2)
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
                driver.find_element(By.XPATH,"//span[@alt='next-icon']").click()   
                current_page = current_page + 1
                time.sleep(4)
            
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
    
    data_path = '../data/raw'
    df.to_csv(data_path + "glassdoor-"+keyword+"-after20.csv", index=False) 


# Scraping the Glassdoor website beginning from page 21 to 30
path = "chromedriver"
get_jobs('data-engineer', 10, path) 