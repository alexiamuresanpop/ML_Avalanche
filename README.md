# Avalanche Danger Classification Using Machine Learning

## Overview

This project explores the use of classical machine learning algorithms to classify avalanche danger levels in Norway using meteorological, geographical, and temporal data from the [NVE Avalanche Forecast API](https://api01.nve.no/hydrology/forecast/avalanche/v6.3.2/swagger/ui/index).

The target variable is the avalanche danger level, grouped into three classes: **Low, Medium, and High**.

## Methodology

The project follows these main steps:

1. **Data collection and preprocessing:** Extracting forecast data from the NVE API and preparing the dataset.
2. **Feature selection:** Comparing different approaches to identify relevant predictors.
3. **Model training:** Evaluating classification algorithms with different feature selection subsets using WEKA and Python.
4. **Evaluation:** Comparing model performance using classification metrics.

## Repository Structure

| Folder | Description |
|---|---|
| `[trying_out]` | Initial files for testing the API functioning |
| `[dataset_creation]` | Data extraction from the NVE API and dataset creation |
| `[exploratory_analysis]` | IInitial exploratory analysis of the dataset |
| `[feature_selection_results]` | Features selected for the different methods |
| `[avalanche_dataset]` | Final datasets used for the models (_DIST for k-NN and Logistic Regression) |
| `[model_results]` | Model evaluation and performance metrics from WEKA (and Python for k-NN) |

## Results

The experiments compare different classifiers and feature selection strategies to assess their impact on classification performance.

See report for the model comparison and final conclusions.

## Tools

- Python
- WEKA
- NVE Avalanche Forecast API

## References

- [NVE Avalanche Forecast API](https://api01.nve.no/hydrology/forecast/avalanche/v6.3.2/swagger/ui/index)
- [Norwegian Avalanche Warning Website](https://www.varsom.no/en/avalanches/avalanche-warnings/)
