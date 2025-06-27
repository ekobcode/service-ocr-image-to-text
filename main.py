from fastapi import FastAPI, Request, Depends, UploadFile, File, HTTPException, Query
from middleware.auth import api_key_auth
from services.ocr_image import ocr_from_url, ocr_from_file
from core.config import MAX_FILE_SIZE_MB, ALLOWED_IMAGE_CONTENT_TYPES
import time

app = FastAPI(title="Advanced OCR Image to Text")

@app.get("/image-to-text/url")
async def image_to_text_from_url(
    request: Request,
    url: str = Query(..., description="URL of the image"),
    output: str = Query("clean", description="Text format: 'clean' or 'raw'"),
    _: str = Depends(api_key_auth)
):
    start_time = time.time()
    result = ocr_from_url(url)
    response_time_ms = int((time.time() - start_time) * 1000)

    print(
        f"[OCR URL] IP: {request.client.host} | URL: {url} | Status: {result['status']} | "
        f"Message: {result['message']} | ResponseTime: {response_time_ms}ms"
    )

    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["message"])

    return result


@app.post("/image-to-text/file")
async def image_to_text_from_file(
    file: UploadFile = File(...),
    request: Request = None,
    output: str = Query("clean", description="Text format: 'clean' or 'raw'"),
    _: str = Depends(api_key_auth)
):
    if file.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 5MB.")

    start_time = time.time()
    result = ocr_from_file(content)
    response_time_ms = int((time.time() - start_time) * 1000)

    print(
        f"[OCR FILE] IP: {request.client.host} | Filename: {file.filename} | "
        f"ContentType: {file.content_type} | Status: {result['status']} | "
        f"Message: {result['message']} | ResponseTime: {response_time_ms}ms"
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result


@app.get("/ping")
async def ping():
    return {
        "status": "ok",
        "message": "pong",
        "timestamp": int(time.time() * 1000)
    }
