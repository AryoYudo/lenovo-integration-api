@echo off
call venv\Scripts\activate
cd mysatnusa
uvicorn core.main:app --port 8080
