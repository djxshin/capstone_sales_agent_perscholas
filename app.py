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

    # --- MAIN LOGIC BLOCK ---

# Use a placeholder to display the final output, allowing us to easily clear it later
output_placeholder = st.empty() 

if generate_btn:
    # 1. Check for required inputs (Company URL is the minimum)
    if not company_url:
        st.error("Please enter a **Company URL** to generate insights.")
    else:
        # 2. Display a 'Working' message while the agent is running
        with output_placeholder.container():
            st.info(f"Agent running... Gathering insights for **{company_url}** using product **{product_name}**.")
            st.progress(25) # Mock progress bar
            
            # 3. Call the Agent logic (This is where the LLM call will eventually go)
            
            # 4. Display the structured one-pager output (Placeholder for Step 2)
            st.success("Insights Generated! See the one-pager below.")
            
           # --- ONE-PAGER DOCUMENT STRUCTURE ---
            st.markdown("---")
            st.subheader("🎯 Account One-Pager Summary")
            st.markdown(f"**Target Account:** {company_url}")
            st.markdown(f"**Product Focus:** {product_name} ({product_category})")
            st.markdown("---")

            st.markdown("#### 1. Company Strategy (Source: LLM Analysis of Web Data)")
            st.text("— Summary of public statements, press releases, and job postings indicating strategy [cite: 62-64] —")

            st.markdown("#### 2. Competitor Mentions")
            st.text("— Analysis of web data to find mentions of competitors [cite: 65] —")

            st.markdown("#### 3. Leadership Information")
            st.text("— Key leaders and their relevance, based on press releases [cite: 66] —")

            st.markdown("#### 4. Article Links & Sources")
            st.text("— Links to full articles, 10-Ks, and press releases [cite: 67-68] —")
            
            st.progress(100)