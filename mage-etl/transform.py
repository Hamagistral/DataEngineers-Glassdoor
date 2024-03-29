if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import numpy as np
import datetime
import re

prog_languages = ['python', 'java', 'scala', 'go', 'r', 'c', 'c++', 'c#', 'sql', 'rust', 'bash']
cloud_tools = ['aws', 'azure', 'gcp']
viz_tools = ['power bi', 'tableau', 'excel', 'ssis', 'qlik', 'sap', 'looker']
databases = ['sql server', 'nosql', 'postgresql', 'mongodb', 'mysql', 'oracle', 'casandra', 'elasticsearch', 'dynamodb', 'snowflake', 'redis', 'neo4j', 'hive', 'databricks', 'redshift']
big_data = ['spark', 'hadoop', 'flink']
data_tools = ['airflow', 'kafka', 'dbt']
devops = ['gitlab', 'terraform', 'kubernetes', 'docker', 'jenkins', 'ansible']

education = ['associate', 'bachelor', 'master', 'phd']

def clean_salary(salary_string):

    if pd.isnull(salary_string):
        return np.nan
    else:
        match_year = re.search(r'\$(\d{1,3},?\d{0,3},?\d{0,3}) \/yr \(est.\)', salary_string)
        match_hour = re.search(r'\$(\d+(\.\d+)?) \/hr \(est.\)', salary_string)

        if match_year:
            salary_amount = float(match_year.group(1).replace(',', ''))
        elif match_hour:
            hourly_salary = float(match_hour.group(1))
            salary_amount = hourly_salary * 1800
        else:
            salary_amount = np.nan

        return salary_amount

def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'data analyst' in title.lower():
        return 'data analyst'
    elif 'machine learning' in title.lower():
        return 'mle'
    else:
        return 'na'

def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'sr.' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
            return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'junior'
    else:
        return 'na'


def extract_keywords(description, keywords):
    pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, keywords)))
    matches = set(re.findall(pattern, description.lower(), flags=re.IGNORECASE))
    
    return list(matches)

def extract_degree(description, degrees):
    pattern = r'\b(?:{})\b'.format('|'.join(map(re.escape, degrees)))
    matches = re.findall(pattern, description.lower(), flags=re.IGNORECASE)
    
    if matches:
        return matches[0]
    
    return None

def extract_experience(description):
    pattern = r'(?:Experience level|experience|\+).*(?:\n.*)*(\d+|\+)\s*(?:year|years|\+ years|\+ years of experience)'
    matches = re.findall(pattern, description, flags=re.IGNORECASE)
    
    if matches:
        experience = matches[0]
        if experience == '+':
            return "+10 years"
        elif int(experience) < 2:
            return "0-2 years"
        elif int(experience) < 5:
            return "2-5 years"
        elif int(experience) < 10:
            return "5-10 years"
        else:
            return "+10 years"
    else:
        return None

@transformer
def transform(data, data_2, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    df = data.drop_duplicates(subset=['job_description'])

    df = df.dropna(subset=['company'])
    df['company'] = df['company'].apply(lambda x: x.split('\n')[0].strip())

    df['salary_estimate'] = df['salary_estimate'].apply(clean_salary)
    df['salary_estimate'].fillna(df['salary_estimate'].mean(), inplace=True)
    df['salary_estimate'] = df['salary_estimate'].round().astype(int)

    df['location'] = df['location'].astype(str)
    df['job_state'] = df['location'].apply(lambda x: x if x.lower() == 'remote' else x.split(', ')[-1])

    common_states = df.job_state.value_counts().index.tolist()
    common_state = next((state for state in common_states if state != 'Remote'), None)

    df['job_state']= df['job_state'].replace('United States', common_state)

    cr_median = df.company_rating.mean()
    cr_median = round(cr_median, 1)
    
    df['company_rating'] = df['company_rating'].fillna(cr_median)

    df['company_founded'] = df['company_founded'].fillna(-1)
    df['company_founded'] = df['company_founded'].astype(int)

    today = datetime.datetime.now()

    df['company_age'] = df.company_founded.apply(lambda x: x if x < 0 else today.year - x)
    
    df['job_simp'] = df['job_title'].apply(title_simplifier)
    df = df[df['job_simp'] == 'data engineer']

    df['seniority'] = df['job_title'].apply(seniority)
    df = df[df['seniority'] != "junior"]

    df['job_languages'] = df['job_description'].apply(lambda x: extract_keywords(x, prog_languages))
    df['job_cloud'] = df['job_description'].apply(lambda x: extract_keywords(x, cloud_tools))
    df['job_viz'] = df['job_description'].apply(lambda x: extract_keywords(x, viz_tools))
    df['job_databases'] = df['job_description'].apply(lambda x: extract_keywords(x, databases))
    df['job_bigdata'] = df['job_description'].apply(lambda x: extract_keywords(x, big_data))
    df['job_datatools'] = df['job_description'].apply(lambda x: extract_keywords(x, data_tools))
    df['job_devops'] = df['job_description'].apply(lambda x: extract_keywords(x, devops))

    df['job_education'] = df['job_description'].apply(lambda x: extract_degree(x, education))

    df = df[df['job_education'] != "associate"]
    df = df[df['job_education'] != "phd"]

    df['job_experience'] = df['job_description'].apply(lambda x: extract_experience(x))

    data = pd.concat([df, data_2], axis=0, join="outer")

    data = data[data['salary_estimate'] <= 175000]

    data = data.drop_duplicates(subset=['job_description'])

    print(data.shape)
    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'