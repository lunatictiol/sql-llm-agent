# 🧠 SQL LLM Agent (Schema-Aware, Validated)

This project is a **schema-grounded SQL generation system** that converts natural language questions into **valid PostgreSQL SELECT queries**, using:

* **Schema introspection**
* **RAG (Retrieval-Augmented Generation)**
* **LangChain for SQL generation**
* **DSPy + Phi-3 for strict SQL validation**
* **FastAPI backend**
* **Streamlit frontend**

This is **not** a chatbot demo.
It is a **compiler-style pipeline** focused on correctness, safety, and debuggability.

---

## ✨ Key Features

* 🔍 Automatic PostgreSQL schema introspection
* 🧠 RAG-based grounding using vector search
* 🧾 SQL generation using **LangChain + Ollama**
* 🔒 Strict SQL validation using **DSPy + Phi-3**
* 🚫 Blocks:

  * invalid tables or columns
  * non-PostgreSQL syntax (e.g. `YEAR()`)
  * non-SELECT queries
* 🎛️ Deterministic validation (temperature = 0)
* 🖥️ Minimal Streamlit UI for testing

---

## 🏗️ High-Level Architecture

```
User Question
     ↓
Schema Retrieval (RAG – LangChain)
     ↓
SQL Generation (LangChain + Qwen)
     ↓
SQL Validation (DSPy + Phi-3)
     ↓
✔ Valid SQL or ❌ Error
```

---

## 🧠 Why LangChain + DSPy (Design Rationale)

This project **intentionally uses both LangChain and DSPy**, but for **different roles**.

### Why LangChain for SQL generation?

SQL generation is an **open-ended, language-heavy task**:

* Requires interpreting user intent
* Benefits from prompt engineering
* Needs flexible context injection (schema, examples)
* Works well with message-based LLM APIs

LangChain is well-suited for this because it:

* Makes prompt composition easy
* Integrates cleanly with Ollama
* Handles RAG-style context injection naturally

In short: **generation is creative**, and LangChain handles that well.

---

### Why DSPy for validation?

SQL validation is **not creative**.
It is a **judgment and constraint-checking problem**.

Validation requires:

* Deterministic outputs
* Strict structure
* No hallucinated explanations
* Guaranteed machine-readable results

DSPy is used here because it:

* Enforces **typed outputs** (e.g. `valid: bool`)
* Eliminates fragile JSON-in-prompt parsing
* Constrains the model’s reasoning space
* Produces reliable, debuggable decisions

In short: **validation must behave like software**, not chat.

---

### Separation of concerns (intentional)

| Task           | Tool      | Reason                    |
| -------------- | --------- | ------------------------- |
| SQL generation | LangChain | Flexible, prompt-driven   |
| SQL validation | DSPy      | Structured, deterministic |
| Execution      | Database  | Authoritative             |

This separation prevents:

* Tool-call leakage into SQL
* Hallucinated fixes during validation
* Prompt complexity explosion

---

## 🚀 How It Works

### 1️⃣ Load Database Schema

**Endpoint**

```http
POST /api/v1/schema
```

**Request**

```json
{
  "url": "postgresql://readonly_user:readonly_pass@localhost:5432/mydb"
}
```

**Response**

```json
{
  "message": "Schema stored successfully",
  "schema_id": "e14b9576-1f64-4c05-aa43-6f3d6094821e"
}
```

What happens:

* Schema is introspected (tables, columns, keys, relations)
* Normalized into text documents
* Cached for reuse
* Embedded for RAG-based retrieval

---

### 2️⃣ Generate SQL

**Endpoint**

```http
POST /api/v1/chat
```

**Request**

```json
{
  "question": "List all customers",
  "schema_id": "e14b9576-1f64-4c05-aa43-6f3d6094821e"
}
```

**Response**

```json
{
  "sql": "SELECT * FROM customers LIMIT 100;"
}
```

Pipeline:

1. Retrieve relevant schema context via RAG
2. Generate SQL using LangChain + LLM
3. Validate SQL using DSPy + Phi-3
4. Return SQL or validation error

---

## 🧪 Validation Guarantees

The validator enforces:

* ✅ SELECT-only queries
* ✅ Tables exist in schema
* ✅ Columns exist in schema
* ✅ Joins align with foreign keys
* ✅ PostgreSQL-compatible syntax
* ✅ LIMIT is present
* ❌ No destructive operations

Validation output is **typed**, not free-form JSON.

---

## 🖥️ Streamlit UI

Run the frontend:

```bash
streamlit run app.py
```

The UI allows you to:

* Paste a PostgreSQL connection string
* Load schema
* Ask natural language questions
* Inspect generated SQL

The UI is intentionally minimal and developer-focused.

---

## ❗ What This Project Is NOT

* ❌ A chatbot
* ❌ An autonomous agent loop
* ❌ A SQL executor (yet)
* ❌ A BI dashboard

This project is a **SQL generation + validation system**.

---

## 🧭 Roadmap

* Read-only SQL execution
* Retry-on-validation-failure loop
* Query history
* CLI client (Go)
* Multi-schema support

---

## 🧠 Design Philosophy

> Use LLMs where they are strong.
> Constrain them where correctness matters.

* LangChain → generation
* DSPy → judgment
* Database → truth

This keeps the system **safe, explainable, and testable**.


