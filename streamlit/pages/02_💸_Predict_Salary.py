import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Predict Salary", page_icon='💸')

def load_model():
    with open('../models/model_salary_pred.pkl', 'rb') as file:
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

def show_predict_page():

    st.subheader("💸 Data Engineer's Salary Prediction")

    st.write("""#### We need some informations to predict your salary :""")

    states = ('Remote', 'CA', 'GA', 'TX', 'NJ', 'DC', 'VA', 'MN', 'WI', 'IL', 'MS', 'MD', 'NY', 'MA', 'OR', 'UT', 'FL', 'OH', 'PA')

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

    company_rating = st.slider("Company Rating (According to Glassdoor) :", 0.0, 5.0, step=0.1)

    seniority_pos = st.checkbox("Senior Position")

    if seniority_pos:
        seniority = "senior"
    else:
        seniority = "na"

    submit = st.button("Calculate Salary")

    if submit:
        X = np.array([[state, seniority, education.lower(), experience, industry, company_rating]])
        X[:, 0] = le_state.transform(X[:,0])
        X[:, 1] = le_sen.transform(X[:,1])
        X[:, 2] = le_edu.transform(X[:,2])
        X[:, 3] = le_exp.transform(X[:,3])
        X[:, 4] = le_indu.transform(X[:,4])
        X[:, 5] = le_rating.transform(X[:,5])

        salary = regressor.predict(X)
        st.subheader(f'The estimated salary is ${salary[0]:.2f}')

show_predict_page()

# Hide Left Menu
st.markdown("""<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)