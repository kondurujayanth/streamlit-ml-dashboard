import streamlit as st
import requests
import pandas as pd
import numpy as np
import time

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="ML Prediction Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Theme toggle
# ---------------------------
theme = st.sidebar.selectbox("Select Theme", ["Light", "Dark"])
if theme == "Dark":
    bg_color = "#1e1e2f"
    text_color = "#f5f5f5"
    card_bg = "#2c2c3c"
    gradient = "linear-gradient(135deg, #667eea, #764ba2)"
else:
    bg_color = "#f5f7fa"
    text_color = "#0f111a"
    card_bg = "#ffffff"
    gradient = "linear-gradient(135deg, #4CAF50, #81C784)"

# ---------------------------
# Custom CSS
# ---------------------------
st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
    color: {text_color};
}}
h1 {{
    text-align: center;
    color: #1f77b4;
}}
.card {{
    background: {gradient};
    color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 2px 2px 20px rgba(0,0,0,0.3);
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    margin-top: 20px;
}}
.sidebar .sidebar-content {{
    background-color: #e0e6f2;
    padding: 20px;
    border-radius: 10px;
}}
button.css-1emrehy.edgvbvh3 {{
    background-color: #1f77b4 !important;
    color: white !important;
    font-weight: bold;
}}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar inputs
# ---------------------------
st.sidebar.header("Input Features")
st.sidebar.markdown("Adjust values for prediction:")

features = []
feature_names = ["Feature 1 (Age)", "Feature 2 (Hours)", "Feature 3 (Distance)",
                 "Feature 4 (Weight)", "Feature 5 (Volume)", "Feature 6 (Count)", "Feature 7 (Year)"]

default_values = [14.0, 8, 350, 165, 4209, 12, 1972]

for name, default in zip(feature_names, default_values):
    features.append(st.sidebar.number_input(name, value=default))

# ---------------------------
# Main page
# ---------------------------
st.markdown("<h1>🤖 ML Model Prediction Dashboard</h1>", unsafe_allow_html=True)
st.markdown("Enter feature values in the sidebar and click **Predict** to get the prediction.")

# ---------------------------
# Show inputs as metrics in columns
# ---------------------------
cols = st.columns(len(features))
for col, name, val in zip(cols, feature_names, features):
    col.metric(label=name.split("(")[0], value=val)

# ---------------------------
# Prediction button
# ---------------------------
if st.button("Predict"):
    data = {"features": features}
    url = "https://fastapi-ml-app-62il.onrender.com/predict"
    
    try:
        # Loading animation
        with st.spinner("Predicting..."):
            time.sleep(1)  # simulate delay
            response = requests.post(url, json=data)
            prediction = response.json()["prediction"]

        # Animated prediction display
        st.markdown(f'<div class="card">Prediction: {prediction}</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error: {e}")

# ---------------------------
# Feature overview chart
# ---------------------------
st.markdown("### 📊 Feature Values Overview")
df_features = pd.DataFrame({
    "Feature": [f"F{i+1}" for i in range(len(features))],
    "Value": features
})
st.bar_chart(df_features.set_index("Feature"))

# ---------------------------
# Optional: Feature contribution mockup (for aesthetics)
# ---------------------------
st.markdown("### ⚡ Feature Impact (Mockup)")
impact = np.random.randint(10, 100, size=len(features))
df_impact = pd.DataFrame({
    "Feature": [f"F{i+1}" for i in range(len(features))],
    "Impact": impact
})
st.bar_chart(df_impact.set_index("Feature"))
