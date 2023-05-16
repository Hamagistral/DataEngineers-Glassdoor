<div align="center">
  <a href="https://jobsglassdoor-dataengineers.streamlit.app/">
    <img src="https://user-images.githubusercontent.com/66017329/223897397-46ed35cb-2f61-4cfc-9f38-0cf8b472a864.png" alt="Banner" width="720">
  </a>

  <div id="user-content-toc">
    <ul>
      <summary><h1 style="display: inline-block;">Glassdoor Data Engineering Jobs</h1></summary>
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
<hr>

### 🕵️ Data Exploration Page
![image](https://user-images.githubusercontent.com/66017329/223897683-bbc5ebb9-abd4-48db-86ea-3127ad2cc2e2.png)

### 💸 Salary Prediction Page

![image](https://user-images.githubusercontent.com/66017329/223897830-beaf5abc-526e-48ee-b07b-bc7a0034ca4a.png)

#### 🎯 Goal :

The goal of this data science project is to gain insights into the job market for data engineers in the USA. By analyzing job postings and related data from Glassdoor, the project aims to identify the most in-demand tools, education degrees, and other qualifications required by companies hiring for this role. Additionally, the project seeks to create a model to predict salaries for data engineers based on a variety of factors including location, company industry and rating, education level, and seniority.

#### 🧭 Project Overview :

The project begins with web scraping weekly job postings posted last week of data engineering roles from Glassdoor in the US. The collected data includes job titles, company names, job locations, job descriptions, salaries, education requirements, and required skills. The data is named like "glassdoor-data-engineer-15-2023.csv" where 15 is the week number the data was scraped in and 2023 is the year, then it's stored locally on data/raw/ folder then it's uploaded to an AWS S3 Bucket containing  only the raw uncleaned data. The data is then cleaned and preprocessed to remove irrelevant information and ensure consistency, the duplicates are dropped then it's joined with the initial cleaned data in another S3 Bucket containing only one csv file that contains all the job postings. All of this is automated in a data pipeline using MageAI.

Exploratory data analysis (EDA) is performed on the cleaned data to gain insights into trends and patterns. This includes identifying the most common job titles, the industries and locations with the highest demand, and the most commonly required skills and education degrees. EDA also involves creating visualizations to aid in understanding the data.

After EDA, feature engineering is performed to create new features that may improve the accuracy of the salary prediction model. This includes creating dummy variables for categorical features such as location, education level, and seniority.

The salary prediction model is built using a random forest regressor. Finally, the model is deployed in a web application using Streamlit, allowing users to input their own data and receive a salary prediction based on the model.

## 📝 Project Architecture

![Project Arch](https://github.com/Hamagistral/DataEngineers-Glassdoor/assets/66017329/fcecfbbf-d78b-41c8-b8ab-84275fbae73f)

## ⚒️ Mage ETL :

![ETL](https://github.com/Hamagistral/DataEngineers-Glassdoor/assets/66017329/f6001cab-f061-47d2-ab94-334e94d27bd9)

## 🛠️ Technologies Used

![Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
<img src="https://user-images.githubusercontent.com/66017329/236063928-77e42e58-26aa-425f-88eb-1b46fa76fd8c.png" alt="mageai" width="70">
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
<img src="https://user-images.githubusercontent.com/66017329/223900076-e1d5c1e5-7c4d-4b73-84e7-ae7d66149bc6.png" alt="Banner" width="100">

### Installation : 
1. Clone the repository:

`git clone https://github.com/Hamagistral/DataEngineers-Glassdoor.git`

2. Install the required packages:

`pip install -r requirements.txt`

### Run Mage

1. Change directory to mage-etl:

`cd mage-etl`

2. Run project : 

`mage start [project_name]`


### Usage : 
1. Run the app:

`streamlit run app.py`

2. Enter the OpenAI API Key followed by YouTube video URL and the question you want to ask.

3. Click on the **Generate Answer** button to get the answer to your question.

## 📨 Contact Me

[LinkedIn](https://www.linkedin.com/in/hamza-elbelghiti/) •
[Website](https://Hamagistral.me) •
[Gmail](hamza.lbelghiti@gmail.com)
