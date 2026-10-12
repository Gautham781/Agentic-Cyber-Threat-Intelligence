from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from tools import check_virustotal, check_abuseipdb

llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)

agent = create_agent(
    model=llm,
    tools=[check_virustotal, check_abuseipdb]
)

response = agent.invoke({
    "messages": [
        (
            "user",
            """Investigate the IP address 8.8.8.8.

Use BOTH VirusTotal and AbuseIPDB.

First gather the results from both tools.
Then provide the results separately.
After that, interpret the combined evidence point-by-point.

Do not mix the raw tool results with your interpretation."""
        )
    ]
})

print(response["messages"][-1].content)