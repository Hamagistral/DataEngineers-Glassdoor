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

unique_company_ratings = [4.7, 4.4, 4.2, 5. , 2.7, 3.8, 4.8, 4.1, 1. , 3.1, 3.5, 4. , 4.5, 3.9, 4.3, 3.2, 2.6, 3.6, 4.9, 2.8, 4.6, 3.7, 3.4, 3. , 3.3, 2. , 2.9, 2.5, 2.3, 2.2, 1.3, 1.8]

def show_predict_page():

    st.write("## 💸 Data Engineer Salary Prediction 💹")

    st.write("""#### We need some information to predict your likely salary:""")

    states = ('Remote',
            'TX, Texas',
            'CA, California',
            'VA, Virginia',
            'MA, Massachusetts',
            'GA, Georgia',
            'NJ, New Jersey',
            'IL, Illinois',
            'NY, New York',
            'DC, District of Columbia',
            'OH, Ohio',
            'FL, Florida',
            'NC, North Carolina',
            'PA, Pennsylvania',
            'WA, Washington',
            'MN, Minnesota',
            'CO, Colorado',
            'MD, Maryland',
            'OR, Oregon',
            'UT, Utah',
            'WI, Wisconsin',
            'AZ, Arizona',
            'MO, Missouri',
            'TN, Tennessee',
            'CT, Connecticut',
            'MI, Michigan',
            'DE, Delaware',
            'IN, Indiana',
            'NV, Nevada')

    degrees = ('Bachelor', 'Master')

    experience_years = ('0-2 years', '2-5 years', '5-10 years', '+10 years')

    industries = ('Information Technology Support Services',
       'Biotech & Pharmaceuticals', 'Computer Hardware Development',
       'Health Care Services & Hospitals', 'Internet & Web Services',
       'HR Consulting', 'Consumer Product Manufacturing',
       'Investment & Asset Management', 'Accounting & Tax',
       'Business Consulting', 'Enterprise Software & Network Solutions',
       'Financial Transaction Processing', 'Staffing & Subcontracting',
       'Banking & Lending', 'Travel Agencies',
       'Airlines, Airports & Air Transportation', 'Sports & Recreation',
       'National Agencies', 'Aerospace & Defense', 'Software Development',
       'Beauty & Wellness', 'Publishing', 'Food & Beverage Manufacturing',
       'Energy & Utilities', 'Advertising & Public Relations',
       'Wholesale', 'Department, Clothing & Shoe Stores',
       'Machinery Manufacturing', 'Crop Production',
       'Colleges & Universities', 'Research & Development',
       'Pet & Pet Supplies Stores', 'Real Estate', 'Taxi & Car Services',
       'Education & Training Services', 'Mining & Metals',
       'Transportation Equipment Manufacturing',
       'Catering & Food Service Contractors', 'Membership Organizations',
       'Restaurants & Cafes', 'Vehicle Dealers', 'Grocery Stores',
       'Insurance Agencies & Brokerages', 'Gambling',
       'Insurance Carriers', 'State & Regional Agencies',
       'Civic & Social Services', 'Gift, Novelty & Souvenir Stores',
       'Broadcast Media', 'Cable, Internet & Telephone Providers',
       'Shipping & Trucking', 'Architectural & Engineering Services',
       'Telecommunications Services', 'Security & Protective',
       'Medical Testing & Clinical Laboratories',
       'Laundry & Dry Cleaning', 'Electronics Manufacturing',
       'Chemical Manufacturing', 'Farm Support', 'Biotechnology', 'Legal',
       'Culture & Entertainment', 'Film Production', 'Construction',
       'Hotels & Resorts', 'Other Retail Stores',
       'Commercial Equipment Services',
       'Grantmaking & Charitable Foundations',
       'General Merchandise & Superstores', 'Municipal Agencies',
       'Primary & Secondary Schools', 'Religious Institutions',
       'Health Care Products Manufacturing', 'Drug & Health Stores',
       'Hospitals & Health Clinics', 'Building & Personnel Services',
       'Consumer Product Rental')

    state =  st.selectbox("State :", states)

    def get_short_name(state_value):
        if state_value == 'Remote':
            return 'Remote'
        else:
            return state_value.split(', ')[0]

    state = get_short_name(state)

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
            X = np.array([[state, seniority, education.lower(), experience, industry, float(company_rating)]])
            X[:, 0] = le_state.transform(X[:,0])
            X[:, 1] = le_sen.transform(X[:,1])
            X[:, 2] = le_edu.transform(X[:,2])
            X[:, 3] = le_exp.transform(X[:,3])
            X[:, 4] = le_indu.transform(X[:,4])
            X[:, 5] = le_rating.transform(X[:,5])

            salary = regressor.predict(X)
            st.success(f"### 💰 The estimated salary is ${round(salary[0]):,} /yr")
        except ValueError: 
            st.error("There was an error while trying to predict your salary. Please try with other options.")

show_predict_page()

# Hide Left Menu
st.markdown("""<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)