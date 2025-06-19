# api/process_invoice.py
import tempfile
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from backend import process_invoice_pdf
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)  # Required for Vercel's serverless deployment

@app.post("/api/process_invoice")
async def process_invoice(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = process_invoice_pdf(tmp_path)

        return JSONResponse({
            "json_data": result,
            "ocr_text": result.get("combined_ocr_text", "")
        })
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
