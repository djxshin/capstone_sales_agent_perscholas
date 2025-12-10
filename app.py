import streamlit as st
import google.generativeai as genai

# 1. Configure the API Key
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing Gemini API Key. Please add it to .streamlit/secrets.toml")

st.set_page_config(page_title="Sales Agent Prototype", layout="wide")
st.title("Sales Agent Prototype")
st.header("Generate Account Insights")

# Sidebar for inputs
with st.sidebar:
    st.subheader("Input Data")
    product_name = st.text_input("Product Name", placeholder="What are you selling?")
    company_url = st.text_input("Company URL", placeholder="https://target-company.com")
    product_category = st.text_input("Product Category", placeholder="e.g., Cloud Data Platform")
    competitors_url = st.text_input("Competitors URL", placeholder="https://competitor.com")
    value_proposition = st.text_input("Value Proposition", placeholder="One sentence summary")
    target_customer = st.text_input("Target Customer", placeholder="Name of person you are selling to")
    generate_btn = st.button("Generate Insights")

# Placeholder for output
output_placeholder = st.empty() 

def generate_sales_insights(product_name, company_url, product_category, competitors_url, value_prop, target_customer):
    """
    Sends a structured prompt to Gemini to generate the one-pager content.
    """
    # --- CHANGE 1: Use the newer, correct model name ---
    model = genai.GenerativeModel('models/gemini-2.0-flash')

    prompt = f"""
    You are an expert Sales Assistant Agent. Your goal is to help a sales rep sell "{product_name}" to the company at "{company_url}".
    
    Here is the context:
    - Product Category: {product_category}
    - Value Proposition: {value_prop}
    - Competitors URL: {competitors_url}
    - Target Customer: {target_customer}

    Please generate a professional "Account One-Pager" with the following 4 sections based on your knowledge. 

    SECTION 1: Company Strategy
    Summarize the company's recent activities, strategy, and press releases relevant to {product_category}.

    SECTION 2: Competitor Mentions
    Analyze how they might interact with {competitors_url} or similar rivals.

    SECTION 3: Leadership Information
    Identify key leaders (C-suite, VPs) relevant to buying {product_category}.

    SECTION 4: Article Links
    List 2-3 relevant real or likely search terms for finding recent news.

    Keep the tone professional and concise.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating insights: {str(e)}"

# Main Logic
if generate_btn:
    if not company_url:
        st.error("Please enter a **Company URL** to generate insights.")
    else:
        with output_placeholder.container():
            st.info(f"Agent running... Gathering insights for **{company_url}**...")
            
            # --- CHANGE 2: Call the function ---
            generated_output = generate_sales_insights(
                product_name, company_url, product_category, 
                competitors_url, value_proposition, target_customer
            )
            
            st.success("Insights Generated! See the one-pager below.")
            
            # --- CHANGE 3: Display the REAL AI output ---
            st.markdown("---")
            st.subheader("🎯 Account One-Pager Summary")
            st.markdown(generated_output) # This replaces the static placeholders
            st.markdown("---")