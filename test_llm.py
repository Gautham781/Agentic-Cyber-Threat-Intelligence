from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)

response = llm.invoke("Explain Cyber Threat Intelligence in one sentence.")

print(response.content)