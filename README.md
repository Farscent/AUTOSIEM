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

Dataset: 6.3M financial transactions (Kaggle Security Information and Event Management dataset).

Features Used: step, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest.

Model: XGBoost Classifier (optimized with Optuna).

Performance: ~99.9% accuracy, strong fraud detection with minimal false positives.

2. Behavioral Analytics

Detects fraud patterns such as:

Account Draining (emptying accounts in a single transaction).

Unusual Timing (fraud spikes outside business hours).

Top Offenders (ranking suspicious accounts).

3. Generative AI Integration

Gemini API generates:

Concise fraud alerts.

Automated attack timelines for investigations.

4. Visualization & Dashboard

KPIs: Total transactions, fraud count, fraud rate, fraud amount.

Visuals: Pie chart (account drained vs partial), bar chart (fraud by hour), scatter/violin plots.

Tables: Top offenders, live alerts, fraud drilldown.

UI/UX: Designed in Figma → professional, SOC-friendly, clean, and intuitive.

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

