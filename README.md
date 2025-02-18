# Multi-Agent Finance Advisor
## An Advanced AI-Powered Financial Advisory System

The Multi-Agent Finance Advisor is a sophisticated financial advisory system that leverages multiple AI agents to provide comprehensive financial insights and investment recommendations. Built with Streamlit, it combines real-time market data, news analysis, and expert financial modeling to deliver reliable financial advice.
Features

## Multi-Agent Architecture

- Web Agent: Searches and analyzes current market trends and financial news
- Finance Agent: Processes financial data and performs quantitative analysis
- Reasoning Agent: Integrates insights for comprehensive recommendations


### Real-Time Data Integration

- Live market data through YFinance
- Current news and trends via DuckDuckGo
- Historical financial data analysis


### Interactive User Interface

- Customizable agent instructions
- Streaming responses with markdown formatting
- Wide-layout design for better data visualization


### Advanced Analysis Capabilities

- Step-by-step reasoning
- Source verification and citation
- Numerical data presentation in tables
- Market trend analysis



# Installation
- Clone the repository
- git clone https://github.com/yourusername/multi-agent-finance-advisor.git

## Install required dependencies
- pip install -r requirements.txt

## Start the Streamlit application:

- streamlit run app.py

- Access the web interface at http://localhost:8501
- Enter your API keys in the sidebar
- Input your financial question and customize agent instructions if needed
- Click "Submit" to receive comprehensive financial analysis

### API Keys
The system requires two API keys:

- OpenAI API Key

- Get it from: https://platform.openai.com

- Groq API Key

- Get it from: https://console.groq.com

- Create a .env file in the root directory:
- OPENAI_API_KEY=your_openai_key_here
- GROQ_API_KEY=your_groq_key_here

# Submit a query
query = "Where should I invest my 10,000 dollars for optimal returns?"
For more information or support, please open an issue in the repository.
