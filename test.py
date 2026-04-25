import cv2
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import joblib
import numpy as np
import os

# ── Load everything ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

mobilenet = models.mobilenet_v2(pretrained=True)
mobilenet.classifier = nn.Identity()
mobilenet.eval()

classifier = joblib.load(os.path.join(BASE_DIR,'model', 'classifier.pkl'))
classes    = joblib.load(os.path.join(BASE_DIR,'model', 'classes.pkl'))

print("Classes:", classes)
print("Model loaded successfully!")

# ── Same transform as training ──
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

# ── Open camera ──
cap = cv2.VideoCapture(0)   # 0 = default camera

print("Press Q to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame for prediction
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    img_tensor = transform(img).unsqueeze(0)

    # Extract features
    with torch.no_grad():
        features = mobilenet(img_tensor)

    # Predict
    features_np  = features.numpy()
    prediction   = classifier.predict(features_np)
    probabilities = classifier.predict_proba(features_np)
    confidence   = round(float(np.max(probabilities)) * 100, 2)
    label        = classes[prediction[0]]

    # Show result on frame
    cv2.putText(
        frame,
        f"{label} {confidence}%",  # text
        (20, 50),                  # position
        cv2.FONT_HERSHEY_SIMPLEX,  # font
        1,                         # size
        (0, 255, 0),               # color (green)
        2                          # thickness
    )

    # Show camera window
    cv2.imshow("ML Detection", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()