from fastapi import FastAPI
from src.pcb_v2 import router as pcb_v2

app = FastAPI(title="Multi-App FastAPI")

# Menyertakan semua router dari aplikasi yang berbeda
app.include_router(pcb_v2, prefix="/sfis", tags=["pcb_v2"])
