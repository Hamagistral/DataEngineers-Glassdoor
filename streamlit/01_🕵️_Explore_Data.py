import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
from pathlib import Path

st.set_page_config(page_title="Exploratory Data Analysis", page_icon='👨‍💻')

# Countplot of tools 
def filtered_keywords(tools, keywords, head=10):
    # get keywords in a column
    count_keywords = pd.DataFrame(tools.sum()).value_counts().rename_axis('keywords').reset_index(name='counts')
    
    # get frequency of occurrence of word (as word only appears once per line)
    length = len(tools) # number of job postings
    count_keywords['percentage'] = 100 * count_keywords.counts / length

    # plot the results
    count_keywords = count_keywords[count_keywords.keywords.isin(keywords)]
    count_keywords = count_keywords.head(head)
    
    bar_chart = alt.Chart(count_keywords).mark_bar().encode(
        x=alt.X('percentage', type="quantitative", title=None),
        y=alt.Y('keywords', type="nominal", title=None, sort=None),
        color='keywords'
    ).configure_axis(
        labelFontSize=18
    ).configure_text(
        fontSize=16,
        fontWeight='bold'
    ).configure_legend(
        disable=True
    ).properties(
        height=500
    )

    st.altair_chart(bar_chart, use_container_width=True)


@st.cache_resource
def load_data():

    data_path = Path(__file__).parents[1] / 'data/processed/glassdoor-data-engineer-eda.csv'
    df = pd.read_csv(data_path)
    
    cols = ['job_languages', 'job_cloud', 'job_viz', 'job_databases', 'job_librairies']

    def safe_eval(x):
        try:
            return eval(x)
        except:
            return x

    df[cols] = df[cols].astype(str).applymap(safe_eval)

    return df

df = load_data()

# Data Engineering Skills
prog_languages = ['python', 'java', 'scala', 'go', 'r', 'c++', 'c#', 'sql', 'nosql', 'shell', 'rust']
cloud_tools = ['aws', 'azure', 'google cloud', 'snowflake', 'databricks', 'redshift', 'oracle', 'gcp', 'bigquery']
viz_tools = ['power bi', 'tableau', 'excel', 'ssis', 'qlik', 'sap', 'sas', 'dax']
databases = ['sql server', 'postegresql', 'mongodb', 'mysql', 'casandra', 'elasticsearch', 'dynamodb', 'redis', 'neo4j']
librairies = ['spark', 'hadoop', 'kafka', 'airflow']

def show_explore_page():

    st.subheader("🕵️ Exploring Glassdoor Data Engineering Jobs")
    st.write(f":blue[{len(df)} jobs analyzed, March 2023]")

    # Data Engineering Skills
    st.markdown("#### 🛠️ Top Skills for Data Engineers")

    type = st.radio("Skills :", ('Languages', 'Cloud', 'Visualization', 'Databases', 'Librairies'), horizontal=True)

    if type == "Languages":
        data = df['job_languages']
        tools = prog_languages
    elif type == "Cloud":
        data = df['job_cloud']
        tools = cloud_tools
    elif type == "Visualization":
        data = df['job_viz']
        tools = viz_tools
    elif type == "Databases":
        data = df['job_databases']
        tools = databases
    elif type == "Librairies":
        data = df['job_librairies']
        tools = librairies

    filtered_keywords(data, tools)

    # Most in Demand Degrees
    st.markdown("#### 🎓 Most in Demand Degrees for Data Engineers")

    degree_counts = df['job_education'].value_counts().reset_index()
    degree_counts.columns = ['Degree', 'Count']

    education_chart = alt.Chart(degree_counts).mark_bar().encode(
        x=alt.Y('Degree:N', title=None),
        y=alt.X('Count:Q', title=None),
        color="Degree"
    ).properties(
        height=500
    ).configure_axis(
        labelFontSize=18,
        labelAngle=0
    ).configure_text(
        fontSize=16,
        fontWeight='bold'
    ).configure_legend(
        disable=True
    )

    st.altair_chart(education_chart, use_container_width=True)

    # Experience required

    st.markdown("#### ⏲️ Years of Experience Needed")

    exp_counts = df['job_experience'].value_counts().reset_index()
    exp_counts.columns = ['Experience', 'Count']

    experience_chart = alt.Chart(exp_counts).mark_bar().encode(
        x=alt.X('Experience:N', sort='-y', title=None),
        y=alt.Y('Count:Q', title=None),
        color=alt.Color('Experience', legend=None)
    ).properties(
        height=500
    ).configure_axis(
        labelFontSize=18,
        labelAngle=0
    )

    st.altair_chart(experience_chart, use_container_width=True)

    # Salary Distribution
    st.markdown("#### 🤑 Salary Distribution")

    salary_chart = alt.Chart(df).mark_bar(opacity=0.9, interpolate='step', binSpacing=0.8).encode(
        x=alt.X('salary_estimate:Q', bin=alt.Bin(maxbins=20), title="Salary Estimate in $"),
        y=alt.Y('count()', title=None),
        color=alt.value('#FFA500')
    ).properties(
        height=500
    )

    st.altair_chart(salary_chart, use_container_width=True)

    # Top Recruiting Companies
    st.markdown("#### 🖥️ Top 10 Companies Recruiting Data Engineers")

    top10 = df['company'].value_counts().head(10)

    companies_chart = alt.Chart(top10.reset_index()).mark_bar().encode(
        y=alt.Y('index:N', sort='-x', title=None),
        x=alt.X('company:Q', title=None),
        color=alt.Color('index:N', legend=None)
    ).properties(
        height=500
    ).configure_axis(
        labelFontSize=14,
        labelAngle=0
    )

    st.altair_chart(companies_chart, use_container_width=True)

    # Top Company Industries
    st.markdown("#### 🖥️ Top 10 Company Industries Recruiting Data Engineers")

    industry_counts = df['company_industry'].value_counts().reset_index().head(10)
    industry_counts.columns = ['Industry', 'Count']

    industries_chart = alt.Chart(industry_counts).mark_bar().encode(
        y=alt.Y('Industry:N', sort='-x', title=None),
        x=alt.X('Count:Q', title=None),
        color=alt.Color('Industry', legend=None)
    ).properties(
        height=500
    ).configure_axis(
        labelFontSize=12,
    )

    st.altair_chart(industries_chart, use_container_width=True)

    st.markdown("""### For more see : [😼 GitHub](https://github.com/Hamagistral/DataEngineers-Glassdoor/blob/master/notebooks/data_eda.ipynb)""")

show_explore_page()

# Hide Left Menu
st.markdown("""<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)




