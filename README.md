# <p align="center"><img src="assets/logo.png" width="150" alt="GREENGROW Logo"><br>GREENGROW</p>

### <p align="center">The Ultimate AI-Powered Smart Farming & Gardening Ecosystem</p>

<p align="center">
  <img src="assets/banner.png" alt="GREENGROW Banner" width="100%">
</p>

---

## 🌟 Overview

**GREENGROW** is a comprehensive, modern platform designed to empower farmers and gardening enthusiasts. By blending cutting-edge AI with intuitive management tools, we provide a one-stop ecosystem for plant care, community engagement, and commerce. Whether you're a commercial farmer or a home gardener, GREENGROW brings technology to your roots.

---

## ✨ Key Features

- **🌱 Smart Garden Management**: Effortlessly track your plants, manage gardening tasks, and monitor growth cycles.
- **🔍 AI-Powered Diagnostics**:
  - **Plant Disease Detection**: Identify plant issues instantly using a custom Keras-based ML model or Google Gemini AI.
  - **Crop Recommendations**: Receive data-driven crop suggestions tailored to your soil and environmental conditions.
  - **Plant Encyclopedia**: Access a vast library of care guides and plant facts via the Plant.id API.
- **🛒 Community Marketplace**: Securely buy and sell seeds, produce, and supplies with integrated **Razorpay** payments.
- **💬 Real-time Connectivity**: Connect with expert farmers and peers through instant messaging powered by **Django Channels** and WebSockets.
- **📱 Social Feed**: Share your gardening success, tips, and updates with a vibrant community.
- **🌍 Bilingual Interface**: Accessible in both **English** and **Tamil** (தமிழ்) to support local farming communities.

---

## 🛠 Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | ![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) |
| **Frontend** | ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=flat&logo=tailwind-css&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) |
| **Databases** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=flat&logo=mongodb&logoColor=white) |
| **AI / ML** | ![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=flat&logo=google&logoColor=white) ![Scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=flat&logo=scikit-learn&logoColor=white) |
| **Real-time** | ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=flat&logo=redis&logoColor=white) ![Channels](https://img.shields.io/badge/Django_Channels-092E20?style=flat&logo=django&logoColor=white) |
| **Payments** | ![Razorpay](https://img.shields.io/badge/Razorpay-020425?style=flat&logo=razorpay&logoColor=528FF0) |
| **Cloud** | ![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=flat&logo=cloudinary&logoColor=white) ![Render](https://img.shields.io/badge/Render-46E3B7?style=flat&logo=render&logoColor=black) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js & npm (for Tailwind builds)
- Redis server (required for Chat features)

### Installation

1. **Clone the Project**:
   ```bash
   git clone https://github.com/Vinoth-R-2003/GREENGROW.git
   cd GREENGROW/FP
   ```

2. **Setup Environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Configure Variables**:
   Create a `.env` file in the `FP/` folder:
   ```env
   SECRET_KEY=your_key
   DEBUG=True
   DATABASE_URL=postgres://... (Optional)
   MONGODB_URI=your_mongo_uri
   GEMINI_API_KEY=your_gemini_key
   PLANT_ID_API_KEY=your_plant_id_key
   RAZORPAY_KEY_ID=your_razorpay_id
   RAZORPAY_KEY_SECRET=your_razorpay_secret
   ```

4. **Run Migrations & Seed Data**:
   ```bash
   python manage.py migrate
   python manage.py seed_plants
   python manage.py seed_items
   ```

5. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

---

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License.

---
<p align="center">Built with 🌿 by <a href="https://github.com/Vinoth-R-2003">Vinoth R</a></p>
