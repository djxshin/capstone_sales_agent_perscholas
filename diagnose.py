import streamlit as st
import google.generativeai as genai

st.title("Gemini Model Diagnostic")

# 1. Get the key from your secrets file
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    st.write("✅ API Key found.")
else:
    st.error("❌ No API Key found in .streamlit/secrets.toml")
    st.stop()

st.write("### 🔍 The following models are available to you:")

try:
    # 2. Ask Google for the list
    found_any = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # 3. Print the EXACT string you need to use
            st.code(m.name) 
            found_any = True
    
    if not found_any:
        st.warning("No models found. Your API key might be inactive or restricted.")

except Exception as e:
    st.error(f"Error contacting Google: {e}")