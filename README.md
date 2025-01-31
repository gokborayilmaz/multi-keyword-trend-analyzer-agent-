# 21-Day Agent Series: Day 2
## **AGENT: Multi-Keyword-Based Trend Analyzer Agent**

### **Overview**
The **Multi-Keyword-Based Trend Analyzer Agent** is part of the 21-day AI agent series. This agent leverages SerpAPI to perform real-time-multi keyword-based searches and fetch the latest relevant articles, providing an efficient way to track trends. 🚀🔍

### **Features**
- Accepts a multi keyword input from the user 📌
- Fetches search results using **SerpAPI**
- Displays results in a structured UI format 📊
- Powered by **Upsonic AI** 🧠⚡

## **Installation**

### **Prerequisites**
- Python **3.9+** 🐍
- **Git** installed
- **Virtual environment** (recommended) 🏗️
- **Node.js** installed (for MCP support)

### **Steps**

#### **1. Clone the Repository**
```sh
git clone <repository-url>
cd <repository-folder>
```

#### **2. Install Dependencies**
```sh
pip install -r requirements.txt
```

#### **3. Configure Environment Variables**
Create a `.env` file in the root directory and set your API keys:

```ini
AWS_ACCESS_KEY_ID="your_aws_access_key_id"
AWS_SECRET_ACCESS_KEY="your_aws_secret_access_key"
AWS_REGION="your_aws_region"

AZURE_OPENAI_ENDPOINT="your_azure_openai_endpoint"
AZURE_OPENAI_API_VERSION="your_azure_openai_api_version"
AZURE_OPENAI_API_KEY="your_azure_openai_api_key"

SERPAPI_API_KEY="your_serpapi_api_key"
```

### **Running the Application**

#### **1. Start the FastAPI Server**
```sh
uvicorn upsonicai:app --reload
```

#### **2. Access the UI in Your Browser**
Navigate to:
```
http://127.0.0.1:8000/
```
- Enter a keyword 📎
- Click "Search" 🔍
- View and analyze search results 📄

### **API Documentation**
Interactive API documentation is available at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 📖


### **License**
This project is open-source and follows the MIT License. 📝

### **Credits**
- Developed using **Upsonic AI**
- Powered by **SerpAPI** for real-time search data

---
**Powered by [Upsonic AI](https://upsonic.ai)** 🚀


