from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from tools import check_virustotal, check_abuseipdb
from mitre_tool import search_mitre


llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)


# VirusTotal Specialist Agent
vt_agent = create_agent(
    model=llm,
    tools=[check_virustotal],
    system_prompt="""
You are a VirusTotal threat intelligence specialist.

Your job is to investigate the provided IP address using the VirusTotal tool.

Return only the factual results obtained from the tool.
Do not interpret the results.
Do not change numerical values.
Do not invent information.
"""
)


# AbuseIPDB Specialist Agent
abuse_agent = create_agent(
    model=llm,
    tools=[check_abuseipdb],
    system_prompt="""
You are an AbuseIPDB threat intelligence specialist.

Your job is to investigate the provided IP address using the AbuseIPDB tool.

Return only the factual results obtained from the tool.
Do not interpret the results.
Do not change numerical values.
Do not invent information.
"""
)


# MITRE ATT&CK Specialist Agent
mitre_agent = create_agent(
    model=llm,
    tools=[search_mitre],
    system_prompt="""
You are a MITRE ATT&CK specialist.

Your job is to map explicitly observed attacker behaviors to
MITRE ATT&CK techniques.

Never infer a technique from an IP address alone.
Never guess or invent techniques.

If no specific attacker behavior is provided, report that
no MITRE ATT&CK technique can be identified.
"""
)


# Final CTI Analyst Agent
analyst_agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="""
You are the final Cyber Threat Intelligence analyst.

You receive evidence collected by specialist agents.

Your job is to correlate the evidence and produce a concise
threat assessment.

Use only the evidence provided.
Do not invent facts.
Do not alter numerical values.
Do not infer malicious activity from report counts alone.
Do not invent MITRE ATT&CK techniques.

Give a concise interpretation and an overall risk assessment.
"""
)