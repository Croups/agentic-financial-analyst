import streamlit as st
import time
import re
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

# Optional: If you want to reduce heading sizes (e.g., #### -> ###),
# you can adjust the regex in this function.
def adjust_markdown_headings(text: str) -> str:
    # Example: replace "####" with "###"
    text = re.sub(r"####", "###", text)
    return text

# --------- Page Layout ---------
st.set_page_config(page_title="Reliable Finance Advisor", layout="wide")
st.title("Multi-Agent Finance Advisor with DeepSeek Reasoning")
st.markdown(
    """
    Welcome to the Reliable Finance Advisor demo! This multi-agent system leverages up-to-date financial data, market news, 
    and expert analysis to answer your finance-related questions. Adjust the advisor's instructions and API keys as needed.
    """
)

# --------- Sidebar Inputs for API Keys ---------
st.sidebar.header("API Keys")
openai_api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
groq_api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")

# --------- User Input for Agent Instructions & Query ---------
default_instructions = (
    "Act as a reliable financial advisor capable of answering any finance-related questions.\n"
    "Generate separate outputs for market research and financial data analysis, then integrate them into one comprehensive final answer.\n"
    "Always include verified sources, clear numerical data, and step-by-step reasoning."
)
agent_instructions = st.text_area("Agent Team Instructions (optional)", default_instructions, height=150)
query = st.text_input("Enter your finance question", "Where should I invest my 10,000 dollars for 100% revenue?")
close_reasoning = st.checkbox("Disable detailed reasoning (Close Reasoning)", value=False)

# --------- Submit Button ---------
if st.button("Submit"):
    if not openai_api_key or not groq_api_key:
        st.error("Please provide both OpenAI and Groq API keys in the sideb ar.")
    else:
        # Define the Web Agent for market news and trends.
        web_agent = Agent(
            name="Web Agent",
            role="Search the web for up-to-date financial news, market trends, and expert analysis",
            model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
            tools=[DuckDuckGo()],
            instructions=[
                "Always provide verified sources and links to reputable financial news outlets.",
                "Include context on market trends and current events affecting the finance world.",
                "Summarize information clearly and accurately."
            ],
            show_tool_calls=True,
            markdown=True,
        )

        # Define the Finance Agent for data analysis and calculations.
        finance_agent = Agent(
            name="Finance Agent",
            role="Retrieve and analyze financial data, perform calculations, and offer detailed insights",
            model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
            tools=[YFinanceTools(stock_price=True, company_info=True)],
            instructions=[
                "Provide detailed, step-by-step financial calculations where necessary.",
                "Always use tables for a clear presentation of numerical data.",
                "Verify data accuracy and include sources or references when available."
            ],
            show_tool_calls=True,
            markdown=True,
        )

        # Define the Reasoning Agent to integrate responses from the Web and Finance agents.
        reasoning_agent = Agent(
            name="Reasoning Agent",
            role="Integrate outputs from the Web and Finance agents to produce a reliable, comprehensive final financial analysis",
            model=Groq(id="deepseek-r1-distill-llama-70b", api_key=groq_api_key),
            reasoning=True,
            markdown=True,
            structured_outputs=True,
            instructions=[
                "Aggregate the outputs from the Web and Finance agents, ensuring consistency and accuracy.",
                "Provide a final analysis that includes step-by-step reasoning and clearly highlights any calculations and assumptions.",
                "Cite sources from the individual agent responses where applicable."
            ],
        )

        # Create the Agent Team with the (possibly user-modified) instructions.
        agent_team = Agent(
            team=[web_agent, finance_agent, reasoning_agent],
            instructions=[agent_instructions],
            show_tool_calls=True,
            markdown=True,
        )

        # --------- Streaming Response ---------
        st.markdown("### Answer")
        placeholder = st.empty()
        response_text = ""
        
        # Stream the response, display it as Markdown, and optionally adjust headings.
        for delta in agent_team.run(query, stream=True, show_full_reasoning=not close_reasoning):
            # Extract content if available, else convert to string
            text = delta.content if hasattr(delta, "content") else str(delta)
            response_text += text

            # If you want to adjust headings, apply the function here
            final_text = adjust_markdown_headings(response_text)

            # Display as Markdown (no horizontal scroll)
            placeholder.markdown(final_text)
            
            # Optional short delay to ensure UI updates smoothly
            time.sleep(0.075)
