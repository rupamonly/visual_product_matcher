import json
from pathlib import Path
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import io

app = Flask(__name__)
CORS(app)

# --- AI Model & Data Loading ---
print("Loading model and data... This may take a moment.")

SERVER_DIR = Path(__file__).resolve().parent
PRODUCTS_FILE = SERVER_DIR / "data" / "products.json"
FEATURES_FILE = SERVER_DIR / "data" / "features.json"

with open(PRODUCTS_FILE, 'r') as f:
    product_data = json.load(f)
with open(FEATURES_FILE, 'r') as f:
    product_features = json.load(f)

product_id_map = {item['id']: item for item in product_data}

product_ids = list(product_features.keys())
feature_vectors = np.array([product_features[pid] for pid in product_ids])

# Load pre-trained ResNet-50 model
model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
model.eval()
feature_extractor = torch.nn.Sequential(*list(model.children())[:-1])

# Define image transformations
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
print("Model and data loaded successfully!")


def extract_features_from_image(image_bytes):
    """Extracts a feature vector from an image in byte format."""
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0)

        with torch.no_grad():
            features = feature_extractor(input_batch)
        
        return features.flatten().numpy()
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# --- API Endpoints ---
@app.route('/')
def index():
    return "Hello, the Visual Matcher API is running!"

@app.route('/api/find-similar', methods=['POST'])
def find_similar():
    """Receives an image, finds similar products, and returns them."""
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()

    # 1. Extract features from the user's uploaded image
    query_features = extract_features_from_image(image_bytes)
    if query_features is None:
        return jsonify({"error": "Could not process the uploaded image"}), 500
    
    # 2. Calculate Cosine Similarity
    similarities = cosine_similarity(query_features.reshape(1, -1), feature_vectors)
    
    # 3. Get top 10 most similar products
    # `similarities[0]` contains the scores. `argsort` finds the indices that would sort the array.
    # `[::-1]` reverses it to get descending order.
    top_indices = np.argsort(similarities[0])[::-1][:15]

    # 4. Format the results
    results = []
    for i in top_indices:
        product_id = product_ids[i]
        product_info = product_id_map.get(product_id)
        if product_info:
            result_item = {
                "id": product_info["id"],
                "name": product_info["name"],
                "category": product_info["category"],
                "image_url": product_info["image_url"],
                "similarity_score": float(similarities[0][i])
            }
            results.append(result_item)
            
    return jsonify(results)

# --- Run the App ---
if __name__ == '__main__':
    app.run(debug=True)
















# from flask import Flask, request, jsonify
# from flask_cors import CORS

# # --- Initialize the Flask App ---
# app = Flask(__name__)
# # Enable CORS for all routes, allowing our frontend to communicate with this backend
# CORS(app)


# # --- API Endpoints ---

# @app.route('/')
# def index():
#     """A simple endpoint to test if the server is running."""
#     return "Hello, the Visual Matcher API is running!"

# @app.route('/api/find-similar', methods=['POST'])
# def find_similar():
#     """
#     The main endpoint that receives an image and returns similar products.
#     (This is just a placeholder for now).
#     """
#     # Check if an image file is present in the request
#     if 'image' not in request.files:
#         return jsonify({"error": "No image file provided"}), 400

#     image_file = request.files['image']
    
#     # For now, we'll just confirm we received the file
#     print(f"Received image: {image_file.filename}")

#     # TODO: Add the actual image processing and similarity search logic here.

#     # Return a dummy success response
#     return jsonify({
#         "message": "Image received successfully!",
#         "filename": image_file.filename,
#         "similar_products": [] # The real results will go here
#     })


# # --- Run the App ---
# if __name__ == '__main__':
#     # Running in debug mode provides helpful error messages
#     app.run(debug=True)