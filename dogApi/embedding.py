import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import torch
import torchvision.transforms as T
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image
import numpy as np

device = "cpu"

model = resnet50(weights=ResNet50_Weights.DEFAULT)
model.fc = torch.nn.Identity()
model.eval().to(device)

transform = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def image_to_vector(img: Image.Image) -> np.ndarray:
    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        feat = model(x).cpu().numpy()[0]
    feat = feat / np.linalg.norm(feat)
    return feat.astype("float32")
