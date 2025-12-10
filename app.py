import streamlit as st

st.set_page_config(page_title="Sales Agent Prototype", layout="wide")

st.title("Sales Agent Prototype")
st.header("Generate Account Insights")

# Create the sidebar for inputs
with st.sidebar:
    st.subheader("Input Data")
    
    # Required Inputs based on project instructions
    product_name = st.text_input("Product Name", placeholder="What are you selling?")
    company_url = st.text_input("Company URL", placeholder="https://target-company.com")
    product_category = st.text_input("Product Category", placeholder="e.g., Cloud Data Platform")
    competitors_url = st.text_input("Competitors URL", placeholder="https://competitor.com")
    value_proposition = st.text_input("Value Proposition", placeholder="One sentence summary")
    target_customer = st.text_input("Target Customer", placeholder="Name of person you are selling to")

    # Button to trigger the agent
    generate_btn = st.button("Generate Insights")