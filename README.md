# Project Overview: Brazil Economic Intelligence Platform

## 1. Project Summary

**Project Name:** Brazil Economic Intelligence Platform

**Objective:**
Develop an end-to-end data platform that automatically collects Brazilian macroeconomic indicators from public sources, stores and transforms the data in a structured database, generates business-oriented analyses and dashboards, and applies machine learning models to identify and predict economic conditions.

The project aims to demonstrate skills relevant to:

* Data Engineering
* Data Analysis
* Data Science
* Business Intelligence

while solving a realistic economic intelligence problem similar to those found in banks, fintechs, consulting firms, and corporate planning departments.

---

## 2. Business Problem

Economic indicators are scattered across multiple government databases and are frequently updated.

Analysts often spend considerable time:

* Collecting data manually
* Cleaning datasets
* Merging indicators
* Producing reports
* Monitoring economic trends

This project automates the entire process and creates a centralized platform capable of:

* Monitoring Brazil's economic conditions
* Identifying relationships between indicators
* Supporting decision-making
* Generating forecasts

---

## 3. Project Architecture

```text
Public Data Sources
(BACEN, IBGE, IPEA)

        │
        ▼

Data Ingestion Pipeline

        │
        ▼

PostgreSQL Database

        │
        ▼

Data Transformation Layer
(SQL + Python)

        │
        ▼

Analytics Layer

        ├─────────────┐
        ▼             ▼

Dashboard      Machine Learning

        └──────┬──────┘
               ▼

Economic Intelligence Platform
```

---

# Phase 1 – Data Engineering

## Goal

Build a robust data pipeline capable of collecting and storing macroeconomic data automatically.

---

## 1.1 Data Source Selection

### Initial Sources

#### BACEN SGS API

Examples:

* SELIC Rate
* IBC-Br
* Exchange Rate
* Credit Indicators
* Default Rates

#### Optional Future Sources

* IBGE
* IPEA Data
* Tesouro Nacional
* B3

---

## 1.2 Data Ingestion

### Objective

Automatically retrieve economic indicators.

### Implementation

Python scripts will:

* Connect to APIs
* Download data
* Validate responses
* Standardize formats

### Technologies

* Python
* Requests
* Pandas

---

## 1.3 Database Design

### Objective

Create a structured storage layer.

### Implementation

Use PostgreSQL to store:

#### Indicator Metadata

```text
indicator_id
indicator_name
source
frequency
unit
```

#### Indicator Values

```text
date
indicator_id
value
```

---

## 1.4 ETL Process

### Objective

Transform raw data into analysis-ready datasets.

### Tasks

* Handle missing values
* Standardize dates
* Remove duplicates
* Create derived indicators

Examples:

```text
Inflation YoY

Credit Growth Rate

SELIC Variation

Economic Momentum
```

---

## 1.5 Workflow Orchestration

### Objective

Automate updates.

### Implementation

Airflow DAGs will:

1. Collect new data
2. Validate data
3. Load database
4. Execute transformations

---

## 1.6 Containerization

### Objective

Improve reproducibility.

### Implementation

Docker containers for:

* PostgreSQL
* Airflow
* Application code

---

# Phase 2 – Data Analysis

## Goal

Understand the behavior of economic indicators and identify meaningful relationships.

---

## 2.1 Exploratory Data Analysis

### Questions

* How has inflation evolved over time?
* How does SELIC react to inflation?
* How does economic activity respond to interest rates?

### Deliverables

* Time series visualizations
* Summary statistics
* Correlation analysis

---

## 2.2 Lag Analysis

### Objective

Investigate delayed effects.

Examples:

* Does SELIC affect inflation after 6 months?
* Does credit growth anticipate economic expansion?

Methods:

* Cross-correlation
* Lagged features

---

## 2.3 Economic Cycle Analysis

### Objective

Identify economic phases.

Potential labels:

```text
Expansion

Slowdown

Recession

Recovery
```

Methods:

* Rule-based classification
* Historical economic periods

---

## 2.4 Dashboard Development

### Objective

Provide interactive visualization.

### Suggested Dashboard Sections

#### Macroeconomic Overview

* Inflation
* SELIC
* Exchange Rate
* IBC-Br

#### Credit Market

* Credit Growth
* Default Rates

#### Economic Cycle Monitor

* Current phase
* Historical phases

### Technologies

* Power BI

or

* Tableau

---

# Phase 3 – Data Science

## Goal

Develop predictive models using economic indicators.

---

## 3.1 Problem Definition

Two possible approaches:

### Classification

Predict economic conditions:

```text
Expansion
Recovery
Slowdown
Recession
```

### Regression

Predict future values of:

* Inflation
* SELIC
* IBC-Br

---

## 3.2 Feature Engineering

Create features such as:

```text
Lagged indicators

Moving averages

Growth rates

Volatility measures

Rolling statistics
```

---

## 3.3 Model Development

Baseline:

* Logistic Regression
* Random Forest

Advanced:

* XGBoost
* LightGBM

Time Series:

* Prophet
* XGBoost Forecasting

---

## 3.4 Model Evaluation

### Classification Metrics

* Accuracy
* Precision
* Recall
* F1-score

### Regression Metrics

* RMSE
* MAE
* MAPE

---

## 3.5 Model Explainability

### Objective

Understand model decisions.

### Techniques

* SHAP
* Feature Importance

Questions:

* Which indicators contribute most to predictions?
* Which variables anticipate economic slowdowns?

---

# Phase 4 – Documentation & Communication

## Goal

Present results in a professional manner.

---

## 4.1 Main Repository README

Contents:

* Project overview
* Architecture diagram
* Technologies
* Results
* Dashboard screenshots
* Model performance

---

## 4.2 Data Engineering Documentation

Separate README:

* Database schema
* ETL design
* Airflow workflows
* Docker setup

---

## 4.3 Data Analysis Documentation

Separate README:

* Business questions
* Visualizations
* Insights
* Conclusions

---

## 4.4 Machine Learning Documentation

Separate README:

* Feature engineering
* Modeling process
* Evaluation
* Explainability

---

# Expected Skills Demonstrated

## Data Engineering

* Python
* PostgreSQL
* SQL
* ETL
* Airflow
* Docker
* API Integration

## Data Analysis

* EDA
* Statistics
* Data Visualization
* Business Analysis
* Dashboard Development

## Data Science

* Machine Learning
* Feature Engineering
* Model Evaluation
* Time Series Analysis
* Explainable AI (SHAP)

---

# Final Deliverable

A production-style economic intelligence platform that automatically collects Brazilian macroeconomic data, transforms it into actionable insights, visualizes economic trends, and generates predictive forecasts.

The project should showcase the complete data lifecycle and serve as a portfolio piece relevant for:

* Junior Data Analyst
* Junior Data Scientist
* Junior Data Engineer
* Analytics Engineer
* Risk Analytics positions

This scope is intentionally modular, allowing each phase to be completed and published independently while still contributing to a cohesive end-to-end project.




