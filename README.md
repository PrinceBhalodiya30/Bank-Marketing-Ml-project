# BankInvest AI 
### Intelligent Investment Prediction Engine

![BankInvest AI Banner](https://img.shields.io/badge/BankInvest-AI-0f172a?style=for-the-badge&logo=google-cloud&logoColor=3b82f6)

**BankInvest AI** is a premium machine learning solution designed for financial institutions to predict term deposit subscription success rates with high precision. Powered by a robust Random Forest algorithm, it analyzes comprehensive client demographic and financial data to drive actionable marketing insights.

---

## 🚀 Key Features

*   **Precision Analytics**: Advanced Random Forest Classifier trained on 45,000+ data points.
*   **Real-Time Processing**: Instant analysis of 16 distinct client variables.
*   **Enterprise Security**: Local data processing ensures complete client privacy.
*   **Modern Interface**: Glassmorphism-inspired UI designed for financial professionals.

## 🛠️ Installation & Setup

### Prerequisites
*   Python 3.8+
*   pip package manager

### 1. Clone & Install
Navigate to the project directory and install the required dependencies:

```bash
cd bank
pip install -r requirements.txt
```

### 2. Model Training (Optional)
The project comes with a pre-trained model. To retrain with fresh data:

```bash
python train_model.py
```

### 3. Launch Application
Start the predictive engine server:

```bash
cd flask_app
python app.py
```

The application will be accessible at: `http://127.0.0.1:5000`

## 📊 Usage Guide

1.  **Navigate to the Dashboard**: Open your browser to the local server address.
2.  **Input Client Data**: Fill in the "Client Analysis Interface" with the customer's details (Age, Job, Balance, etc.).
3.  **Run Prediction**: Click "Run Predictive Analysis".
4.  **View Insights**: Receive an instant probability assessment and recommended actions.

## 🔒 Security Note
This application runs entirely on your local machine. No client data is transmitted to external servers, making it compliant with strict financial data privacy regulations.

---
&copy; 2024 BankInvest AI. Market Intelligence Division.
