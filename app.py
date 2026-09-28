import streamlit as st
import joblib
import pandas as pd

# Load models
linear_model = joblib.load('linear.sav')
logistic_model = joblib.load('logi.sav')

# Page title
st.title('📊 Telecom Customer Prediction App')
st.write('Enter customer details to predict churn and estimate monthly charges.')

# Customer inputs
senior_citizen = st.selectbox('Senior Citizen', [0, 1])
tenure = st.number_input('Tenure (months)', min_value=0, max_value=100, value=24)
total_charges = st.number_input('Total Charges ($)', min_value=0.0, value=1500.0)

gender = st.selectbox('Gender', ['Male', 'Female'])
partner = st.selectbox('Partner', ['Yes', 'No'])
dependents = st.selectbox('Dependents', ['Yes', 'No'])
phone_service = st.selectbox('Phone Service', ['Yes', 'No'])
paperless_billing = st.selectbox('Paperless Billing', ['Yes', 'No'])
streaming_tv = st.selectbox('Streaming TV', ['Yes', 'No'])
streaming_movies = st.selectbox('Streaming Movies', ['Yes', 'No'])

# Convert inputs to model format
gender_value = 1 if gender == 'Male' else 0

partner_value = 1 if partner == 'Yes' else 0
dependents_value = 1 if dependents == 'Yes' else 0
phone_service_value = 1 if phone_service == 'Yes' else 0
paperless_billing_value = 1 if paperless_billing == 'Yes' else 0
streaming_tv_value = 1 if streaming_tv == 'Yes' else 0
streaming_movies_value = 1 if streaming_movies == 'Yes' else 0

# Create input dataframe
input_data = pd.DataFrame([{
    'SeniorCitizen': senior_citizen,
    'tenure': tenure,
    'TotalCharges': total_charges,
    'gender': gender_value,
    'Partner': partner_value,
    'Dependents': dependents_value,
    'PhoneService': phone_service_value,
    'PaperlessBilling': paperless_billing_value,
    'StreamingTV': streaming_tv_value,
    'StreamingMovies': streaming_movies_value
}])

# Prediction button
if st.button('Predict Customer'):
    
    # Churn prediction
    churn_prediction = logistic_model.predict(input_data)
    churn_probability = logistic_model.predict_proba(input_data)

    st.subheader('📉 Customer Churn Prediction')

    if churn_prediction[0] == 1:
        st.error('The customer is predicted to CHURN.')
    else:
        st.success('The customer is predicted to STAY.')

    st.write(f'Probability of Staying: {churn_probability[0][0]:.2%}')
    st.write(f'Probability of Churning: {churn_probability[0][1]:.2%}')

    # Monthly charges prediction
    monthly_charges = linear_model.predict(input_data)[0]

    st.subheader('💰 Estimated Monthly Charges')
    st.success(f'Estimated Monthly Charges: ${monthly_charges:.2f} per month')
