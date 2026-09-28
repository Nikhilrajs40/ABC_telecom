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

/* ========================================================
   BACKGROUND
======================================================== */

.stApp {
    background-color: #f5f7fb;
}


/* ========================================================
   HEADER
======================================================== */

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #17365d;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #64748b;
    margin-bottom: 5px;
}

.developed-by {
    font-size: 15px;
    color: #64748b;
    margin-bottom: 10px;
}

.instruction {
    font-size: 15px;
    color: #64748b;
    margin-bottom: 30px;
}


/* ========================================================
   SECTION HEADINGS
======================================================== */

.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #17365d;
    margin-bottom: 18px;
}


/* ========================================================
   CUSTOM INPUT LABEL
======================================================== */

.custom-label {
    color: #17365d;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 6px;
}

.info-icon {
    display: inline-block;
    margin-left: 4px;
    color: #17365d;
    font-size: 14px;
    font-weight: 700;
    cursor: help;
    position: relative;
}


/* ========================================================
   TOOLTIP
======================================================== */

.info-icon .tooltip-text {
    visibility: hidden;
    opacity: 0;

    position: absolute;
    z-index: 9999;

    width: 280px;

    background-color: #ffffff;
    color: #17365d;

    border: 1px solid #cbd5e1;
    border-radius: 8px;

    padding: 10px 12px;

    font-size: 13px;
    font-weight: 400;
    line-height: 1.4;

    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.18);

    left: 20px;
    top: -5px;

    transition: opacity 0.15s ease;
}


/* Show tooltip only when mouse is over icon */
.info-icon:hover .tooltip-text {
    visibility: visible;
    opacity: 1;
}


/* ========================================================
   HIDE STREAMLIT DEFAULT LABEL
======================================================== */

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    display: none !important;
}


/* ========================================================
   RESULT TITLE
======================================================== */

.result-title {
    color: #17365d !important;
    font-size: 18px;
    font-weight: 800;
}


/* ========================================================
   NORMAL TEXT
======================================================== */

.result-text {
    color: #17365d !important;
    font-size: 16px;
}


/* ========================================================
   BUTTON
======================================================== */

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


/* ========================================================
   FOOTER
======================================================== */

.footer {
    text-align: center;
    color: #64748b;
    font-size: 15px;
    margin-top: 45px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTION FOR LABEL + TOOLTIP
# =========================================================

def show_label(label, explanation):

    st.markdown(
        f"""
        <div class="custom-label">
            {label}
            <span class="info-icon">
                ⓘ
                <span class="tooltip-text">
                    {explanation}
                </span>
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">'
    '📡 ABC Ltd Telecom Decision Support'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Customer churn prediction & monthly charges estimation'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="developed-by">'
    'Developed by Group 10'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="instruction">'
    'Hover over the ⓘ icons for help with each field.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# TWO COLUMN LAYOUT
# =========================================================

left, right = st.columns(
    [1, 1],
    gap="large"
)


# =========================================================
# LEFT SIDE - CUSTOMER INFORMATION
# =========================================================

with left:

    st.markdown(
        '<div class="section-title">'
        '👤 Customer Information'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # SENIOR CITIZEN + GENDER
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        show_label(
            "Senior Citizen",
            "Select Yes if the customer is a senior citizen."
        )

        senior_citizen = st.selectbox(
            "Senior Citizen",
            ["No", "Yes"],
            label_visibility="collapsed"
        )


    with col2:

        show_label(
            "Gender",
            "Select the customer's gender."
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"],
            label_visibility="collapsed"
        )


    # =====================================================
    # TENURE + TOTAL CHARGES
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        show_label(
            "Tenure (months)",
            "Number of months the customer has been with the company."
        )

        tenure = st.number_input(
            "Tenure",
            min_value=0,
            max_value=100,
            value=24,
            label_visibility="collapsed"
        )


    with col2:

        show_label(
            "Total Charges ($)",
            "Total amount charged to the customer so far."
        )

        total_charges = st.number_input(
            "Total Charges",
            min_value=0.0,
            value=1500.0,
            step=100.0,
            label_visibility="collapsed"
        )


    # =====================================================
    # PARTNER + DEPENDENTS
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        show_label(
            "Partner",
            "Select Yes if the customer has a partner or spouse."
        )

        partner = st.selectbox(
            "Partner",
            ["Yes", "No"],
            label_visibility="collapsed"
        )


    with col2:

        show_label(
            "Dependents",
            "Select Yes if the customer has dependents, such as children or other financially dependent people."
        )

        dependents = st.selectbox(
            "Dependents",
            ["Yes", "No"],
            label_visibility="collapsed"
        )


    # =====================================================
    # PHONE SERVICE + PAPERLESS BILLING
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        show_label(
            "Phone Service",
            "Select Yes if the customer has a phone service subscription."
        )

        phone_service = st.selectbox(
            "Phone Service",
            ["Yes", "No"],
            label_visibility="collapsed"
        )


    with col2:

        show_label(
            "Paperless Billing",
            "Select Yes if the customer uses paperless billing instead of paper bills."
        )

        paperless_billing = st.selectbox(
            "Paperless Billing",
            ["Yes", "No"],
            label_visibility="collapsed"
        )


    # =====================================================
    # STREAMING TV + STREAMING MOVIES
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        show_label(
            "Streaming TV",
            "Select Yes if the customer subscribes to a streaming TV service."
        )

        streaming_tv = st.selectbox(
            "Streaming TV",
            ["Yes", "No"],
            label_visibility="collapsed"
        )


    with col2:

        show_label(
            "Streaming Movies",
            "Select Yes if the customer subscribes to a streaming movie service."
        )

        streaming_movies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No"],
            label_visibility="collapsed"
        )


    st.write("")


    # =====================================================
    # ANALYZE BUTTON
    # =====================================================

    predict_button = st.button(
        "🔍 Analyze Customer"
    )


# =========================================================
# RIGHT SIDE - PREDICTION RESULTS
# =========================================================

with right:

    st.markdown(
        '<div class="section-title">'
        '📊 Prediction Results'
        '</div>',
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

        # =================================================
        # CONVERT INPUTS TO MODEL FORMAT
        # =================================================

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


        # =================================================
        # CREATE INPUT DATAFRAME
        # =================================================

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
        # LOGISTIC REGRESSION - CHURN PREDICTION
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
                '<div class="result-title">'
                'CUSTOMER CHURN'
                '</div>',
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
                f"""
                <div class="result-text">
                    Probability of Staying:
                    <b>{churn_probability[0][0]:.2%}</b>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            st.markdown(
                f"""
                <div class="result-text">
                    Probability of Churning:
                    <b>{churn_probability[0][1]:.2%}</b>
                </div>
                """,
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
                f"""
                <h1 style="
                    color:#17365d !important;
                    font-size:40px;
                    margin-bottom:10px;
                ">
                    ${monthly_charges:.2f}
                </h1>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="result-text">
                    Estimated monthly charges based on
                    customer characteristics.
                </div>
                """,
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
