from fastapi import FastAPI
from batch.router import router as batch
from pcb.router import router as pcb
from pcb_v2.router import router as pcb_v2
from batch_v2.router import router as batch_v2

app = FastAPI(title="Multi-App FastAPI")

# Menyertakan semua router dari aplikasi yang berbeda
app.include_router(batch, prefix="/batch", tags=["batch"])
app.include_router(pcb, prefix="/pcb", tags=["pcb"])
app.include_router(pcb_v2, prefix="/sfis", tags=["pcb_v2"])
app.include_router(batch_v2, prefix="/batch_v2", tags=["batch_v2"])
