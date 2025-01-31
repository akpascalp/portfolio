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

        prediction = model.predict(image)
        predicted_class = np.argmax(prediction)

        if predicted_class < 10:
            predicted_class = int(predicted_class)
        else:
            predicted_class = chr(predicted_class + 55)  # 10 -> 'A', 11 -> 'B', etc.

        return JSONResponse(content={"predictied": predicted_class})
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

    S = round(S, 2)
    I = round(I, 2)
    R = round(R, 2)

    S = max(0, min(S, 1))
    I = max(0, min(I, 1))
    R = max(0, min(R, 1))

    return {"day": day, "S": S, "I": I, "R": R, "beta": beta, "gamma": gamma, "population": population}
