# 🚀 FastAPI Backend — Learning Notes

A personal learning project to explore **FastAPI** as a backend framework, covering routing, databases, and authentication.

---

## 📌 What is FastAPI?

FastAPI is a modern, fast Python web framework for building APIs. It's built on top of **Starlette** and **Pydantic**, and automatically generates interactive docs.

---

## 🛠️ Installation

```bash
pip install fastapi uvicorn sqlalchemy python-jose[cryptography] passlib[bcrypt]
```

Run the server:

```bash
uvicorn main:app --reload
```

Then open: `http://127.0.0.1:8000/docs` for the auto-generated Swagger UI.

---

## 📁 Project Structure
