import streamlit as st
import joblib
import pandas as pd

# =========================================================
# LOAD MODELS
# =========================================================

linear_model = joblib.load("linear.sav")
logistic_model = joblib.load("logi.sav")


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ABC Ltd Telecom Decision Support",
    page_icon="📡",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

/* Main title */
.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #17365d !important;
    margin-bottom: 5px;
}

/* Subtitle */
.subtitle {
    font-size: 17px;
    color: #64748b !important;
    margin-bottom: 5px;
}

/* Developed by */
.developed-by {
    font-size: 15px;
    color: #64748b !important;
    margin-bottom: 12px;
}

/* User instruction */
.instruction {
    font-size: 15px;
    color: #64748b !important;
    margin-bottom: 30px;
}

/* Section headings */
.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #17365d !important;
    margin-bottom: 18px;
}

/* Input labels */
label {
    color: #17365d !important;
    font-weight: 600 !important;
}

[data-testid="stWidgetLabel"] p {
    color: #17365d !important;
    font-weight: 600 !important;
}

/* Normal text */
.stMarkdown p,
.stMarkdown span,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] span {
    color: #17365d !important;
}

/* Result title */
.result-title {
    color: #17365d !important;
    font-size: 18px;
    font-weight: 800;
}

/* Button */
div.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #4f46e5, #6366f1);
    color: white !important;
    font-size: 17px;
    font-weight: 700;
    border-radius: 12px;
    border: none;
    padding: 12px;
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b !important;
    font-size: 15px;
    margin-top: 45px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📡 ABC Ltd Telecom Decision Support</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Customer churn prediction & monthly charges estimation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="developed-by">Developed by Group 10</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="instruction">'
    'ⓘ Hover over the information icons for help with each field.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# TWO COLUMN LAYOUT
# =========================================================

left, right = st.columns([1, 1], gap="large")


# =========================================================
# LEFT SIDE - CUSTOMER INFORMATION
# =========================================================

with left:

    st.markdown(
        '<div class="section-title">👤 Customer Information</div>',
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # SENIOR CITIZEN + GENDER
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        senior_citizen = st.selectbox(
            "Senior Citizen ⓘ",
            ["No", "Yes"],
            help="Select Yes if the customer is a senior citizen."
        )

    with col2:

        gender = st.selectbox(
            "Gender ⓘ",
            ["Male", "Female"],
            help="Select the customer's gender."
        )


    # -----------------------------------------------------
    # TENURE + TOTAL CHARGES
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        tenure = st.number_input(
            "Tenure (months) ⓘ",
            min_value=0,
            max_value=100,
            value=24,
            help="Number of months the customer has been with the company."
        )

    with col2:

        total_charges = st.number_input(
            "Total Charges ($) ⓘ",
            min_value=0.0,
            value=1500.0,
            step=100.0,
            help="Total amount charged to the customer so far."
        )


    # -----------------------------------------------------
    # PARTNER + DEPENDENTS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        partner = st.selectbox(
            "Partner ⓘ",
            ["Yes", "No"],
            help="Select Yes if the customer has a partner or spouse."
        )

    with col2:

        dependents = st.selectbox(
            "Dependents ⓘ",
            ["Yes", "No"],
            help="Select Yes if the customer has dependents, such as children or other financially dependent people."
        )


    # -----------------------------------------------------
    # PHONE SERVICE + PAPERLESS BILLING
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        phone_service = st.selectbox(
            "Phone Service ⓘ",
            ["Yes", "No"],
            help="Select Yes if the customer has a phone service subscription."
        )

    with col2:

        paperless_billing = st.selectbox(
            "Paperless Billing ⓘ",
            ["Yes", "No"],
            help="Select Yes if the customer uses paperless billing instead of paper bills."
        )


    # -----------------------------------------------------
    # STREAMING TV + STREAMING MOVIES
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        streaming_tv = st.selectbox(
            "Streaming TV ⓘ",
            ["Yes", "No"],
            help="Select Yes if the customer subscribes to a streaming TV service."
        )

    with col2:

        streaming_movies = st.selectbox(
            "Streaming Movies ⓘ",
            ["Yes", "No"],
            help="Select Yes if the customer subscribes to a streaming movie service."
        )


    st.write("")


    # -----------------------------------------------------
    # ANALYZE BUTTON
    # -----------------------------------------------------

    predict_button = st.button(
        "🔍 Analyze Customer"
    )


