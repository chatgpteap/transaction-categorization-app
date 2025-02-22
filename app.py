# Install Streamlit: pip install streamlit pandas openpyxl

import streamlit as st
import pandas as pd
from io import BytesIO

# ✅ Load the master file from a secure location (e.g., local server, AWS S3, or Streamlit's secrets)
# For this example, let's assume it's stored locally. In production, load it from cloud storage.
MASTER_FILE_PATH = "Master_Categorization_File.xlsx"

@st.cache_data
def load_master_file():
    return pd.read_excel(MASTER_FILE_PATH, engine='openpyxl')

# Categorize descriptions
def categorize_description(description, master_df):
    for _, row in master_df.iterrows():
        if pd.notnull(row['Key Word']) and row['Key Word'].lower() in str(description).lower():
            return row['Category']
    return 'Uncategorized'

def categorize_statement(statement_df, master_df):
    statement_df['Categorization'] = statement_df['Description'].apply(lambda x: categorize_description(x, master_df))
    return statement_df

# 🌐 Streamlit Interface
st.title("📄 Transaction Categorization Web App")
st.write("Upload your **statement file** to receive a categorized output.")

statement_file = st.file_uploader("Upload Statement File (Excel or CSV)", type=["xlsx", "csv"])

if statement_file:
    # Load master categorization file
    master_df = load_master_file()

    # Read statement file
    try:
        statement_df = pd.read_excel(statement_file, engine='openpyxl')
    except:
        statement_df = pd.read_csv(statement_file)

    # Show preview
    st.write("### 📂 Uploaded Statement Preview", statement_df.head())

    # Process and categorize
    categorized_df = categorize_statement(statement_df, master_df)

    # Show categorized data preview
    st.success("✅ Categorization completed!")
    st.write("### 📝 Categorized Statement Preview", categorized_df.head())

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
