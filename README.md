# ❤️ Heart Disease Prediction using Interpretable Machine Learning Models

> Comparative analysis of interpretable machine learning algorithms for heart disease prediction using clinical data from the UCI Cleveland Heart Disease Dataset.

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)]()
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange.svg)]()
[![Status](https://img.shields.io/badge/Status-Research%20Project-success.svg)]()
[![Conference](https://img.shields.io/badge/Accepted-INCIP%202026-green.svg)]()

## 📖 Overview

Heart disease remains one of the leading causes of mortality worldwide. Early diagnosis and accurate risk prediction are critical for improving patient outcomes and supporting clinical decision-making.

This project presents a **comparative study of interpretable machine learning models** for heart disease prediction using structured clinical data. Multiple classification algorithms were evaluated under a unified experimental framework to analyze the trade-off between **predictive performance, model complexity, and interpretability**.

The research paper based on this work has been **accepted for presentation at INCIP-2026**.

---

## 🎯 Objectives

- Develop machine learning models for heart disease prediction.
- Compare the performance of multiple interpretable classifiers.
- Evaluate models using clinically relevant metrics.
- Analyze the balance between accuracy and explainability.
- Build a predictive framework suitable for healthcare decision support.

---

## 📂 Dataset

**Dataset:** UCI Cleveland Heart Disease Dataset

The dataset contains clinical parameters including:

- Age
- Sex
- Chest Pain Type
- Resting Blood Pressure
- Cholesterol
- Fasting Blood Sugar
- Resting ECG
- Maximum Heart Rate
- Exercise-induced Angina
- ST Depression
- Number of Major Vessels
- Thalassemia

**Target Variable:** Presence/Absence of Heart Disease

---

## 🧠 Machine Learning Models Evaluated

| Model | Description |
|-------|-------------|
| Logistic Regression | Interpretable probabilistic baseline model |
| Support Vector Machine | Maximum-margin classifier |
| Decision Tree | Rule-based interpretable classifier |
| Naive Bayes | Probabilistic classifier using Bayes theorem |
| Random Forest | Ensemble learning algorithm |

---

## ⚙️ Project Workflow

```text
Clinical Dataset
        ↓
Data Preprocessing
        ↓
Feature Engineering
        ↓
Train-Test Split
        ↓
Model Training
        ↓
Model Evaluation
        ↓
Comparative Analysis
        ↓
Prediction System
```

---

## 📊 Evaluation Metrics

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC Score

---

## 📈 Experimental Results

| Model | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|------|------|------|------|------|------|
| Logistic Regression | 91.4% | 92.1% | 90.7% | 91.4% | 95.2% |
| Support Vector Machine | 90.5% | 89.8% | 91.0% | 90.4% | 93.8% |
| Decision Tree | 89.2% | 90.1% | 88.4% | 89.2% | 91.2% |
| Naive Bayes | 92.6% | 93.4% | 91.8% | 92.6% | 94.8% |
| Random Forest | 91.8% | 92.5% | 93.1% | 92.8% | 95.5% |

### Key Findings

- **Naive Bayes** achieved the highest classification accuracy.
- **Random Forest** demonstrated superior recall performance.
- **Logistic Regression** provided strong predictive performance while maintaining interpretability.
- Interpretable machine learning models can achieve competitive performance in clinical prediction tasks.

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Jupyter Notebook

---

## 🚀 Future Improvements

- Integration of SHAP explainability methods.
- Hyperparameter optimization.
- Cross-validation based evaluation.
- Deployment as a web-based clinical decision support system.
- Validation using larger real-world clinical datasets.

---

## 📄 Research Publication

**Paper Title:**

> *Evaluation of Multiple Interpretable Machine Learning Models for Heart Disease Prediction Using Clinical Data*

📌 Accepted for presentation at **International Conference on Next Generation Communication & Information Processing (INCIP-2026)**.

---

## 👨‍💻 Authors

**Ayush Kumar**  
B.Tech Computer Science and Engineering  
SRM Institute of Science and Technology

**Mukesh Kumar Shah**  
B.Tech Computer Science and Engineering  
SRM Institute of Science and Technology

---

## ⭐ If you found this project useful, please consider giving it a star.
