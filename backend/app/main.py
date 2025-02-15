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
        b, g, r, a = cv2.split(image)
        alpha_mask = a / 255.0
        b = (b * alpha_mask + 255 * (1 - alpha_mask)).astype(np.uint8)
        g = (g * alpha_mask + 255 * (1 - alpha_mask)).astype(np.uint8)
        r = (r * alpha_mask + 255 * (1 - alpha_mask)).astype(np.uint8)
        image = cv2.merge([b, g, r])

    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    image = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU)[1]
    image = cv2.resize(image, (28, 28), interpolation=cv2.INTER_AREA)
    image = image.astype(np.float32) / 255.0

    threshold_value = 0.9
    image = np.where(image > threshold_value, 1.0, 0.0)

    return image.reshape(1, 28, 28, 1)

@app.post("/recognition/")
async def recognition(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        image = preprocess_image(image_bytes)

        prediction = model.predict(image)[0]
        top_indices = prediction.argsort()[-3:][::-1]
        top_predictions = [(int(idx) if idx < 10 else chr(idx + 55), float(prediction[idx])) for idx in top_indices]

        results = [{"class": pred[0], "score": round(pred[1] * 100, 2)} for pred in top_predictions]

        return JSONResponse(content={"predictions": results})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

def sir_step(S, I, R, beta, gamma):
    new_I = beta * S * I
    new_R = gamma * I
    new_S = -new_I
    return S + new_S, I + new_I - new_R, R + new_R

def get_R_value(S: float, I: float):
    S = min(max(S, 0), 1)
    I = min(max(I, 0), 1 - S)
    R = 1 - (S + I)
    return R

@app.get("/sir")
async def step_simulation(S: float, I: float, beta: float, gamma: float, day: int, population: int, R: float | None = None):
    if R is None:
        R = get_R_value(S, I)
    # Mise à jour du modèle SIR pour un jour
    S, I, R = sir_step(S, I, R, beta, gamma)
    day += 1

    S = round(S, 3)
    I = round(I, 3)
    R = round(R, 3)

    S = max(0, min(S, 1))
    I = max(0, min(I, 1))
    R = max(0, min(R, 1))

    return {"S": S, "I": I, "R": R, "beta": beta, "gamma": gamma, "day": day, "population": population}
