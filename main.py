import uvicorn
from fastapi import FastAPI
from src.route import router as route

app = FastAPI(title="Multi-App FastAPI")

# Menyertakan semua router dari aplikasi yang berbeda
app.include_router(route, prefix="/sfis", tags=["lenovo"])


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)