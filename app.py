import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
from sklearn.preprocessing import LabelEncoder

st.set_page_config(
    page_title="AI Churn Dashboard",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0b1220, #0f172a);
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding: 2rem 2.5rem;
    border-radius: 16px;
    background: rgba(15, 23, 42, 0.55);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.title {
    font-size: 25px;
    font-weight: 500;
    text-align: center;
    color: white;
    margin-top: 35px;
    margin-bottom: 12px;
    letter-spacing: 1px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-top: 5px;
    font-size: 15px;
}

.card {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 18px;
}

.stTextInput input,
.stNumberInput input {
    background: #E5E7EB !important;
    color: #111827 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
    padding: 10px !important;
    font-weight: 600 !important;
}

div[data-baseweb="select"] > div {
    background: #E5E7EB !important;
    color: #111827 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 10px !important;
}

.stNumberInput input[type=number]::-webkit-outer-spin-button,
.stNumberInput input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

.stButton > button {
    background: #E34234 !important;
    color: white !important;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
    border: none;
    transition: 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(239, 68, 68, 0.35);
}

.stMarkdown,
.stText,
label {
    color: #cbd5e1 !important;
    font-size: 14px;
}

::placeholder {
    color: #64748b !important;
}

label {
    color: #cbd5e1 !important;
}

/* Slider numbers */
.stSlider span {
    color: #E34234 !important;
    font-weight: 600 !important;
}

.title {
    margin-bottom: 2px !important;
}

.subtitle {
    margin-top: 0px !important;
    line-height: 1.2;
}

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 1rem !important;
}

.element-container {
    margin-bottom: 6px !important;
}

.stMarkdown {
    margin-bottom: 4px !important;
}

h3 {
    margin-top: 8px !important;
    margin-bottom: 15px !important;
}
            
</style>
""", unsafe_allow_html=True)
st.markdown(
    "<div class='title'>AI-POWERED CUSTOMER CHURN PREDICTION</div>",
    unsafe_allow_html=True
)
st.markdown("<div class='subtitle'>Analyze churn risk and customer retention using machine learning</div>", unsafe_allow_html=True)

model = joblib.load("churn_model_streamlit.pkl")
encoders = joblib.load("encoders.pkl")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Customer Information")

    satisfaction = st.slider("Satisfaction Level", 1, 5, 3)
    age = st.slider("Age", 18, 80, 30)
    contract = st.selectbox("Plan Type", ["Month-to-Month", "One Year", "Two Year"])
    tenure = st.slider("Usage Duration (Months)", 0, 100, 12)

with col2:
    st.markdown("### Billing Information")

    monthly_charge = st.number_input("Monthly Bill (Units)", value=500.0)
    total_charges = st.number_input("Total Charges (Units)", value=1000.0)
    total_revenue = st.number_input("Total Revenue (Units)", value=1200.0)
    referrals = st.slider("Referrals Given", 0, 10, 0)
    long_distance = st.number_input("Extra Charges (Units)", value=0.0)

input_data = pd.DataFrame([[
    satisfaction,
    contract,
    monthly_charge,
    tenure,
    total_revenue,
    referrals,
    total_charges,
    long_distance,
    age
]], columns=[
    "Satisfaction Score",
    "Contract",
    "Monthly Charge",
    "Tenure in Months",
    "Total Revenue",
    "Number of Referrals",
    "Total Charges",
    "Total Long Distance Charges",
    "Age"
])
for col in input_data.columns:
    if col in encoders:
        input_data[col] = encoders[col].transform(input_data[col])

st.markdown("---")

if st.button("Predict Churn Risk"):

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)

    churn_prob = probability[0][1] * 100
    stay_prob = 100 - churn_prob

    st.markdown("### Live Prediction Analytics")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=["Churn Risk", "Retention"],
        y=[churn_prob, stay_prob],
        marker_color=["#ef4444", "#22c55e"],
        opacity=0.75
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=350
    )

    st.plotly_chart(fig, width="stretch")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric("Churn Risk", f"{churn_prob:.2f}%")
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.metric("Retention Chance", f"{stay_prob:.2f}%")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### AI Decision")

    if prediction[0] == 1:
        st.error("High Risk: Customer may leave soon")
    else:
        st.success("Low Risk: Customer will likely stay")