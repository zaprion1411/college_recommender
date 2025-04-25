import streamlit as st
import pandas as pd

# === CATEGORY AND GENDER TO SHEET NAME MAPPING ===
def get_sheet_name(category, gender):
    cat_map = {
        "GEN": "GEN",
        "OBC": "OBC",
        "EWS": "EWS",
        "SC": "SC",
        "ST": "ST"
    }
    gen_suffix = "Both" if gender.lower() == "male" else "Female"
    return f"{cat_map.get(category.upper(), category.upper())}_{gen_suffix}"

# === LOAD DATA ===
def load_data(sheet_name):
    xls = pd.ExcelFile("JOSAA - NIT+System R5 Cut-Off - WE WON ACADEMY 2024.xlsx")
    if sheet_name not in xls.sheet_names:
        st.error(f"Sheet '{sheet_name}' not found in the file.")
        return pd.DataFrame()
    df = pd.read_excel(xls, sheet_name=sheet_name)
    return df

# === STREAMLIT APP ===
st.title("🎓 College Recommender - JOSAA Counselling")

st.sidebar.header("Enter Your Details")
category_rank = st.sidebar.number_input("Your Category Rank", min_value=1)
category_input = st.sidebar.selectbox("Category", ["GEN", "OBC", "EWS", "SC", "ST"])
gender_input = st.sidebar.selectbox("Gender", ["Male", "Female"])
quota_input = st.sidebar.selectbox("Quota", ["HS", "OS"])
num_results = st.sidebar.slider("Number of Colleges to Show (each list)", 1, 10, 4)
buffer_range = st.sidebar.number_input("Buffer for High Chance Colleges (Above Rank)", value=1000)

sheet_name = get_sheet_name(category_input, gender_input)
df = load_data(sheet_name)

if not df.empty:
    # Filter dataset
    filtered_df = df[
        (df['Seat Type'].str.upper() == category_input.upper()) &
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

    st.info("Tip: Increase buffer range if no high chance colleges are shown.")
else:
    st.warning("Data could not be loaded. Please check your inputs or data file.")

