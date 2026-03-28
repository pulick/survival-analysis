# 🧬 Survival Analysis & Risk Prediction using Gene Expression (TCGA-BRCA)

## 🌐 Live Demo

👉 **Try the app here:**
https://survival-analysis-9gze2w98kxusgx6eclcj7x.streamlit.app/

---

## 📌 Project Overview

This project predicts **high-risk vs low-risk breast cancer patients** using gene expression data from **TCGA-BRCA (Breast Cancer subset of TCGA)**.

The Cancer Genome Atlas is a large-scale cancer genomics database containing multiple cancer types.
In this project, we specifically use **TCGA-BRCA** to ensure consistent disease biology and meaningful modeling.

The pipeline integrates:

* Survival Analysis (Kaplan–Meier, Cox Model)
* Feature Selection (LASSO)
* Machine Learning (XGBoost, Random Forest, Neural Network)
* Deployment using **Streamlit**

---

## 🎯 Objectives

* Analyze survival patterns in breast cancer patients
* Identify key genes associated with survival
* Build ML models to classify **high-risk vs low-risk patients**
* Deploy a clinical-style application for real-time prediction

---

## 📂 Dataset

**Source:** TCGA-BRCA

### Data Used:

* Clinical data (survival time, event)
* Gene expression data (RNA-seq)

### Final Dataset:

* 41 patients
* 20 selected genes
* Target: `risk_label`

  * 1 → High risk
  * 0 → Low risk

---

## ⚙️ Methodology

### 1️⃣ Data Preprocessing

* Cleaned missing values (`"--"` → NaN)
* Converted survival columns to numeric
* Created:

  * `time` (survival duration)
  * `event` (death indicator)

---

### 2️⃣ Survival Analysis

* Kaplan–Meier estimation
* Cox Proportional Hazards model
* L1 regularization (LASSO) for feature selection

---

### 3️⃣ Feature Selection

```text
~60,000 genes → Top 500 → LASSO → Top 20 genes
```

---

### 4️⃣ Risk Label Creation

```python
risk_label = (time < median(time)).astype(int)
```

---

### 5️⃣ Machine Learning Models

* XGBoost (**ROC-AUC: 0.79**)
* Neural Network (**0.76**)
* Random Forest (**0.71**)

### Evaluation:

* Cross-validation (cv=5)
* ROC-AUC metric

---

## 🚀 Deployment (Streamlit App)

A **Streamlit web application** was developed to simulate a clinical decision-support tool.

### Features:

* Upload patient gene expression data (CSV)
* Predict survival risk (High / Low)
* Display prediction probability
* Provide model-based insights

👉 **Live App:**
https://survival-analysis-9gze2w98kxusgx6eclcj7x.streamlit.app/

---

## 📊 Results

| Model          | ROC-AUC  |
| -------------- | -------- |
| XGBoost        | **0.79** |
| Neural Network | 0.76     |
| Random Forest  | 0.71     |

---

## 🧠 Key Insights

* Gene expression data can predict patient survival risk
* Multiple genes contribute to cancer progression (not just BRCA1/2)
* XGBoost achieved the best performance
* Combining survival analysis with ML improves interpretability

---

## ⚠️ Limitations

* Small sample size (41 patients)
* Risk label simplifies survival (does not fully account for censoring)

---

## 🚀 Future Work

* Use larger datasets
* Apply deep learning survival models (e.g., DeepSurv)
* Integrate multi-omics data
* External validation on independent cohorts

---

## 🛠️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* XGBoost
* Lifelines
* Streamlit

---

## 📌 Conclusion

This project demonstrates an end-to-end pipeline from genomic data to deployment.
It highlights how **machine learning and survival analysis can support clinical decision-making** in breast cancer.

---

## 👨‍💻 Author

**Abraham Pulickakudiyil**
Master’s Student – Life Science Informatics

---

⭐ If you like this project, consider giving it a star!
