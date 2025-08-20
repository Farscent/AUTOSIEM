# AutoSIEM 🛡️

Integrating Machine Learning & Generative AI on SIEM Tools for Automated Cybersecurity Surveillance

## 📌 Overview

AutoSIEM is a prototype Security Information and Event Management (SIEM) system enhanced with machine learning and generative AI. It is designed to automate fraud detection, reduce analyst workload, and provide real-time, human-readable insights for Security Operations Center (SOC) teams.

This project was developed during the UGM DCSE Summer Course 2025 and received an Honorable Mention 🏅.

## 🚨 Problem Statement

Traditional SIEM tools rely heavily on manual rule creation and human analysis, making them less effective against sophisticated or novel cyberattacks. With increasing volumes of user activity data, analysts need automated, intelligent systems to detect fraud and anomalies in real time. 

## 🎯 Objectives

Automate fraud detection within SIEM data using machine learning.

Identify behavioral patterns such as account draining, unusual timing, and inconsistent activity.

Integrate generative AI (Gemini API) to generate real-time, human-readable summaries and attack timelines.

Deliver an intuitive SIEM dashboard inspired by industry tools like Splunk.

## 🛠️ Technical Approach
1. Machine Learning Pipeline

Dataset: 6.3M financial transactions (Kaggle Security Information and Event Management dataset). --> https://www.kaggle.com/datasets/ibtasamahmad/security-information-and-event-management

Features Used: step, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest.

Model: XGBoost Classifier (optimized with Optuna).

Performance: ~99.9% accuracy, strong fraud detection with minimal false positives.

<img width="1090" height="615" alt="image" src="https://github.com/user-attachments/assets/f9353f76-ef4d-403e-8a5e-168fc85a13f0" />

2. Behavioral Analytics

Detects fraud patterns such as:

Account Draining (emptying accounts in a single transaction).

Unusual Timing (fraud spikes outside business hours).

Top Offenders (ranking suspicious accounts).

3. Generative AI Integration

Gemini API generates:

Concise fraud alerts.

Automated attack timelines for investigations.

<img width="1067" height="582" alt="image" src="https://github.com/user-attachments/assets/ed5b3382-36e8-4331-9df6-e5ce5555fd61" />

4. Visualization & Dashboard

KPIs: Total transactions, fraud count, fraud rate, fraud amount.

Visuals: Pie chart (account drained vs partial), bar chart (fraud by hour), scatter/violin plots.

Tables: Top offenders, live alerts, fraud drilldown.

UI/UX: Designed in Figma → professional, SOC-friendly, clean, and intuitive.

<img width="948" height="531" alt="image" src="https://github.com/user-attachments/assets/51725863-15b1-4f63-9415-4b2bd6e8c875" />

<img width="929" height="560" alt="image" src="https://github.com/user-attachments/assets/b5dfc52c-39e3-428e-8b2e-bf978a67cdd1" />

<img width="955" height="552" alt="image" src="https://github.com/user-attachments/assets/78910dab-6700-438d-bddd-46c0e88f7b42" />

<img width="970" height="533" alt="image" src="https://github.com/user-attachments/assets/7dc5e0d8-deac-4c7b-b46f-89a3a91e5b64" />

<img width="932" height="549" alt="image" src="https://github.com/user-attachments/assets/cb0aa12c-6b73-41bb-abd7-0850c8ea70ea" />

## 📊 Prototype

Pages: Login, Dashboard, Fraud, Analytics, Account.

Tools Used: Python (XGBoost, Optuna, Pandas, Plotly), Gemini API, Figma.

## 👥 Team

Farhan Adiwidya Pradana

M. Ahsan Wiryawan

Silvester Taffarel Irza

Nadja Donosepoetro

## 🏆 Acknowledgements

This project was developed as part of the UGM DCSE Summer Course 2025 organized by DCSE FMIPA UGM.
Special thanks to the committee, lecturers, and mentors for their guidance and support.

