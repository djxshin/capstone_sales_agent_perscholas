import streamlit as st
import google.generativeai as genai

# 1. Configure the API Key securely
# Streamlit automatically looks inside .streamlit/secrets.toml for this
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing Gemini API Key. Please add it to .streamlit/secrets.toml")

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

    # --- MAIN LOGIC BLOCK ---

# Use a placeholder to display the final output, allowing us to easily clear it later
output_placeholder = st.empty() 

def generate_sales_insights(product_name, company_url, product_category, competitors_url, value_prop, target_customer):
    """
    Sends a structured prompt to Gemini Pro to generate the one-pager content.
    """
    # 1. Select the Model (Gemini Pro)
    model = genai.GenerativeModel('gemini-pro')

    # 2. Construct the Prompt (The "Instructions" for the Agent)
    # We use f-strings to insert the user's data into the instructions.
    prompt = f"""
    You are an expert Sales Assistant Agent. Your goal is to help a sales rep sell "{product_name}" to the company at "{company_url}".
    
    Here is the context:
    - Product Category: {product_category}
    - Value Proposition: {value_prop}
    - Competitors URL: {competitors_url}
    - Target Customer: {target_customer}

    Please generate a professional "Account One-Pager" with the following 4 sections based on your knowledge of these companies. 
    If you cannot access real-time URL data, use your internal knowledge base to infer likely strategies based on the company's public profile.

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

    # 3. Generate Content
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating insights: {str(e)}"

if generate_btn:
    # 1. Check for required inputs (Company URL is the minimum)
    if not company_url:
        st.error("Please enter a **Company URL** to generate insights.")
    else:
        # 2. Display a 'Working' message while the agent is running
        with output_placeholder.container():
            st.info(f"Agent running... Gathering insights for **{company_url}** using product **{product_name}**.")
            
            # --- CALL THE FUNCTION ---
            # Call the function we defined above and save the result
            generated_output = generate_sales_insights(
                product_name, 
                company_url, 
                product_category, 
                competitors_url, 
                value_proposition, 
                target_customer
            )
            
            st.success("Insights Generated! See the one-pager below.")
            
            # --- DISPLAY THE AI OUTPUT ---
            st.markdown("---")
            st.subheader("🎯 Account One-Pager Summary")
            
            # Display the raw markdown response from Gemini
            st.markdown(generated_output)
            st.markdown("---")