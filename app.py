# Streamlit code for categorizing transaction descriptions with master file from Google Sheets

# ✅ Features:
# - Loads the master categorization file from Google Sheets (no local files needed)
# - Users only upload the statement file for processing
# - Outputs a categorized statement for download

# 🚀 How to Run:
# 1. Save this code in `app.py`.
# 2. Deploy it on Streamlit Cloud.
# 3. Users upload statements and get categorized outputs.

import streamlit as st
import pandas as pd
from io import BytesIO

# ✅ Google Sheets URL for the master categorization file
MASTER_SHEET_URL = "https://docs.google.com/spreadsheets/d/1d6uWrCQsuYmIjBet27cCb6BoIIafNwR2/export?format=xlsx"

@st.cache_data
def load_master_file():
    """Load the master categorization file from Google Sheets."""
    return pd.read_excel(MASTER_SHEET_URL)

# Function to categorize descriptions
def categorize_description(description, master_df):
    for _, row in master_df.iterrows():
        if pd.notnull(row['Key Word']) and row['Key Word'].lower() in str(description).lower():
            return row['Category']
    return 'Uncategorized'

# Function to apply categorization to the statement
def categorize_statement(statement_df, master_df):
    statement_df['Categorization'] = statement_df['Description'].apply(lambda x: categorize_description(x, master_df))
    return statement_df

# 🌐 Streamlit Interface
st.title("📄 Transaction Categorization Web App")
st.write("Upload your **statement file** to receive a categorized output. The master categorization data is loaded from a secure backend.")

# Statement file uploader
statement_file = st.file_uploader("Upload Statement File (Excel or CSV)", type=["xlsx", "csv"])

if statement_file:
    # Load the master categorization file
    master_df = load_master_file()

    # Read uploaded statement file
    try:
        statement_df = pd.read_excel(statement_file)
    except Exception:
        statement_df = pd.read_csv(statement_file)

    st.subheader("📂 Uploaded Statement Preview")
    st.dataframe(statement_df.head())

    # Categorize the statement
    categorized_df = categorize_statement(statement_df, master_df)

    st.success("✅ Categorization completed!")
    st.subheader("📝 Categorized Statement Preview")
    st.dataframe(categorized_df.head())

    # Download categorized file
    output = BytesIO()
    categorized_df.to_excel(output, index=False)
    output.seek(0)

    st.download_button(
        label="📥 Download Categorized Statement",
        data=output,
        file_name="Categorized_Statement.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("👆 Upload a statement file to begin.")
