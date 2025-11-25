import os
from typing import List
from sheet_service import get_service
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import Swarm
from autogen_agentchat.base import TaskResult
from autogen_agentchat.ui import Console
from pydantic import BaseModel
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient
from firecrawl import Firecrawl
from prompts import Research_Agent_Prompt
import streamlit as st

load_dotenv()
api_key = st.secrets["GEMINI_API_KEY"]

# google_sheet_id = os.getenv("GOOGLE_SHEET_ID")
# Firecrawl_api_key = os.getenv("FIRECRAWL_API_KEY")
google_sheet_id = st.secrets("GOOGLE_SHEET_ID")
Firecrawl_api_key = st.secrets("FIRECRAWL_API_KEY")

model_client = OpenAIChatCompletionClient(model="gemini-2.5-flash",api_key=api_key,
                                          parallel_tool_calls=False)

def read_sheet(range_str: str) -> List[List[str]]:
    """Read values from a Google Sheet range."""
    service = get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=google_sheet_id, range=range_str
    ).execute()
    return result.get("values", [])

async def fire_search(query:str):
    """Searches the web"""
    firecrawl = Firecrawl(api_key=Firecrawl_api_key)
    results = firecrawl.search(query=query,limit=3)
    return results

async def fire_extract_content(query: str) -> str:
    """Extracts Content"""
    firecrawl = Firecrawl(api_key=Firecrawl_api_key)
    docs = firecrawl.crawl(url=query,limit=2,ignore_sitemap=True,crawl_entire_domain=True)
    return docs.data
   
sheet_read  = FunctionTool(read_sheet,description="read a sheet")
Web_Search = FunctionTool(fire_search,description="search the web")
Extract_Content = FunctionTool(fire_extract_content,description="extracts the web")

async def Research_agent_run(Task:str):
    researcher = AssistantAgent(
    name="researcher",
    model_client=model_client,
    tools=[sheet_read,Web_Search,Extract_Content],
    max_tool_iterations=7,
    system_message=Research_Agent_Prompt,
)
    result: TaskResult = await researcher.run(task=Task)

    #extract the final assistant message from the list of messages
    if result.messages:
        final_msg = result.messages[-1].content
        print("\n-- Final Report --\n")
        print(final_msg)

        #save the research report into report.txt file
        with open("report.txt", "w", encoding="utf-8") as f:
            f.write(final_msg)

        print("\n Report has been saved to report.txt")
    else:
        print("No final message produced.")

# if __name__ == "__main__":

#     asyncio.run(main())
