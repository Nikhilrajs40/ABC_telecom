import streamlit as st
import joblib
import pandas as pd
import json
from groq import Groq


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ABC Ltd Telecom Decision Support",
    page_icon="📡",
    layout="wide"
)


# =========================================================
# SAMPLE TEXT PAGE
# =========================================================

if st.query_params.get("sample") == "1":

    st.title("AI Natural Language Example")

    st.write(
        "Copy-paste this into the **AI Natural Language** box:"
    )

    st.markdown("""
The customer is a male and is not a senior citizen.

He has been with the company for 1 month.

He does not have a partner or dependents.

He does not have phone service.

He uses paperless billing.

He uses streaming TV and streaming movies.

His total charges so far are $29.85.
""")

    st.stop()


# =========================================================
# LOAD MODELS
# =========================================================

linear_model = joblib.load("linear.sav")
logistic_model = joblib.load("logi.sav")


# =========================================================
# GROQ CLIENT
# =========================================================

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ========================================================
   PAGE BACKGROUND
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
    color: #17365d !important;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #64748b !important;
    margin-bottom: 5px;
}

.developed-by {
    font-size: 15px;
    color: #64748b !important;
    margin-bottom: 10px;
}

.instruction {
    font-size: 15px;
    color: #64748b !important;
    margin-bottom: 20px;
}


/* ========================================================
   SECTION HEADINGS
======================================================== */

.section-title {
    font-size: 25px;
    font-weight: 750;
    color: #17365d !important;
    margin-bottom: 18px;
}


/* ========================================================
   CUSTOM INPUT LABEL
======================================================== */

.custom-label {
    color: #17365d !important;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 6px;
}


/* ========================================================
   INFORMATION ICON
======================================================== */

