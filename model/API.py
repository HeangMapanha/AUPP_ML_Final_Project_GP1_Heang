from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import base64
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io
import os

app = FastAPI()
mobilenet = models.mobilenet_v2(pretrained=True)
mobilenet.classifier = nn.Identity()
mobilenet.eval()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
classifier = joblib.load(os.path.join(BASE_DIR, 'classifier.pkl'))
classes    = joblib.load(os.path.join(BASE_DIR, 'classes.pkl'))

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

class ImageData(BaseModel):
    image: str

@app.post("/predict")
async def predict(data: ImageData):
    try:
        image_data = data.image
        if "," in image_data:
            image_data = image_data.split(",")[1]

        img_bytes = base64.b64decode(image_data)
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # CNN features only (1280)
        img_tensor = transform(pil_img).unsqueeze(0)
        with torch.no_grad():
            features = mobilenet(img_tensor).numpy()

        prediction    = classifier.predict(features)
        probabilities = classifier.predict_proba(features)
        confidence    = round(float(np.max(probabilities)) * 100, 2)
        label         = classes[prediction[0]]
        return {"result": label, "confidence": confidence}
    except Exception as e:
        print("ERROR:", str(e))
        return {"result": "Error", "confidence": 0, "message": str(e)}