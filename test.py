import cv2
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import joblib
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
mobilenet = models.mobilenet_v2(pretrained=True)
mobilenet.classifier = nn.Identity()
mobilenet.eval()

classifier = joblib.load(os.path.join(BASE_DIR, 'model', 'classifier.pkl'))
classes    = joblib.load(os.path.join(BASE_DIR, 'model', 'classes.pkl'))
print("Classes:", classes)
print("Model loaded successfully!")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

cap = cv2.VideoCapture(0)
print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # CNN features only (1280)
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        features = mobilenet(img_tensor).numpy()

    prediction    = classifier.predict(features)
    probabilities = classifier.predict_proba(features)
    confidence    = round(float(np.max(probabilities)) * 100, 2)
    label         = classes[prediction[0]]

    cv2.putText(frame, f"{label} {confidence}%", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("ML Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()