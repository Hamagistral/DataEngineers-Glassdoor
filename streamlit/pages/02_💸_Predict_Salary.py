import streamlit as st
import pickle
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Predict Salary", page_icon='💸')

def load_model():
    model_path = Path(__file__).parents[2] / 'models/model_salary_pred.pkl'
    with open(model_path, 'rb') as file:
        data = pickle.load(file)

    return data

data = load_model()

regressor = data["model"]
le_state = data["le_state"]
le_sen = data["le_sen"]
le_edu = data["le_edu"]
le_exp = data["le_exp"]
le_indu = data["le_indu"]
le_rating = data["le_rating"]

unique_company_ratings = [1., 2., 2.3, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4., 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.]

def show_predict_page():

    st.write("## 💸 Data Engineer Salary Prediction 💹")

    st.write("""#### We need some informations to predict your salary :""")

    states = ('Remote',
                'TX',
                'CA',
                'GA',
                'NJ',
                'MA',
                'NY',
                'VA',
                'DC',
                'IL',
                'FL',
                'NC',
                'PA',
                'MN',
                'CO',
                'OH',
                'WI',
                'OR',
                'MD')

    degrees = ('Bachelor', 'Master')

    experience_years = ('0-2 years', '2-5 years', '5-10 years', '+10 years')

    industries = ('Information Technology Support Services', 'HR Consulting', 'Enterprise Software & Network Solutions', 
                'Computer Hardware Development', 'Business Consulting', 'Biotech & Pharmaceuticals', 'Airlines, Airports & Air Transportation', 
                'Travel Agencies', 'Staffing & Subcontracting', 'Investment & Asset Management', 'Software Development', 
                'Financial Transaction Processing', 'Sports & Recreation', 'Health Care Services & Hospitals', 'Aerospace & Defense', 
                'Beauty & Wellness', 'Accounting & Tax', 'Banking & Lending', 'Consumer Product Manufacturing', 'Internet & Web Services', 
                'National Agencies', 'Publishing', 'Food & Beverage Manufacturing')

    state= st.selectbox("State :", states)

    education = st.selectbox("Education Level :", degrees)
    
    experience = st.selectbox("Years of Experience :", experience_years)

    industry = st.selectbox("Company Industry :", industries)

    company_rating = st.slider("Company Rating (According to Glassdoor) :", 0.0, 5.0, step=0.1, value=unique_company_ratings[0])

    # Convert company_rating to numpy array
    company_rating = np.array([company_rating])

    seniority_pos = st.checkbox("Senior Position")

    if seniority_pos:
        seniority = "senior"
    else:
        seniority = "na"

    # Check if user input is in unique_company_ratings
    if company_rating not in unique_company_ratings:
        # Find closest value in unique_company_ratings
        closest_value = unique_company_ratings[np.argmin(np.abs(unique_company_ratings - company_rating))]
        st.warning(f"The company rating of {company_rating[0]} is not found in the data. The company rating will be replaced by {closest_value} which is the closest valid rating.")
        company_rating = closest_value

    else:
        st.success(f"The company rating of {company_rating[0]} is valid.")

    submit = st.button("Calculate Salary")

    if submit:
        try:
            X = np.array([[state, seniority, education.lower(), experience, industry, company_rating]])
            X[:, 0] = le_state.transform(X[:,0])
            X[:, 1] = le_sen.transform(X[:,1])
            X[:, 2] = le_edu.transform(X[:,2])
            X[:, 3] = le_exp.transform(X[:,3])
            X[:, 4] = le_indu.transform(X[:,4])
            X[:, 5] = le_rating.transform(X[:,5])

            salary = regressor.predict(X)
            st.success(f"#### 💰 The estimated salary is ${round(salary[0]):,} /yr")
        except ValueError: 
            st.error(ValueError)

show_predict_page()

# Hide Left Menu
st.markdown("""<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)