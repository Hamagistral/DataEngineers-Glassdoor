import streamlit as st

st.set_page_config(page_title="About", page_icon='📊')

st.header("📊 About The Project")

st.markdown("### 🎯 Goal :")

st.write("""The goal of this data science project is to gain insights into the job market for data engineers in the USA. 
             By analyzing job postings and related data from Glassdoor, the project aims to identify the most in-demand tools, 
             education degrees, and other qualifications required by companies hiring for this role. Additionally, the project seeks 
             to create a model to predict salaries for data engineers based on a variety of factors including location, company industry 
             and rating, education level, and seniority.""")
    
st.markdown("### 🧭 Project Overview :")

st.write("""The project begins with web scraping job postings for data engineers from Glassdoor. The collected data includes job titles, 
                company names, job locations, job descriptions, salaries, education requirements, and required skills. The data is then cleaned and 
                preprocessed  to remove irrelevant information and ensure consistency.""")

st.write("""Exploratory Data Analysis (EDA) is performed on the cleaned data to gain insights into trends and patterns. This includes identifying 
                the most common job titles, the industries and locations with the highest demand, and the most commonly required skills and education 
                degrees. EDA also involves creating visualizations to aid in understanding the data.""")

st.write("""After EDA, feature engineering is performed to create new features that may improve the accuracy of the salary prediction model. 
                This includes creating dummy variables for categorical features such as location, education level, and seniority.""")

st.write("""The salary prediction model is built using a random forest regressor. Finally, the model is deployed in a web application using Streamlit, 
                allowing users to input their own data and receive a salary prediction based on the model.""")
    
st.markdown("### 🔗 Links :")

st.markdown("""##### [📘 Data on Kaggle](https://www.kaggle.com/datasets/hamzaelbelghiti/data-engineering-jobs-in-the-usa-glassdoor) | [😼 See full project on GitHub](https://github.com/Hamagistral/DataEngineeringJobs-Analysis) | [📨 Contact me via LinkedIn](https://www.linkedin.com/in/hamza-elbelghiti/) """)

# Hide Left Menu
st.markdown("""<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)