# =========================================================
# RIGHT SIDE - PREDICTION RESULTS
# =========================================================

with right:

    st.markdown(
        '<div class="section-title">📊 Prediction Results</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # BEFORE ANALYSIS
    # =====================================================

    if not predict_button:

        st.info(
            "Enter customer information and click "
            "**Analyze Customer** to view predictions."
        )


    # =====================================================
    # AFTER ANALYSIS
    # =====================================================

    else:

        # -------------------------------------------------
        # CONVERT INPUTS TO MODEL FORMAT
        # -------------------------------------------------

        senior_citizen_value = (
            1 if senior_citizen == "Yes" else 0
        )

        gender_value = (
            1 if gender == "Male" else 0
        )

        partner_value = (
            1 if partner == "Yes" else 0
        )

        dependents_value = (
            1 if dependents == "Yes" else 0
        )

        phone_service_value = (
            1 if phone_service == "Yes" else 0
        )

        paperless_billing_value = (
            1 if paperless_billing == "Yes" else 0
        )

        streaming_tv_value = (
            1 if streaming_tv == "Yes" else 0
        )

        streaming_movies_value = (
            1 if streaming_movies == "Yes" else 0
        )


        # -------------------------------------------------
        # CREATE INPUT DATAFRAME
        # -------------------------------------------------

        input_data = pd.DataFrame([{

            "SeniorCitizen": senior_citizen_value,

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


        # =================================================
        # LOGISTIC REGRESSION - CHURN
        # =================================================

        churn_prediction = logistic_model.predict(
            input_data
        )

        churn_probability = logistic_model.predict_proba(
            input_data
        )


        # =================================================
        # CUSTOMER CHURN RESULT
        # =================================================

        with st.container(border=True):

            st.markdown(
                '<div class="result-title">CUSTOMER CHURN</div>',
                unsafe_allow_html=True
            )

            st.write("")


            if churn_prediction[0] == 1:

                st.error(
                    "❌ Customer Predicted to Churn"
                )

            else:

                st.success(
                    "✅ Customer Predicted to Stay"
                )


            st.markdown(
                f'<p style="color:#17365d !important; '
                f'font-size:16px;">'
                f'Probability of Staying: '
                f'<b>{churn_probability[0][0]:.2%}</b>'
                f'</p>',
                unsafe_allow_html=True
            )


            st.markdown(
                f'<p style="color:#17365d !important; '
                f'font-size:16px;">'
                f'Probability of Churning: '
                f'<b>{churn_probability[0][1]:.2%}</b>'
                f'</p>',
                unsafe_allow_html=True
            )


        # =================================================
        # LINEAR REGRESSION - MONTHLY CHARGES
        # =================================================

        monthly_charges = linear_model.predict(
            input_data
        )[0]


        # =================================================
        # MONTHLY CHARGES RESULT
        # =================================================

        with st.container(border=True):

            st.markdown(
                '<div class="result-title">'
                '💰 ESTIMATED MONTHLY CHARGES'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                f'<h1 style="color:#17365d !important; '
                f'font-size:40px;">'
                f'${monthly_charges:.2f}'
                f'</h1>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<p style="color:#17365d !important; '
                'font-size:16px;">'
                'Estimated monthly charges based on '
                'customer characteristics.'
                '</p>',
                unsafe_allow_html=True
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    '<b>Developed by Group 10</b>'
    '</div>',
    unsafe_allow_html=True
)
