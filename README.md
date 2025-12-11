# capstone_sales_agent_perscholas

# AI Sales Agent Prototype 🤖

A streamlined AI tool designed to help sales representatives generate instant account insights. This application takes a company URL and product details, scrapes the target website for real-time data, and uses Google Gemini to generate a strategic "One-Pager" summary.

## 🚀 Features

* **Real-Time Web Scraping:** Fetches live content from target company websites using `requests` and `BeautifulSoup`.
* **AI Analysis:** Integrated with **Google Gemini (Flash Model)** to synthesize data into actionable sales intelligence.
* **Strategic Outputs:** Generates a structured report including Company Strategy, Competitor Mentions, and Leadership identification.
* **User Interface:** Clean, interactive front-end built with **Streamlit**.

## 🛠️ Tech Stack

* **Python 3.x**
* **Streamlit** (UI Framework)
* **Google Generative AI SDK** (LLM Integration)
* **BeautifulSoup4** (Web Parsing)

## 📋 Prerequisites

Before running the app, ensure you have:
1.  Python installed on your machine.
2.  A **Google Gemini API Key** (Free tier available at [Google AI Studio](https://aistudio.google.com/)).

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd capstone_sales_agent
2. Create a Virtual Environment

Bash

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies

Bash

pip install -r requirements.txt
4. Configure API Key For security, this project uses a secrets file that is ignored by Git.

Create a folder named .streamlit in the root directory.

Inside it, create a file named secrets.toml.

Add your API key:

Ini, TOML

# .streamlit/secrets.toml
GEMINI_API_KEY = "YOUR_API_KEY_HERE"
▶️ Usage
Run the application locally:

Bash

streamlit run app.py
Enter the Product Name you are selling.

Enter the Target Company URL (e.g., https://www.example.com).

Click Generate Insights.

The agent will scrape the site and display a structured One-Pager below.

📂 Project Structure
capstone_sales_agent/
├── app.py                # Main application logic
├── requirements.txt      # Project dependencies
├── .gitignore            # Ignores secrets and virtual env
├── README.md             # Documentation
└── .streamlit/
    └── secrets.toml      # API Keys (Not tracked in Git)
🛡️ Troubleshooting
404 Error: If the model is not found, ensure you are using a supported model name in app.py (e.g., models/gemini-flash-latest).

429 Quota Error: If you hit the free tier limit, wait a few minutes or switch to a different Gemini model.


---

### Why this structure matters for your grade:
This single file covers multiple requirements:
* **"Documentation":** It explains what the project is.
* **"Installation & Setup":** It proves you know how to instruct others to run your code.
* **"Tech Stack":** It lists the libraries you used (Streamlit, BeautifulSoup, Gemini).

Once you have pasted and saved this, you can do the final commit we discussed!

