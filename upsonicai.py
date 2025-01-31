import os
import requests
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from upsonic import UpsonicClient, Task, AgentConfiguration, ObjectResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Upsonic client
client = UpsonicClient("localserver")
client.set_config("AWS_ACCESS_KEY_ID", os.getenv("AWS_ACCESS_KEY_ID"))
client.set_config("AWS_SECRET_ACCESS_KEY", os.getenv("AWS_SECRET_ACCESS_KEY"))
client.set_config("AWS_REGION", os.getenv("AWS_REGION"))

client.set_config("AZURE_OPENAI_ENDPOINT", os.getenv("AZURE_OPENAI_ENDPOINT"))
client.set_config("AZURE_OPENAI_API_VERSION", os.getenv("AZURE_OPENAI_API_VERSION"))
client.set_config("AZURE_OPENAI_API_KEY", os.getenv("AZURE_OPENAI_API_KEY"))

client.default_llm_model = "azure/gpt-4o"

# Define FastAPI app
app = FastAPI()

# Define Input Model
class DoubleSearchInput(BaseModel):
    keyword1: str
    keyword2: str

# Define Response Format
class SearchResult(ObjectResponse):
    title: str
    link: str
    snippet: str

class DoubleSearchResponse(ObjectResponse):
    keyword1_results: list[SearchResult]
    keyword2_results: list[SearchResult]

# SerpAPI Tool for Web Search
@client.tool()
class SerpAPITool:
    def search(query: str) -> list:
        """Searches SerpAPI with the given query and returns top results."""
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="SerpAPI API Key not found!")

        url = "https://google.serper.dev/search"
        headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }
        payload = json.dumps({"q": query})

        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            search_results = data.get("organic", [])

            return [
                SearchResult(
                    title=result.get("title", "No Title"),
                    link=result.get("link", "#"),
                    snippet=result.get("snippet", "No Description")
                )
                for result in search_results[:10]
            ]
        else:
            raise HTTPException(status_code=500, detail=f"SerpAPI Request Failed: {response.text}")

# Define Search Agent
search_agent = AgentConfiguration(
    job_title="Double Keyword Search Analyst",
    company_url="https://upsonic.ai",
    company_objective="Fetch and analyze the latest search results for two different keywords.",
    reflection=True
)

@app.post("/double-search/")
async def perform_double_search(input_data: DoubleSearchInput):
    """Performs a web search using SerpAPI for two keywords and returns results."""
    
    # Task for first keyword
    search_task1 = Task(
        description=f"Perform a web search for {input_data.keyword1} and return the top results.",
        tools=[SerpAPITool],
        response_format=DoubleSearchResponse
    )

    # Task for second keyword
    search_task2 = Task(
        description=f"Perform a web search for {input_data.keyword2} and return the top results.",
        tools=[SerpAPITool],
        response_format=DoubleSearchResponse
    )

    # Run Agent for both tasks
    client.agent(search_agent, search_task1)
    client.agent(search_agent, search_task2)

    search_data1 = search_task1.response
    search_data2 = search_task2.response

    if not search_data1 or not search_data2:
        raise HTTPException(status_code=500, detail="Failed to fetch search results.")

    return {
        "keyword1": input_data.keyword1,
        "keyword1_results": search_data1.keyword1_results,
        "keyword2": input_data.keyword2,
        "keyword2_results": search_data2.keyword2_results
    }

# UI for double search functionality
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Dual Search</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
            input { padding: 10px; margin: 10px; width: 300px; }
            button { padding: 10px; background: blue; color: white; border: none; cursor: pointer; }
            #results { margin-top: 20px; text-align: left; }
            footer { margin-top: 30px; font-size: 0.9em; color: #555; }
            footer a { color: #007BFF; text-decoration: none; }
            footer a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>AI Dual Search</h1>
        <input type="text" id="keyword1" placeholder="Enter first keyword">
        <input type="text" id="keyword2" placeholder="Enter second keyword">
        <button onclick="fetchDoubleSearchResults()">Search</button>
        <div id="results"></div>
        <footer>
            Powered by <a href="https://upsonic.ai" target="_blank">UpsonicAI</a>
        </footer>
        <script>
            async function fetchDoubleSearchResults() {
                const keyword1 = document.getElementById('keyword1').value;
                const keyword2 = document.getElementById('keyword2').value;
                const response = await fetch('/double-search/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ keyword1, keyword2 })
                });

                const data = await response.json();
                let resultsHTML = "<h2>Results:</h2>";

                resultsHTML += `<h3>${data.keyword1} Results:</h3>`;
                data.keyword1_results.forEach(result => {
                    resultsHTML += `<p><strong>${result.title}</strong><br>${result.snippet}<br><a href="${result.link}" target="_blank">Read more</a></p>`;
                });

                resultsHTML += `<h3>${data.keyword2} Results:</h3>`;
                data.keyword2_results.forEach(result => {
                    resultsHTML += `<p><strong>${result.title}</strong><br>${result.snippet}<br><a href="${result.link}" target="_blank">Read more</a></p>`;
                });

                document.getElementById('results').innerHTML = resultsHTML;
            }
        </script>
    </body>
    </html>
    """
