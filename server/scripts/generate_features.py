import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import requests
import json
from pathlib import Path
from tqdm import tqdm # For the progress bar
import time

# --- Configuration ---
# Use pathlib to create robust file paths
SERVER_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = SERVER_DIR / "data" / "products.json"
OUTPUT_FILE = SERVER_DIR / "data" / "features.json"

# --- Model Setup ---
# Load a pre-trained ResNet-50 model
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
# Set the model to evaluation mode (we're not training it)
model.eval()

# Remove the final classification layer to get the feature vector
# We access the layers of the model and take all but the last one
feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])

# --- Image Pre-processing ---
# Define the transformations that will be applied to each image.
# These must match the transformations the model was trained on.
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def extract_features(image_bytes):
    """Takes image bytes, preprocesses the image, and extracts its features."""
    try:
        # Open the image from byte data
        image = Image.open(requests.get(image_bytes, stream=True).raw).convert("RGB")
        # Apply the transformations
        input_tensor = preprocess(image)
        # Add a batch dimension (models expect a batch of images)
        input_batch = input_tensor.unsqueeze(0)

        # Use 'torch.no_grad()' to disable gradient calculations, saving memory and speeding up computation
        with torch.no_grad():
            features = feature_extractor(input_batch)
        
        # Flatten the feature vector and convert it to a standard Python list
        return features.flatten().tolist()
    except Exception as e:
        # If an image is broken or can't be opened, return None
        print(f"  - Could not process image. Error: {e}")
        return None

# --- Main Execution ---
if __name__ == "__main__":
    print("Starting feature generation process...")

    # Load the product data
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
            
            # Be polite to the server we are downloading images from
            time.sleep(0.1) 

    # Save the features to the output file
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(product_features, f, indent=4)

    print(f"\nFeature generation complete. {len(product_features)} vectors saved to {OUTPUT_FILE}")