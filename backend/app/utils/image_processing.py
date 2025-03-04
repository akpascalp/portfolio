import cv2
import numpy as np

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
