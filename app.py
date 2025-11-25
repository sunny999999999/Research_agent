import streamlit as st
import asyncio
import os

# Import your async agent function
from research_agent import Research_agent_run

st.set_page_config(page_title="AI Research Agent", layout="wide")

st.title("Autonomous Research Agent")
st.write("Provide the prospect details below. The agent will generate a tailored research report.")

# --- User Inputs ---
prospect_name = st.text_input("Prospect Name")
company_name = st.text_input("Company Name")

st.write("The research agent will use these inputs to generate a personalized research report.")

# Run button
if st.button(" Run Research Agent"):
    if not prospect_name.strip() or not company_name.strip():
        st.warning("Please fill both Prospect Name and Company Name!")
    else:
        # Construct the task
        task_input = (
            f"Generate a detailed research report on the prospect '{prospect_name}' "
            f"and the company '{company_name}'. Include company overview, financials, "
            f"market position, recent news, competitive landscape, and any relevant insights."
        )

        st.info("Agent is running... Please wait (10–30 seconds).")

        async def run_agent():
            await Research_agent_run(task_input)

        asyncio.run(run_agent())

        # Load report.txt if available
        if os.path.exists("report.txt"):
            st.success("Research Completed Successfully! 🎉")

            with open("report.txt", "r", encoding="utf-8") as f:
                report_content = f.read()

            st.subheader("Generated Research Report")
            st.text_area("Report", value=report_content, height=450)

            # Option to download the report
            st.download_button(
                "Download Report",
                data=report_content,
                file_name=f"{prospect_name}_{company_name}_report.txt",
                mime="text/plain",
            )
        else:
            st.error("No report generated. Please try again.")
