import streamlit as st
import pandas as pd

def clean_category_input(category):
    cat_map = {
        "GEN": "OPEN",
        "OBC": "OBC-NCL",
        "EWS": "EWS",
        "SC": "SC",
        "ST": "ST",
        "GENPWD": "OPEN (PwD)",
        "OBCPWD": "OBC-NCL (PwD)",
        "SC-PWD": "SC (PwD)",
        "ST-PWD": "ST (PwD)",
    }
    return cat_map.get(category.upper(), category.upper())

# Load data
df = pd.read_csv("JOSAA - NIT+System R5 Cut-Off - WE WON ACADEMY 2024 - GEN-Both.csv")

# Title
st.title("🎓 College Recommender - JOSAA Counselling")

# Sidebar Inputs
st.sidebar.header("Enter Your Details")
category_rank = st.sidebar.number_input("Your Category Rank", min_value=1)
category_input = st.sidebar.text_input("Category (GEN, OBC, SC, ST, etc.)", value="GEN")
quota_input = st.sidebar.selectbox("Quota", ["HS", "OS"])
num_results = st.sidebar.slider("Number of Colleges to Show (each list)", 1, 10, 4)
buffer_range = st.sidebar.number_input("Buffer for High Chance Colleges (Above Rank)", value=1000)

# Processed Category
category = clean_category_input(category_input)

# Filter dataset
filtered_df = df[
    (df['Seat Type'].str.upper() == category.upper()) &
    (df['Quota'].str.upper() == quota_input.upper())
].copy()

# Sort by Closing Rank
filtered_df.sort_values(by='Closing Rank', inplace=True)

# Sure Shot Colleges
sure_shots = filtered_df[filtered_df['Closing Rank'] >= category_rank].head(num_results)

# High Chance Colleges (just above your rank)
high_chances = filtered_df[
    (filtered_df['Closing Rank'] < category_rank) &
    (filtered_df['Closing Rank'] >= category_rank - buffer_range)
].tail(num_results)

# Display Results
st.subheader("✅ Sure Shot Colleges")
st.dataframe(sure_shots[['Institute', 'Academic Program Name', 'Closing Rank']])

st.subheader("⚠️ High Chance Colleges")
st.dataframe(high_chances[['Institute', 'Academic Program Name', 'Closing Rank']])

# Info
st.info("Tip: Increase buffer range if no high chance colleges are shown.")
