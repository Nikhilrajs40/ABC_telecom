import streamlit as st
import joblib
import pandas as pd

# Load models
linear_model = joblib.load('linear.sav')
logistic_model = joblib.load('logi.sav')

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ABC Ltd Telecom Decision Support",
    page_icon="📡",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #17365d;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #64748b;
    margin-bottom: 30px;
}

.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #17365d;
    margin-bottom: 18px;
}

.result-card {
    background-color: white;
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.result-heading {
    font-size: 14px;
    font-weight: 700;
    color: #64748b;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.stay-text {
    color: #008a4b;
    font-size: 25px;
    font-weight: 800;
}

.churn-text {
    color: #d93025;
    font-size: 25px;
    font-weight: 800;
}

.charge-value {
    color: #17365d;
    font-size: 36px;
    font-weight: 800;
}

.probability {
    font-size: 16px;
    color: #64748b;
    margin-top: 12px;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 15px;
    margin-top: 45px;
    padding: 20px;
}

div.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #4f46e5, #6366f1);
    color: white;
    font-size: 17px;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    padding: 12px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">📡 ABC Ltd Telecom Decision Support</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Customer churn prediction & monthly charges estimation</div>',
    unsafe_allow_html=True
)


# ---------------- TWO COLUMNS ----------------
left, right = st.columns([1, 1], gap="large")


# =========================================================
# LEFT SIDE - CUSTOMER INFORMATION
# =========================================================

with left:

    st.markdown(
        '<div class="section-title">👤 Customer Information</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        senior_citizen = st.selectbox(
            "Senior Citizen",
            [0, 1]
        )

    with col2:
        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

    col1, col2 = st.columns(2)

    with col1:
        tenure = st.number_input(
            "Tenure (months)",
            min_value=0,
            max_value=100,
            value=24
        )

    with col2:
        total_charges = st.number_input(
            "Total Charges ($)",
            min_value=0.0,
            value=1500.0,
            step=100.0
        )

    col1, col2 = st.columns(2)

    with col1:
        partner = st.selectbox(
            "Partner",
            ["Yes", "No"]
        )

    with col2:
        dependents = st.selectbox(
            "Dependents",
            ["Yes", "No"]
        )

    col1, col2 = st.columns(2)

    with col1:
        phone_service = st.selectbox(
            "Phone Service",
            ["Yes", "No"]
        )

    with col2:
        paperless_billing = st.selectbox(
            "Paperless Billing",
            ["Yes", "No"]
        )

    col1, col2 = st.columns(2)

    with col1:
        streaming_tv = st.selectbox(
            "Streaming TV",
            ["Yes", "No"]
        )

    with col2:
        streaming_movies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No"]
        )

    st.write("")

    predict_button = st.button("🔍 Analyze Customer")


# =========================================================
# RIGHT SIDE - RESULTS
# =========================================================

with right:

    st.markdown(
        '<div class="section-title">📊 Prediction Results</div>',
        unsafe_allow_html=True
    )

    if predict_button:

        # Convert values exactly as used during model training
        gender_value = 1 if gender == "Male" else 0
        partner_value = 1 if partner == "Yes" else 0
        dependents_value = 1 if dependents == "Yes" else 0
        phone_service_value = 1 if phone_service == "Yes" else 0
        paperless_billing_value = 1 if paperless_billing == "Yes" else 0
        streaming_tv_value = 1 if streaming_tv == "Yes" else 0
        streaming_movies_value = 1 if streaming_movies == "Yes" else 0

        # Input dataframe
        input_data = pd.DataFrame([{
            "SeniorCitizen": senior_citizen,
            "tenure": tenure,
            "TotalCharges": total_charges,
            "gender": gender_value,
            "Partner": partner_value,
            "Dependents": dependents_value,
            "PhoneService": phone_service_value,
            "PaperlessBilling": paperless_billing_value,
            "StreamingTV": streaming_tv_value,
            "StreamingMovies": streaming_movies_value
        }])

        # ---------------- CHURN PREDICTION ----------------
        churn_prediction = logistic_model.predict(input_data)
        churn_probability = logistic_model.predict_proba(input_data)

        if churn_prediction[0] == 1:

            st.markdown("""
            <div class="result-card">
                <div class="result-heading">CUSTOMER CHURN</div>
                <div class="churn-text">❌ Customer Predicted to Churn</div>
                <br>
                <div class="probability">
                    Probability of Staying:
                    <b>{:.2%}</b>
                </div>
                <div class="probability">
                    Probability of Churning:
                    <b>{:.2%}</b>
                </div>
            </div>
            """.format(
                churn_probability[0][0],
                churn_probability[0][1]
            ), unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="result-card">
                <div class="result-heading">CUSTOMER CHURN</div>
                <div class="stay-text">✅ Customer Predicted to Stay</div>
                <br>
                <div class="probability">
                    Probability of Staying:
                    <b>{:.2%}</b>
                </div>
                <div class="probability">
                    Probability of Churning:
                    <b>{:.2%}</b>
                </div>
            </div>
            """.format(
                churn_probability[0][0],
                churn_probability[0][1]
            ), unsafe_allow_html=True)

        # ---------------- MONTHLY CHARGES ----------------
        monthly_charges = linear_model.predict(input_data)[0]

        st.markdown("""
        <div class="result-card">
            <div class="result-heading">💰 ESTIMATED MONTHLY CHARGES</div>
            <div class="charge-value">${:.2f}</div>
            <br>
            <div class="probability">
                Estimated monthly charges based on customer characteristics.
            </div>
        </div>
        """.format(monthly_charges), unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="result-card">
            <div class="result-heading">PREDICTION RESULTS</div>
            <div style="font-size:20px; color:#64748b;">
                Enter customer information and click
                <b>Analyze Customer</b> to view predictions.
            </div>
        </div>
        """, unsafe_allow_html=True)


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    <b>Managed by Group 10</b>
</div>
""", unsafe_allow_html=True)
