from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from app.llm.utils import load_prompt,extract_ai_content
from app.rag.retriever import retrieve_context
from langchain_core.messages import AIMessage
from app.llm.models import ModelType

class SQLAgentExecutor:
    """
    Agent-based SQL generator/executor.
    Responsible for:
    - grounding via schema/context retrieval
    - generating deterministic SQL
    """

    def __init__(
        self,
        model_name: str = ModelType.QWEN,
        temperature: float = 0.1,
    ):
        self.model = ChatOllama(
            model=model_name,
            temperature=temperature,
        )

        self.tools = [retrieve_context]

        self.system_prompt = load_prompt("base") + "\n" + load_prompt("sql_generator")

        self.agent = create_agent(
            model=self.model,
            tools=self.tools,
            system_prompt=self.system_prompt,
        )

    def generate_sql(self, user_question: str) -> str:
        """
        Generate SQL for a natural language question.
        """

        response = self.agent.invoke(
            {
                "messages": [
                    HumanMessage(content=user_question)
                ]
            }
        )
        

        sql = extract_ai_content(response)
        return sql

    def execute_sql(self, user_question: str) -> str:
        """
        Public entrypoint — semantic clarity.
        (Later: hook this into a real DB executor)
        """
        return self.generate_sql(user_question)





