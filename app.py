import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# --- 1. CONFIGURATION AND API SETUP ---
# Configure the LLM access using the secure key from secrets.toml
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing Gemini API Key. Please add it to .streamlit/secrets.toml")

st.set_page_config(page_title="Sales Agent Prototype", layout="wide")
st.title("Sales Agent Prototype")
st.header("Generate Account Insights")


# --- 2. WEB SCRAPING FUNCTION ---
def get_website_content(url):
    """
    Fetches and cleans text content from a given URL to be used as context for the LLM.
    """
    if not url:
        return ""
    
    try:
        # Pretend to be a browser (User-Agent) to avoid getting blocked by website security
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Fetch the page content with a 10-second timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Check for HTTP errors (like 404 or 500)
        
        # Parse the HTML to extract text
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text only from paragraph and header tags (where the content lives)
        text_content = ""
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3']): 
            text_content += tag.get_text() + " "
            
        # Limit text to 4000 characters to prevent overloading the LLM context window
        return text_content[:4000]
        
    except Exception as e:
        # If scraping fails, return empty string so the Agent can fall back to internal knowledge
        return ""


# --- 3. SALES AGENT FUNCTION ---
def generate_sales_insights(product_name, company_url, product_category, competitors_url, value_prop, target_customer):
    """
    Scrapes the target URL, constructs the prompt with real-time context, and calls Gemini.
    """
    # 1. SCRAPE DATA
    website_data = get_website_content(company_url) 
    
    # 2. Model Selection
    # CONFIRMED: 'models/gemini-flash-latest' is the stable working model for your key
    model = genai.GenerativeModel('models/gemini-flash-latest') 
    
    # 3. Construct the Prompt
    prompt = f"""
    You are an expert Sales Assistant Agent. Your goal is to help a sales rep sell "{product_name}" to the company at "{company_url}".
    
    Here is the context:
    - Product Category: {product_category}
    - Value Proposition: {value_prop}
    - Competitors URL: {competitors_url}
    - Target Customer: {target_customer}
    
    --- REAL-TIME WEBSITE DATA START (Priority Source) ---
    {website_data}
    --- REAL-TIME WEBSITE DATA END ---

    CRITICAL: Base your analysis primarily on the [REAL-TIME WEBSITE DATA] if available. If no data is available, infer likely strategies from the company name.

    Please generate a professional "Account One-Pager" with the following 4 sections.

    SECTION 1: Company Strategy
    Summarize the company's recent activities, strategy, and goals, using specific keywords and phrases found in the [REAL-TIME WEBSITE DATA].

    SECTION 2: Competitor Mentions
    Analyze how they might interact with {competitors_url} or similar rivals.

    SECTION 3: Leadership Information
    Identify key leaders (C-suite, VPs) relevant to buying {product_category}.

    SECTION 4: Article Links
    List 2-3 relevant real or likely search terms for finding recent news.

    Keep the tone professional and concise.
    """

    try:
        # Check session state to avoid spamming API if we already hit the quota
        if st.session_state.get('quota_hit'):
            return "Error generating insights: Quota previously exhausted. Please wait before retrying."
            
        response = model.generate_content(prompt)
        
        # If successful, ensure the quota flag is cleared
        st.session_state['quota_hit'] = False 
        return response.text

    except Exception as e:
        # Specific handling for the 429 error
        if "429" in str(e):
            st.session_state['quota_hit'] = True
            return f"Error generating insights: Quota limit hit for model {model.model_name}. Please wait or check your Google AI billing."
        return f"Error generating insights: {str(e)}"


# --- 4. STREAMLIT INTERFACE ---

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

# Main Logic
if generate_btn:
    if not company_url:
        st.error("Please enter a **Company URL** to generate insights.")
    else:
        with output_placeholder.container():
            st.info(f"Agent running... Scraping and analyzing **{company_url}**...")
            
            # CALL THE AGENT FUNCTION
            generated_output = generate_sales_insights(
                product_name, company_url, product_category, 
                competitors_url, value_proposition, target_customer
            )
            
            # Check for error messages in the return text
            if "Error generating insights" in generated_output:
                st.error(generated_output)
            else:
                st.success("Insights Generated! See the one-pager below.")
                st.markdown("---")
                st.subheader("🎯 Account One-Pager Summary")
                st.markdown(generated_output)
                st.markdown("---")