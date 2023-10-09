import streamlit as st
import pandas as pd
import altair as alt
import boto3

st.set_page_config(page_title="Exploratory Data Analysis", page_icon='👨‍💻')

# Countplot of tools 
def filtered_keywords(tools, keywords, head=10):
    # get keywords in a column
    count_keywords = pd.DataFrame(tools.sum()).value_counts().rename_axis('keywords').reset_index(name='counts')
    
    # get frequency of occurrence of word (as word only appears once per line)
    length = len(tools) # number of job postings
    count_keywords['percentage'] = count_keywords.counts / length

    # plot the results
    count_keywords = count_keywords[count_keywords.keywords.isin(keywords)]
    count_keywords = count_keywords.head(head)
    

    bar_chart = alt.Chart(count_keywords).mark_bar(cornerRadiusBottomRight=10, cornerRadiusTopRight=10).encode(
        x=alt.X('percentage', type="quantitative", title=None, axis=alt.Axis(format='%', labelFontSize=17, titleFontSize=17)),
        y=alt.Y('keywords', type="nominal", title=None, sort=None, axis=alt.Axis(labelFontSize=20)),
        color='keywords',
        tooltip=["keywords", alt.Tooltip("percentage", format=".1%")]
    ).configure_axis(
        labelFontSize=18,
        grid=False
    ).configure_text(
        fontSize=16,
        fontWeight='bold'
    ).configure_legend(
        disable=True
    ).properties(
        height=500
    ).configure_view(
        strokeWidth=0
    )

    st.altair_chart(bar_chart, use_container_width=True)

@st.cache_resource
def load_data():

    s3 = boto3.resource('s3', aws_access_key_id=st.secrets['AWS_ACCESS_KEY_ID'], aws_secret_access_key=st.secrets['AWS_SECRET_ACCESS_KEY'])
    bucket = s3.Bucket(st.secrets['AWS_BUCKET_NAME'])
    obj = bucket.Object('glassdoor-data-engineer-2023.csv')
    body = obj.get()['Body']
    df = pd.read_csv(body)
        
    cols = ['job_languages', 'job_cloud', 'job_viz', 'job_databases', 'job_bigdata', 'job_datatools', 'job_devops']

    def safe_eval(x):
        try:
            return eval(x)
        except:
            return x

    df[cols] = df[cols].astype(str).applymap(safe_eval)

    return df

df = load_data()

# Data Engineering Skills
prog_languages = ['python', 'java', 'scala', 'go', 'r', 'c', 'c++', 'c#', 'sql', 'rust', 'bash']
cloud_tools = ['aws', 'azure', 'gcp']
viz_tools = ['power bi', 'tableau', 'excel', 'ssis', 'qlik', 'sap', 'looker']
databases = ['sql server', 'nosql', 'postgresql', 'mongodb', 'mysql', 'oracle', 'casandra', 'elasticsearch', 'dynamodb', 'snowflake', 'redis', 'neo4j', 'hive', 'databricks', 'redshift']
big_data = ['spark', 'hadoop', 'flink']
data_tools = ['airflow', 'kafka', 'dbt']
devops = ['gitlab', 'terraform', 'kubernetes', 'docker', 'jenkins', 'ansible']

def show_explore_page():

    st.header("🕵️ Exploring Data Engineer Jobs")
    st.write(f":blue[{len(df)} jobs analyzed from Glassdoor USA]")

    st.info("##### Gain insights into the job market for data engineers in the USA")

    # Data Engineering Skills
    st.markdown("#### 🛠️ Top Skills for Data Engineers")

    type = st.radio("Skills :", ('Languages', 'Cloud', 'Visualization', 'Databases', 'Big Data', 'Data Tools', 'Dev Ops'), horizontal=True)

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
    elif type == "Big Data":
        data = df['job_bigdata']
        tools = big_data
    elif type == "Dev Ops":
        data = df['job_devops']
        tools = devops
    elif type == "Data Tools":
        data = df['job_datatools']
        tools = data_tools

    filtered_keywords(data, tools)

    st.markdown("#")

    # Salary Distribution
    st.markdown("#### 🤑 Average Salary")

    st.markdown("How much does a Data Engineer make in average in the United States?")

    avg_salary = df['salary_estimate'].mean()
    st.success(f"### 💲 {round(avg_salary):,} per year.")

    st.markdown("#")

    # Most in Demand Degrees
    st.markdown("#### 🎓 Most in Demand Degrees for Data Engineers")

    degree_counts = df['job_education'].value_counts().reset_index()
    degree_counts.columns = ['Degree', 'Count']

    education_chart = alt.Chart(degree_counts).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10).encode(
        x=alt.Y('Degree:N', title=None),
        y=alt.X('Count:Q', title=None),
        color="Degree"
    ).properties(
        height=500
    ).configure_axis(
        labelFontSize=18,
        labelAngle=0,
        grid=False
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

    experience_chart = alt.Chart(exp_counts).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10).encode(
        x=alt.X('Experience:N', sort='-y', title=None),
        y=alt.Y('Count:Q', title=None),
        color=alt.Color('Experience', legend=None)
    ).properties(
        height=500
    ).configure_axis(
        labelFontSize=18,
        labelAngle=0,
        grid=False
    )

    st.altair_chart(experience_chart, use_container_width=True)


    # Salary Distribution
    st.markdown("#### 🤑 Salary Distribution")

    salary_chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=10, cornerRadiusTopRight=10, interpolate='step', binSpacing=0.8).encode(
        x=alt.X('salary_estimate:Q', bin=alt.Bin(maxbins=10), title="Salary Estimate in $"),
        y=alt.Y('count()', title=None),
        color=alt.Color('count()', legend=None)
    ).properties(
        height=500
    ).configure_axis(
        grid=False
    )

    st.altair_chart(salary_chart, use_container_width=True)

    # Top Company Industries
    st.markdown("#### 🚀 Top 10 Company Industries Recruiting Data Engineers")

    industry_counts = df['company_industry'].value_counts().reset_index().head(10)
    industry_counts.columns = ['Industry', 'Count']

    industries_chart = alt.Chart(industry_counts).mark_bar(cornerRadiusBottomRight=10, cornerRadiusTopRight=10).encode(
        y=alt.Y('Industry:N', sort='-x', title=None),
        x=alt.X('Count:Q', title=None),
        color=alt.Color('Industry', legend=None)
    ).properties(
        height=500
    ).configure_axis(
        labelFontSize=12,
        grid=False
    )

    st.altair_chart(industries_chart, use_container_width=True)

    st.markdown("""### For more Data Analysis and Exploration see : [🖥️ GitHub](https://github.com/Hamagistral/DataEngineers-Glassdoor/blob/master/notebooks/data_eda.ipynb)""")
    
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """

    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

show_explore_page()
