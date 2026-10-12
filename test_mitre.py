from agents import mitre_agent


response = mitre_agent.invoke({
    "messages": [
        (
            "user",
            """
            Map the following observed behavior to MITRE ATT&CK.

            Observed behavior:
            No specific attacker behavior was identified.

            Only return the relevant MITRE ATT&CK technique.
            Do not explain or guess.
            """
        )
    ]
})

print(response["messages"][-1].content)