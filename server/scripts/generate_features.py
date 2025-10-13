import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import requests
import json
from pathlib import Path
from tqdm import tqdm
import time

# --- Configuration ---
SERVER_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = SERVER_DIR / "data" / "products.json"
OUTPUT_FILE = SERVER_DIR / "data" / "features.json"

# --- Model Setup ---
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()

feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])

# --- Image Pre-processing ---
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features(image_bytes):
    """Takes image bytes, preprocesses the image, and extracts its features."""
    try:
        
        image = Image.open(requests.get(image_bytes, stream=True).raw).convert("RGB")
        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0)

        with torch.no_grad():
            features = feature_extractor(input_batch)
        
        return features.flatten().tolist()
    except Exception as e:
        print(f"  - Could not process image. Error: {e}")
        return None

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting feature generation process...")

    with open(INPUT_FILE, 'r') as f:
        products = json.load(f)

    product_features = {}
    
    # Use tqdm to create a progress bar
    print(f"Processing {len(products)} images...")
    for product in tqdm(products, desc="Generating Features"):
        product_id = product.get("id")
        image_url = product.get("image_url")

        if product_id and image_url:
            print(f"\nProcessing product ID: {product_id}")
            features = extract_features(image_url)
            
            if features:
                product_features[product_id] = features
                print(f"  - Successfully generated feature vector.")
            
            time.sleep(0.1) 

    # Saving the features to the output file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(product_features, f, indent=4)

    print(f"\nFeature generation complete. {len(product_features)} vectors saved to {OUTPUT_FILE}")