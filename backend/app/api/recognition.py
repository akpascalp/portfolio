import tensorflow as tf
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.utils.image_processing import preprocess_image

router = APIRouter()

MODEL = tf.keras.models.load_model('app/models/handwriting.keras')

@router.post("/")
async def recognition(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = preprocess_image(image_bytes)
        prediction = MODEL.predict(image)[0]
        top_indices = prediction.argsort()[-3:][::-1]
        top_predictions = [(int(idx) if idx < 10 else chr(idx + 55), float(prediction[idx])) for idx in top_indices]
        results = [{"class": pred[0], "score": round(pred[1] * 100, 2)} for pred in top_predictions]
        return JSONResponse(content={"predictions": results})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
