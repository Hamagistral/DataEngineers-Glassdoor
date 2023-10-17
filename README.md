<div align="center">
  <a href="https://jobsglassdoor-dataengineers.streamlit.app/">
    <img src="https://user-images.githubusercontent.com/66017329/223897397-46ed35cb-2f61-4cfc-9f38-0cf8b472a864.png" alt="Banner" width="720">
  </a>

  <div id="user-content-toc">
    <ul>
      <summary><h1 style="display: inline-block;">Glassdoor Data Engineer Jobs</h1></summary>
    </ul>
  </div>
  
  <p>Gain insights into the job market for data engineers in the USA</p>
    <a href="https://jobsglassdoor-dataengineers.streamlit.app/" target="_blank">Live Preview</a>
    🛸
    <a href="https://www.kaggle.com/datasets/hamzaelbelghiti/data-engineering-jobs-in-the-usa-glassdoor" target="_blank">Data on Kaggle</a>
    🌪️
    <a href="https://github.com/Hamagistral/DataEngineers-Glassdoor/issues" target="_blank">Request Feature</a>
</div>
<br>
<div align="center">
      <a href="https://jobsglassdoor-dataengineers.streamlit.app/"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg"/></a>
      <img src="https://img.shields.io/github/stars/hamagistral/DataEngineers-Glassdoor?color=blue&style=social"/>
</div>

## 📝 Table of Contents

