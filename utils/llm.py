import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "foundry")

if LLM_PROVIDER == "github":
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # GitHub Models backup
        api_key=os.getenv("GITHUB_TOKEN"),
        base_url="https://models.inference.ai.azure.com",
        temperature=0,
    )
else:
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(
        model=os.getenv("AZURE_DEPLOYMENT", "gpt-4.1-mini"),
        api_key=os.getenv("AZURE_API_KEY"),
        base_url=os.getenv("AZURE_ENDPOINT"),
        temperature=0,
    )