.info-icon {
    display: inline-block;
    margin-left: 4px;
    color: #17365d !important;
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
    color: #17365d !important;

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


/* Show tooltip only on hover */

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
   RADIO BUTTON TEXT
======================================================== */

div[data-testid="stRadio"] label p {
    color: #17365d !important;
    font-size: 16px !important;
    font-weight: 600 !important;
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
   RESULT TEXT
======================================================== */

.result-text {
    color: #17365d !important;
    font-size: 16px;
    line-height: 1.5;
}


/* ========================================================
   MONTHLY CHARGES VALUE
======================================================== */

.charge-value {
    color: #17365d !important;
    font-size: 42px !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
    margin-top: 15px !important;
    margin-bottom: 15px !important;
}


/* ========================================================
   MONTHLY CHARGES DESCRIPTION
======================================================== */

.charge-description {
    color: #17365d !important;
    font-size: 16px !important;
    line-height: 1.5 !important;
}


/* ========================================================
   ANALYZE BUTTON
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
    color: #64748b !important;
    font-size: 15px;
    margin-top: 45px;
    padding: 20px;
}

.footer a {
    color: #64748b !important;
    text-decoration: none !important;
    font-weight: bold;
    cursor: pointer;
}

.footer a:hover {
    color: #17365d !important;
    text-decoration: underline !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# FUNCTION FOR CUSTOM LABEL + TOOLTIP
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
# GROQ FUNCTION
# =========================================================

def extract_customer_data(customer_text):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": """
You extract telecom customer information from natural language.

Extract ONLY these 10 fields:

1. SeniorCitizen
2. tenure
3. TotalCharges
4. gender
5. Partner
6. Dependents
7. PhoneService
8. PaperlessBilling
9. StreamingTV
10. StreamingMovies

Rules:

- SeniorCitizen:
  1 if the customer is explicitly described as a senior citizen.
  0 if the customer is explicitly described as not a senior citizen.

- gender:
  1 for Male.
  0 for Female.

- Partner:
  1 for Yes.
  0 for No.

- Dependents:
  1 for Yes.
  0 for No.

- PhoneService:
  1 for Yes.
  0 for No.

- PaperlessBilling:
  1 for Yes.
  0 for No.

- StreamingTV:
  1 for Yes.
  0 for No.

- StreamingMovies:
  1 for Yes.
  0 for No.

- tenure:
  Number of months the customer has been with the company.

- TotalCharges:
  Total amount charged to the customer so far.

IMPORTANT:

- Do NOT guess missing information.
- If a required field is missing or unclear, return null.
- Do NOT infer SeniorCitizen from age.
- Do NOT create information that is not present in the customer's description.
- Return only the requested structured data.
"""
            },
            {
                "role": "user",
                "content": customer_text
            }
        ],

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "customer_information",
                "strict": True,
                "schema": {
                    "type": "object",

                    "properties": {

                        "SeniorCitizen": {
                            "type": ["integer", "null"]
                        },

                        "tenure": {
                            "type": ["integer", "null"]
                        },

                        "TotalCharges": {
                            "type": ["number", "null"]
                        },

                        "gender": {
                            "type": ["integer", "null"]
                        },

                        "Partner": {
                            "type": ["integer", "null"]
                        },

                        "Dependents": {
                            "type": ["integer", "null"]
                        },

                        "PhoneService": {
                            "type": ["integer", "null"]
                        },

                        "PaperlessBilling": {
                            "type": ["integer", "null"]
                        },

                        "StreamingTV": {
                            "type": ["integer", "null"]
                        },

                        "StreamingMovies": {
                            "type": ["integer", "null"]
                        }
                    },

                    "required": [
                        "SeniorCitizen",
                        "tenure",
                        "TotalCharges",
                        "gender",
                        "Partner",
                        "Dependents",
                        "PhoneService",
                        "PaperlessBilling",
                        "StreamingTV",
                        "StreamingMovies"
                    ],

                    "additionalProperties": False
                }
            }
        }
    )

    return json.loads(
        response.choices[0].message.content
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


# =========================================================
# INPUT METHOD
# =========================================================

st.markdown(
    '<div class="section-title">'
    'Choose Input Method'
    '</div>',
    unsafe_allow_html=True
)

input_method = st.radio(
    "Choose how to enter customer information:",
    ["Manual Input", "AI Natural Language"],
    horizontal=True
)

st.write("")


# =========================================================
# MANUAL INPUT
# =========================================================

if input_method == "Manual Input":

    st.markdown(
        '<div class="instruction">'
        'Hover over the ⓘ icons for help with each field.'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # TWO COLUMN LAYOUT
    # =====================================================

    left, right = st.columns(
        [1, 1],
        gap="large"
    )


    # =====================================================
    # LEFT SIDE - CUSTOMER INFORMATION
    # =====================================================

    with left:

        st.markdown(
            '<div class="section-title">'
            '👤 Customer Information'
            '</div>',
            unsafe_allow_html=True
        )


        # =================================================
        # SENIOR CITIZEN + GENDER
        # =================================================

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


        # =================================================
        # TENURE + TOTAL CHARGES
        # =================================================

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


        # =================================================
        # PARTNER + DEPENDENTS
        # =================================================

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


        # =================================================
        # PHONE SERVICE + PAPERLESS BILLING
        # =================================================

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


        # =================================================
        # STREAMING TV + STREAMING MOVIES
        # =================================================

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


        # =================================================
        # ANALYZE BUTTON
        # =================================================

        predict_button = st.button(
            "🔍 Analyze Customer"
        )


    # =====================================================
    # RIGHT SIDE - PREDICTION RESULTS
    # =====================================================

    with right:

        st.markdown(
            '<div class="section-title">'
            '📊 Prediction Results'
            '</div>',
            unsafe_allow_html=True
        )


        if not predict_button:

            st.info(
                "Enter customer information and click "
                "**Analyze Customer** to view predictions."
            )

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
            # LOGISTIC REGRESSION
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
            # LINEAR REGRESSION
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
                    <div class="charge-value">
                        ${monthly_charges:.2f}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    '<div class="charge-description">'
                    'Estimated monthly charges based on '
                    'customer characteristics.'
                    '</div>',
                    unsafe_allow_html=True
                )


# =========================================================
# AI NATURAL LANGUAGE INPUT
# =========================================================

else:

    st.markdown(
        '<div class="instruction">'
        'Describe the customer in normal language. '
        'The AI will extract the required information automatically.'
        '</div>',
        unsafe_allow_html=True
    )


    left, right = st.columns(
        [1, 1],
        gap="large"
    )


    # =====================================================
    # LEFT SIDE - AI INPUT
    # =====================================================

    with left:

        st.markdown(
            '<div class="section-title">'
            '🤖 Describe the Customer'
            '</div>',
            unsafe_allow_html=True
        )


        customer_text = st.text_area(
            "Customer Information",
            height=250,
            placeholder="""Example:

The customer is a male and is not a senior citizen.
He has been with the company for 24 months.
He has a partner and dependents.
He has phone service and paperless billing.
He uses streaming TV but not streaming movies.
His total charges so far are $1500."""
        )


        st.write("")


        ai_button = st.button(
            "🤖 Analyze with AI"
        )


    # =====================================================
    # RIGHT SIDE - AI RESULTS
    # =====================================================

    with right:

        st.markdown(
            '<div class="section-title">'
            '📊 Prediction Results'
            '</div>',
            unsafe_allow_html=True
        )


        if not ai_button:

            st.info(
                "Describe the customer and click "
                "**Analyze with AI** to extract information "
                "and generate predictions."
            )

        else:

            if customer_text.strip() == "":

                st.warning(
                    "Please enter customer information."
                )

            else:

                try:

                    # =================================================
                    # GROQ EXTRACTION
                    # =================================================

                    with st.spinner(
                        "🤖 AI is extracting customer information..."
                    ):

                        customer_data = extract_customer_data(
                            customer_text
                        )


                    # =================================================
                    # CHECK FOR MISSING INFORMATION
                    # =================================================

                    missing_fields = [
                        key
                        for key, value in customer_data.items()
                        if value is None
                    ]


                    if missing_fields:

                        st.warning(
                            "Some information is missing or unclear."
                        )

                        st.write(
                            "Please provide the following details:"
                        )

                        for field in missing_fields:

                            st.write(
                                f"• {field}"
                            )


                    else:

                        # =================================================
                        # SHOW EXTRACTED INFORMATION
                        # =================================================

                        st.markdown(
                            '<div class="result-title">'
                            '🔎 INFORMATION EXTRACTED BY AI'
                            '</div>',
                            unsafe_allow_html=True
                        )


                        display_data = pd.DataFrame(
                            [customer_data]
                        ).T

                        display_data.columns = ["Value"]


                        st.dataframe(
                            display_data,
                            use_container_width=True
                        )


                        # =================================================
                        # CREATE MODEL INPUT
                        # =================================================

                        input_data = pd.DataFrame([{

                            "SeniorCitizen":
                                customer_data["SeniorCitizen"],

                            "tenure":
                                customer_data["tenure"],

                            "TotalCharges":
                                customer_data["TotalCharges"],

                            "gender":
                                customer_data["gender"],

                            "Partner":
                                customer_data["Partner"],

                            "Dependents":
                                customer_data["Dependents"],

                            "PhoneService":
                                customer_data["PhoneService"],

                            "PaperlessBilling":
                                customer_data["PaperlessBilling"],

                            "StreamingTV":
                                customer_data["StreamingTV"],

                            "StreamingMovies":
                                customer_data["StreamingMovies"]

                        }])


                        # =================================================
                        # LOGISTIC REGRESSION
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
                        # LINEAR REGRESSION
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
                                <div class="charge-value">
                                    ${monthly_charges:.2f}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )


                            st.markdown(
                                '<div class="charge-description">'
                                'Estimated monthly charges based on '
                                'customer characteristics.'
                                '</div>',
                                unsafe_allow_html=True
                            )


                except Exception as e:

                    st.error(
                        "Something went wrong while processing "
                        "the customer information."
                    )

                    st.write(
                        "Please check your input and try again."
                    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        <a
            href="https://abctelecomindustry.streamlit.app/?sample=1"
            target="_blank"
            style="
                color:#64748b;
                text-decoration:none;
                font-weight:bold;
                cursor:pointer;
            "
        >
            Developed by Group 10
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
