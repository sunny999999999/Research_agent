import os
import json
import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient
from gmail_service import Send_Email_Via_Gmail
from prompts import Email_Agent_Prompt

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gemini-2.5-flash",
    parallel_tool_calls=False
)

async def send_email(subject: str, body_txt: str):
    response = await Send_Email_Via_Gmail(subject, body_txt)
    return response

mail_send = FunctionTool(send_email, description="sends mail")

async def Email_Agent_Run(Context:str):
    email_sender = AssistantAgent(
    name="email_sender",
    model_client=model_client,
    tools=[mail_send],
    system_message=Email_Agent_Prompt,
    max_tool_iterations=1,
    )

    result = await email_sender.run(task=Context)
    #extract final tool call (send_email)
    subject, body = "", ""
    for msg in result.messages:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tool_call in msg.tool_calls:
                if getattr(tool_call, "name", None) == "send_email":
                    args = json.loads(tool_call.arguments)
                    subject = args.get("subject", "")
                    body = args.get("body_txt", "")
    return {
        "subject": subject,
        "body": body
    }

# if __name__ == "__main__":
#     asyncio.run(Send_Email_Agent())