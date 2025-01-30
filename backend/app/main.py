import cv2
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = tf.keras.models.load_model('app/models/handwriting.keras')

def preprocess_image(image_bytes):
    """Convertit une image en bytes en format compatible CNN"""
    image = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)

    if image.shape[-1] == 4:
        # Extraire les canaux et gérer l'alpha
        b, g, r, a = cv2.split(image)
        alpha_mask = a / 255.0
        b = (b * alpha_mask + 255 * (1 - alpha_mask)).astype(np.uint8)
        g = (g * alpha_mask + 255 * (1 - alpha_mask)).astype(np.uint8)
        r = (r * alpha_mask + 255 * (1 - alpha_mask)).astype(np.uint8)
        image = cv2.merge([b, g, r])

    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Binarisation et redimensionnement
    image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    image = cv2.resize(image, (28, 28), interpolation=cv2.INTER_AREA)
    # Normaliser les pixels entre 0 et 1
    image = image.astype(np.float32) / 255.0

    threshold_value = 0.1
    image = np.where(image > threshold_value, 1.0, 0.0)

    image_display = (image * 255).astype(np.uint8)
    cv2.imwrite('image_thresholded.jpg', image_display)

    return image.reshape(1, 28, 28, 1)  # Format compatible CNN

@app.post("/recognition/")
async def recognition(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        image = preprocess_image(image_bytes)
        prediction = model.predict(image)
        predicted_digit = np.argmax(prediction, axis=1)[0]

        return JSONResponse(content={"digit": int(predicted_digit)})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
