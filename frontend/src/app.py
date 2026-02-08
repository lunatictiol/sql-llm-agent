import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000/api/v1"


# -------------------------
# Page setup
# -------------------------
st.set_page_config(
    page_title="SQL LLM Agent",
    page_icon="🧠",
    layout="centered",
)

st.title("🧠 SQL LLM Agent")
st.caption("Schema-aware SQL generation using RAG + validation")


# -------------------------
# Session state
# -------------------------
if "schema_id" not in st.session_state:
    st.session_state.schema_id = None


# -------------------------
# Schema setup section
# -------------------------
st.header("1️⃣ Load Database Schema")

db_url = st.text_input(
    "PostgreSQL connection string",
    placeholder="postgresql://readonly_user:readonly_pass@localhost:5432/dbname",
    type="password",
)

if st.button("Load Schema"):
    if not db_url:
        st.error("Please provide a connection string")
    else:
        with st.spinner("Loading schema..."):
            try:
                resp = requests.post(
                    f"{API_BASE_URL}/schema",
                    json={"url": db_url},
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()

                st.session_state.schema_id = data["schema_id"]

                st.success("Schema stored successfully")
                st.code(f"Schema ID: {st.session_state.schema_id}")

            except Exception as e:
                st.error(f"Failed to load schema: {e}")


# -------------------------
# Chat section
# -------------------------
st.header("2️⃣ Ask Questions")

if not st.session_state.schema_id:
    st.info("Load a schema first to start querying.")
else:
    st.markdown(
        f"**Active schema ID:** `{st.session_state.schema_id}`"
    )

    question = st.text_input(
        "Ask a question about your data",
        placeholder="List all customers",
    )

    if st.button("Generate SQL"):
        if not question:
            st.error("Please enter a question")
        else:
            with st.spinner("Generating SQL..."):
                try:
                    resp = requests.post(
                        f"{API_BASE_URL}/chat",
                        json={
                            "question": question,
                            "schema_id": st.session_state.schema_id,
                        },
                    )
                    resp.raise_for_status()
                    data = resp.json()

                    st.subheader("Generated SQL")

                    # Your backend currently returns tool-style output
                    if "sql" in data:
                        st.json(data["sql"])
                    else:
                        st.json(data)

                except Exception as e:
                    st.error(f"Failed to generate SQL: {e}")
