# 🧾 **Fingerprint Identification System — Digital Image Processing Lab Mini Project**

---

## 🎓 Course Context
This project is developed as a part of the **Digital Image Processing Laboratory**.  
It demonstrates the application of computer vision techniques such as **feature extraction**, **image matching**, and **pattern recognition** using real-world biometric data — fingerprints.

---

## 🔍 Project Title
**Fingerprint Identification Using SIFT and FLANN (OpenCV Project)**

---

## 📘 Overview

This project implements a **Fingerprint Identification System** using **Digital Image Processing** techniques in **Python (OpenCV)**.  
It uses the **SIFT (Scale-Invariant Feature Transform)** algorithm for feature extraction and **FLANN-based matching** for comparing fingerprints.

The system analyzes unknown fingerprint images, compares them against a known database, and determines the **best match** or **duplicate entries** both visually and numerically.

---

## 🧠 Theory (Relevant to This Code)

### 🔹 1. Fingerprint Representation
- A fingerprint consists of **ridges** (raised skin lines) and **valleys** (spaces between ridges).  
- The **unique arrangement** of these ridge patterns identifies an individual.  
- Recognition is performed by **detecting and comparing key feature points** extracted from fingerprint images.

---

### 🔹 2. Feature Extraction (SIFT)
- **SIFT (Scale-Invariant Feature Transform)** detects **keypoints** that are invariant to scale, rotation, and illumination.  
- Each keypoint has a unique **descriptor vector** describing its local region.  
- These descriptors are used for comparing fingerprints between two images.

---

### 🔹 3. Feature Matching (FLANN Matcher)
- **FLANN (Fast Library for Approximate Nearest Neighbors)** efficiently matches descriptors between two images.  
- It uses **KNN (k-Nearest Neighbors)** search to find potential keypoint correspondences.  
- **Lowe’s Ratio Test** filters out false matches:  
  `distance(m) < 0.7 × distance(n)`  
  Only strong matches are retained.

---

### 🔹 4. Match Scoring
- The number of **good matches** represents the fingerprint similarity score.  
- Higher score → stronger similarity between fingerprints.  
- Threshold rule:
  - **Score > 20 → Match Found**
  - **Score ≤ 20 → Not a Match**

---

### 🔹 5. Visualization
- The function `cv2.drawMatches()` connects matched keypoints between two fingerprints.  
- Visual results help in manually validating the match accuracy.

---

### 🔹 6. Duplicate Detection
- The code also checks **unknown fingerprints** against each other to identify duplicates.  
- Useful for verifying datasets or criminal record duplication.

---

## ⚙️ How It Works (Code Logic)

| Step | Description |
|------|--------------|
| **1. Load Data** | Loads fingerprint images from `database/` and `unknowns/` folders. |
| **2. Extract Features** | SIFT detects keypoints and computes feature descriptors. |
| **3. Match Features** | FLANN performs KNN-based matching using descriptor vectors. |
| **4. Compute Score** | Counts the number of good matches to determine similarity. |
| **5. Display Results** | Shows visual comparison of matching features using OpenCV. |
| **6. Duplicate Check** | Compares all unknown fingerprints for duplicates. |

---