1. [ Project Overview ](#introduction)
2. [ Project Architecture ](#arch)
3. [ Web Scrapinng ](#webscraping)
4. [ Data Cleaning, EDA and Model Building](#dataedamodel)
5. [ Installation ](#installation)
6. [ References ](#refs)
7. [ Contact ](#contact)
<hr>

### 🕵️ Data Exploration Page
![image](https://github.com/Hamagistral/DataEngineers-Glassdoor/assets/66017329/3156c441-3b9e-4ab9-9f37-0a9ebc596d92)


### 💸 Salary Prediction Page
![image](https://github.com/Hamagistral/DataEngineers-Glassdoor/assets/66017329/fde4a263-e1ad-454a-b658-aff30745362f)


<a name="introduction"></a>
## 🔬 Project Overview :

### 🎯 Goal :

The goal of this data science project is to gain insights into the job market for data engineers in the USA. By analyzing job postings and related data from Glassdoor, the project aims to identify the most in-demand tools, education degrees, and other qualifications required by companies hiring for this role. Additionally, the project seeks to create a model to predict salaries for data engineers based on a variety of factors including location, company industry and rating, education level, and seniority.

### 🧭 Steps :

The project begins with web scraping weekly job postings posted last week of data engineering roles from Glassdoor in the US. The collected data includes job titles, company names, job locations, job descriptions, salaries, education requirements, and required skills. The data is named like "glassdoor-data-engineer-15-2023.csv" where 15 is the week number the data was scraped in and 2023 is the year, then it's stored locally on data/raw/ folder then it's uploaded to an AWS S3 Bucket containing  only the raw uncleaned data. The data is then cleaned and preprocessed to remove irrelevant information and ensure consistency, the duplicates are dropped then it's joined with the initial cleaned data in another S3 Bucket containing only one csv file that contains all the job postings. All of this is automated in a data pipeline using MageAI.

Exploratory data analysis (EDA) is performed on the cleaned data to gain insights into trends and patterns. This includes identifying the most common job titles, the industries and locations with the highest demand, and the most commonly required skills and education degrees. EDA also involves creating visualizations to aid in understanding the data.

After EDA, feature engineering is performed to create new features that may improve the accuracy of the salary prediction model. This includes creating dummy variables for categorical features such as location, education level, and seniority.

The salary prediction model is built using a random forest regressor. Finally, the model is deployed in a web application using Streamlit, allowing users to input their own data and receive a salary prediction based on the model.

<a name="arch"></a>
## 📝 Project Architecture

![Project Arch](https://github.com/Hamagistral/DataEngineers-Glassdoor/assets/66017329/fcecfbbf-d78b-41c8-b8ab-84275fbae73f)

### ⚙️ Mage ETL :

![ETL](https://github.com/Hamagistral/DataEngineers-Glassdoor/assets/66017329/f6001cab-f061-47d2-ab94-334e94d27bd9)

### 🛠️ Technologies Used

![Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
<img src="https://user-images.githubusercontent.com/66017329/236063928-77e42e58-26aa-425f-88eb-1b46fa76fd8c.png" alt="mageai" width="70">
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
<img src="https://user-images.githubusercontent.com/66017329/223900076-e1d5c1e5-7c4d-4b73-84e7-ae7d66149bc6.png" alt="Banner" width="100">

<a name="webscraping"></a>
## 🕸️ Web Scraping

I adjusted the web scraper using Selenium to scrape data engineering jobs posted last week from Glassdoor US. The output file is then stored in the "/data/raw" folder under the name of "glassdoor-data-engineer-15-2023.csv" where "15" is the week number where the job was posted and "2023" the year. See code [here](https://github.com/Hamagistral/DataEngineers-Glassdoor/blob/master/scripts/glassdoor_scraper.py).

With each job, I obtained the following: Company Name, Job title, Salary Estimate, Job Description, Rating, Job Location, Company Size, Company Founded Date, Type of Ownership, Industry and Sector. The main challenge for this scraping task, was the duplicated job postings, after the 6th page or so the glassdoor website keeps rerendring the first jobs listings, so all the jobs scraped become a duplicates. That's why I came up with the idea to implement a scheduler to run the script once every week to get the latest job listings, and then usin a data pipeline clean and transform the data then joining it with the cleaned dataset stored in aws s3 bucket that contains all non duplicated and cleaned job listings from previous weeks.

<a name="dataedamodel"></a>
## 🧹 Data Cleaning, EDA and Model Building

Please refer to the respective notebooks ([data cleaning](https://github.com/Hamagistral/DataEngineers-Glassdoor/blob/master/notebooks/data_cleaning.ipynb), [data eda](https://github.com/Hamagistral/DataEngineers-Glassdoor/blob/master/notebooks/data_eda.ipynb), [model buidling](https://github.com/Hamagistral/DataEngineers-Glassdoor/blob/master/notebooks/data_modeling.ipynb)).

<a name="installation"></a>
## 🖥️ Installation : 
1. Clone the repository:

```
git clone https://github.com/Hamagistral/DataEngineers-Glassdoor.git
```

2. Install the required packages:

```
pip install -r requirements.txt
```

### - Run Mage

1. Change directory to mage-etl:

```
cd mage-etl
```

2. Launch project : 

```
mage start glassdoor_dataengjobs
```

3. Run pipeline :

```
mage run glassdoor_dataengjobs glassdoor_dataeng_pipeline
```

### - Usage : 
1. Change directory to streamlit:

```
cd streamlit
```

2. Run the app:

```
streamlit run 01_🕵️_Explore_Data.py
```

<a name="refs"></a>
## 📋 References

**Project inspired by**: https://github.com/PlayingNumbers/ds_salary_proj  
**Scraper Github:** https://github.com/arapfaik/scraping-glassdoor-selenium  
**Scraper Article:** https://towardsdatascience.com/selenium-tutorial-scraping-glassdoor-com-in-10-minutes-3d0915c6d905  
**Mage ETL inspired by**: https://youtu.be/WpQECq5Hx9g  
**Streamlit App inspired by**: https://youtu.be/xl0N7tHiwlw

<a name="contact"></a>
## 📨 Contact Me

[LinkedIn](https://www.linkedin.com/in/hamza-elbelghiti/) •
[Website](https://Hamagistral.me) •
[Gmail](hamza.lbelghiti@gmail.com)
