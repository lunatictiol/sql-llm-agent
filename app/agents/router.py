class AgentRouter:
    def route(self, query: str):
        """Decides which agent to use based on the query."""
        if "select" in query.lower() or "table" in query.lower():
            return "sql_agent"
        return "mcp_agent"
