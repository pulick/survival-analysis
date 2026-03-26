# survival-analysis

# 🧬 Survival Analysis & Risk Prediction using Gene Expression (TCGA-BRCA)

## 📌 Project Overview

This project focuses on predicting **high-risk vs low-risk breast cancer patients** using gene expression data from the TCGA-BRCA dataset.

The workflow combines:

* Survival Analysis (Kaplan–Meier, Cox Model)
* Feature Selection (LASSO)
* Machine Learning (XGBoost, Random Forest, Neural Network)

---

## 🎯 Objectives

* Analyze patient survival using clinical and genomic data
* Identify important genes associated with survival
* Build ML models to classify patients into **high-risk** and **low-risk** groups
* Compare model performance using ROC-AUC

---

## 📂 Dataset

Data source: **TCGA-BRCA (The Cancer Genome Atlas)**

### Data Types Used:

* Clinical data (survival information)
* Gene expression data (RNA-seq)

### Final Dataset:

* **41 patients**
* **20 selected genes (features)**
* Target: `risk_label` (0 = low risk, 1 = high risk)

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

#### 🔹 Kaplan–Meier Estimation

* Estimated survival probability over time

#### 🔹 Cox Proportional Hazards Model

* Modeled relationship between gene expression and survival risk
* Used **L1 regularization (LASSO)** for feature selection

---

### 3️⃣ Feature Selection

Pipeline:

```
~60,000 genes → Top 500 (variance) → LASSO → Top 20 genes
```

Selected genes include:

* CD44
* GSTP1
* IFITM3
* DDR1
* S100A7
* SPP1
  (*and others*)

---

### 4️⃣ Risk Label Creation

Converted survival into classification:

```python
risk_label = (time < median(time)).astype(int)
```

* **1 → High risk (short survival)**
* **0 → Low risk (long survival)**

---

### 5️⃣ Machine Learning Models

#### 🔹 XGBoost

* Gradient boosting model
* Handles nonlinear relationships
* Best performance

#### 🔹 Random Forest

* Ensemble of decision trees
* Baseline comparison model

#### 🔹 Neural Network

* Captures complex feature interactions

---

### 6️⃣ Model Evaluation

Used:

* **ROC-AUC score**
* **Cross-validation (cv=5)** for reliability

---

## 📊 Results

| Model          | ROC-AUC    |
| -------------- | ---------- |
| XGBoost        | **0.79** ✅ |
| Neural Network | 0.76       |
| Random Forest  | 0.71       |

---

### 📈 ROC Curve

* XGBoost achieved the best separation between high-risk and low-risk patients
* Demonstrates strong predictive capability

---

## 🧠 Key Insights

* Gene expression data can effectively predict patient risk
* XGBoost outperformed other models
* Feature selection was critical due to small dataset size
* Survival analysis provided biologically meaningful insights

---

## ⚠️ Limitations

* Small sample size (41 patients)
* Limited statistical significance in some genes
* Risk label simplifies survival (ignores censoring)

---

## 🚀 Future Work

* Use larger datasets
* Apply DeepSurv (deep learning for survival analysis)
* Incorporate multi-omics data
* External validation on independent datasets

---

## 🛠️ Tech Stack

* Python
* Pandas, NumPy
* Scikit-learn
* XGBoost
* Lifelines (survival analysis)
* Matplotlib

---

## 📌 Conclusion

This project demonstrates a complete pipeline from raw genomic data to predictive modeling.
It highlights how **machine learning + survival analysis** can be combined to identify high-risk cancer patients and important biological markers.

---

## 👨‍💻 Author

**Abraham Pulickakudiyil**
Master’s Student – Life Science Informatics

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
