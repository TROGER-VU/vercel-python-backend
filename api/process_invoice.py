from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)  # Required for Vercel

@app.post("/api/process_invoice")
async def process_invoice(file: UploadFile = File(...)):
    print(f"[DEBUG] Received file: {file.filename}")
    return JSONResponse({
        "json_data": {"status": "success", "message": "Dummy processing complete"},
        "ocr_text": "This is a dummy OCR result."
    })
