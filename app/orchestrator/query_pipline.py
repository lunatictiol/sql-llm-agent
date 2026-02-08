from app.agents.sql_agent import SQLAgentExecutor
from app.sql.validator import validate_sql_with_llm
from app.sql.errors import SQLValidationError
from app.core.redis import redis_client
import json
def run_query_pipeline(user_question: str,schema_id:str) -> dict:
   

    schema_text = redis_client.get(f"schema:{schema_id}")
    # 4. Generate SQL via LLM
    llm = SQLAgentExecutor()
    sql = llm.generate_sql(user_question)


    # 6. Validate SQL
    try:
       
        validate_sql_with_llm(
            sql=sql,
            schema_context=schema_text,
            user_question=user_question,
        )
    except SQLValidationError as e:
        return {"error": str(e)}

    response = json.loads(sql)    
    
    

    return {"sql":response}
