# 🛡️ Insurance Product Recommendation Agent

This project demonstrates a Generative AI-powered interactive chat agent designed to recommend suitable insurance products to users based on their specific needs and information. Built for BFSI (Banking, Financial Services, and Insurance) sector, it showcases the power of LLMs (Large Language Models) in customer engagement and personalized recommendations.

The agent engages the user in a conversational flow, gathering essential details such as age, dependents, income, assets, health, travel habits, and budget. Based on this collected information, it leverages a Generative AI model to analyze the user's profile against a predefined product catalog and offer tailored insurance recommendations with explanations.

## ✨ Features

- **Interactive Chat Interface**: User-friendly conversational flow built with Streamlit.
- **Sequential Questioning**: Guides the user through a series of questions to gather relevant information.
- **AI-Powered Interpretation & Recommendation**: Uses a Generative AI model to understand user input and generate personalized insurance product suggestions.
- **Configurable LLM Backend**: Supports Google Gemini API ( gemini-2.0-flash model )
- **Modular Codebase**: Organized into separate files for UI, LLM service, and product data.

## 🚀 Technology Stack

- **Python**: Core programming language.
- **Streamlit**: For building the interactive web UI.
- **Google Generative AI (Gemini API)**: The primary Generative AI model for robust and scalable recommendations.  
  *(Alternative: Ollama with Mistral for local inference if configured)*
- **python-dotenv**: For managing environment variables (e.g., API keys, model names).
- **requests**: For making HTTP calls to the Gemini API.

## 🛠️ Setup Guide

Follow these steps to get the Insurance Product Recommendation Agent running on your local machine.

### Prerequisites

- **Google Gemini API Key**: Obtain your API key from Google AI Studio.

### Step-by-Step Installation

**Clone the Repository:**

```bash
git clone https://github.com/Waseemkhan09/Insurance-Product-Recommendation-Agent.git
cd insurance_agent
```
**Install Python Dependencies:**

```bash
pip install -r requirements.txt
```

**Configure Environment Variables:**

```bash
MODEL_NAME="gemini-2.0-flash"
GEMINI_API_KEY="YOUR_GENERATED_GEMINI_API_KEY_HERE"
```
**Important**:Replace "YOUR_GENERATED_GEMINI_API_KEY_HERE" with the actual Google Gemini API Key 

## ▶️ Running the Application
Once all the setup steps are complete, you can run the Streamlit application:

Ensure your virtual environment is activated.

Run the Streamlit app:
```bash
streamlit run app/main.py
```

## 🌐 Access the Application
Streamlit will typically open a new tab in your default web browser (or provide a URL) where your application is running. It will usually be something like:

``` bash
http://localhost:8501
```

## 🤝 Usage
Once the application loads, the AI advisor will greet you and ask the first question.

Type your answers in the input box at the bottom of the chat interface.

The agent will guide you through a series of questions to gather your insurance needs.

After all questions are answered, the agent will process your information and provide personalized insurance product recommendations.

You can click the "🔄 Start New Recommendation" button to restart the conversation at any time.

## Managed By
Waseem Khan
Email: wseem7861khan@gmail.com
