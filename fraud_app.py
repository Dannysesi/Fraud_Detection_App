import streamlit as st
import pickle
import pandas as pd

# Load the model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Prediction function
def make_prediction(transaction_amount, merchant_category, user_country, transaction_country, device_type, transaction_day, user_avg_spend, user_transaction_frequency):
    data = {
        'Transaction_Amount': transaction_amount,
        'Merchant_Category': merchant_category,
        'User_Country': user_country,
        'Transaction_Country': transaction_country,
        'Device_Type': device_type,
        'Transaction_Day': transaction_day,
        'User_Avg_Spend': user_avg_spend,
        'User_Transaction_Frequency': user_transaction_frequency
    }
    df = pd.DataFrame(data, index=[0])
    prediction = model.predict(df)
    if prediction == 1:
        return f"**Prediction:** Based on your input, this transaction is flagged as **fraudulent**. (Please investigate further or take appropriate action.)"
    else:
        return f"**Prediction:** Based on your input, this transaction is **not fraudulent**. (It appears to be legitimate, but routine monitoring is recommended.)"

# App layout
st.title("Fraud Detection App")
st.subheader("Enter your transaction details to check the likelihood of fraud.")

# First row: Transaction Amount and User Average Spend
col1, col2 = st.columns(2)
with col1:
    transaction_amount = st.number_input("Enter Transaction Amount", min_value=3000, max_value=30000, key="transaction_amount")
with col2:
    user_avg_spend = st.number_input("Enter User Average Spend", min_value=3000, max_value=30000, key="user_avg_spend")

# Second row: Merchant Category and User Country
col3, col4 = st.columns(2)
merchant_category_map = {
    'Adult websites': 0, 'Airlines': 1, 'Bakeries': 2, 'Bitcoin exchanges': 3, 
    'Clothing stores': 4, 'Department stores': 5, 'Grocery stores': 6, 
    'Hotels': 7, 'Liquor stores': 8, 'Taxi services': 9
}
with col3:
    merchant_word = st.selectbox("Merchant Category:", list(merchant_category_map.keys()))
    merchant_category = merchant_category_map[merchant_word]

user_country_map = {
    'America': 0, 'Argentina': 1, 'Australia': 2, 'Brazil': 3, 'Canada': 4,
    'China': 5, 'France': 6, 'Germany': 7, 'India': 8, 'Italy': 9,
    'Japan': 10, 'Kenya': 11, 'Mexico': 12, 'Nigeria': 13, 'Russia': 14,
    'South Africa': 15, 'South Korea': 16, 'Spain': 17, 'United Kingdom': 18
}
with col4:
    user_country_word = st.selectbox("User Country:", list(user_country_map.keys()))
    user_country = user_country_map[user_country_word]

# Third row: Transaction Country, Device Type, and Transaction Day
col5, col6, col7 = st.columns(3)
transaction_country_map = {
    'America': 0, 'Argentina': 1, 'Australia': 2, 'Brazil': 3, 'Canada': 4,
    'China': 5, 'France': 6, 'Germany': 7, 'India': 8, 'Indonesia': 9,
    'Italy': 10, 'Japan': 11, 'Kenya': 12, 'Mexico': 13, 'Nigeria': 14,
    'Pakistan': 15, 'Philippines': 16, 'Russia': 17, 'South Africa': 18,
    'South Korea': 19, 'Spain': 20, 'United Kingdom': 21, 'Vietnam': 22
}
with col5:
    transaction_country_word = st.selectbox("Transaction Country:", list(transaction_country_map.keys()))
    transaction_country = transaction_country_map[transaction_country_word]

device_type_map = {'Laptop': 0, 'Mobile': 1, 'Tablet': 2}
with col6:
    device_type_word = st.selectbox("Device Type:", list(device_type_map.keys()))
    device_type = device_type_map[device_type_word]

transaction_day_map = {'Weekday': 0, 'Weekend': 1}
with col7:
    transaction_day_word = st.selectbox("Transaction Day:", list(transaction_day_map.keys()))
    transaction_day = transaction_day_map[transaction_day_word]

# Fourth row: User Transaction Frequency
user_transaction_frequency = st.number_input(
    'Enter User Avg Transaction Frequency Per Day', 
    min_value=1, 
    max_value=10, 
    key="user_transaction_frequency"
)

# Predict button with clear instructions
if st.button("Check Fraud Status"):
    prediction_message = make_prediction(
        transaction_amount, merchant_category, user_country, transaction_country, 
        device_type, transaction_day, user_avg_spend, user_transaction_frequency
    )
    st.subheader(prediction_message)

st.write('----')
# Disclaimer and additional information
st.write("**Disclaimer:** This app is for informational purposes only and does not guarantee the accuracy of fraud detection. Please verify flagged transactions and consult with relevant authorities or fraud prevention professionals for further investigation.")
st.write("**Additional Information:**")
st.write("- Learn more about fraud prevention and detection strategies at the Federal Trade Commission (FTC): [https://www.consumer.ftc.gov](https://www.consumer.ftc.gov)")
