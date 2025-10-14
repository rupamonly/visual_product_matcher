# visual_product_matcher

![React](https://img.shields.io/badge/React-Vite-blue?logo=react&style=for-the-badge)
![Python](https://img.shields.io/badge/Python-Flask-yellow?logo=python&style=for-the-badge)
![AI Model](https://img.shields.io/badge/AI_Model-ResNet50-orange?logo=pytorch&style=for-the-badge)

> An intelligent web application that finds visually similar products from a database using a deep learning model, built with **React, Python (Flask), and PyTorch**.

---

## 🚀 Features

- 🖼️ **Visual Search** – Upload any product image to find the closest matches in the database.
- 🤖 **AI-Powered Similarity** – Uses a pre-trained **ResNet-50** model to understand and compare the deep features of images.
- ⚡ **Fast & Responsive UI** – A modern frontend built with **React (Vite)** provides a seamless, mobile-first user experience.
- 📈 **Ranked Results** – Displays a grid of matching products sorted by their **Cosine Similarity** score.
- 🌐 **Full-Stack Architecture** – A clear separation between the Python backend (for AI processing) and the React frontend (for user interaction).

---

## 🛠️ Tech Stack

| Technology          | Purpose                                        |
|---------------------|------------------------------------------------|
| **React (Vite)** | Frontend UI and state management               |
| **Python (Flask)** | Backend server and REST API endpoints          |
| **PyTorch** | Deep learning framework for the AI model       |
| **Pillow** | Image processing in Python                     |
| **Scikit-learn** | Cosine similarity calculation                  |
| **Selenium** | Automated web scraping for the product dataset |
| **Axios** | Frontend HTTP requests to the backend API      |

---

## 🧠 AI Model & Method

The core of this application is its visual search capability, which is achieved through a feature extraction and comparison pipeline.

- **Model:** A pre-trained **ResNet-50** model from `torchvision`, which has learned rich feature representations from the ImageNet dataset.
- **Process:** The model is used as a **feature extractor** by removing its final classification layer. Each image is passed through the model to produce a high-dimensional vector.
- **Vector Size:** Each product image is converted into a **`2048`-dimension** feature vector.
- **Comparison:** **Cosine Similarity** is used to calculate the similarity between the user's uploaded image vector and all pre-computed vectors in the database. A higher score means the images are more visually alike.

---

## 📦 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/rupamonly/visual_product_matcher.git
cd visual-product-matcher
```
### 2️⃣ Backend Setup

```bash
cd server

# Create and activate a virtual environment
python -m venv venv
# On Windows: .\venv\Scripts\activate
# On macOS/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python app.py
```
The backend will be running at https://www.google.com/search?q=http://127.0.0.1:5000

### 3️⃣ Frontend Setup (in a new terminal)

```bash
cd client

# Install dependencies
npm install

# Run the frontend server
npm run dev
```
Open the browser at http://localhost:5173

---

## 📝 Planned Improvements

- [ ] Allow searching by pasting an image URL in addition to file upload.
- [ ] Add filters to narrow down search results by category.
- [ ] Implement pagination to handle larger datasets efficiently.
- [ ] Containerize the application with Docker for simplified deployment.
- [ ] Migrate feature vectors to a dedicated Vector Database (e.g., Pinecone, Weaviate) for enterprise-level scalability.

---

## 📜 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

This project is licensed under the **MIT License** – you are free modify it with proper attribution.

---

## 💡 Author

👤 **Rupam Bhakta**  
[![GitHub](https://img.shields.io/badge/GitHub-rupamonly-black?logo=github&style=for-the-badge)](https://github.com/rupamonly) [![LinkedIn](https://img.shields.io/badge/LinkedIn-Rupam_Bhakta-blue?logo=linkedin&style=for-the-badge)](https://www.linkedin.com/in/rupam-bhakta-6b8097262/)



