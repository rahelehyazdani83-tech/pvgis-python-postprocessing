# PVGIS Python Post-Processing

This repository contains the Python script developed for post-processing
monthly PVGIS SARAH3 outputs used in a Master's thesis on residential
rooftop photovoltaic systems in Germany.

## Purpose
The script parses PVGIS monthly CSV outputs, computes annual energy yield,
specific yield (kWh/kWp), and performance ratio (PR), performs validation
checks, and generates the tables and figures reported in Chapter 5 of the thesis.

## Execution environment
The script was executed in a Python 3.x environment with the pandas and
matplotlib libraries available. Execution was performed on a separate
system with a suitable Python environment.

## Repository contents
- `main.py`: Python script for data processing and validation
- `validation_table_5_1.csv`: Computed annual performance indicators
- `fig_monthly_energy_4cities.png`: Monthly PV energy output comparison
- `fig_monthly_PR_4cities.png`: Monthly performance ratio comparison

## Reproducibility
All inputs used by the script originate from publicly available PVGIS
SARAH3 datasets. The repository is provided to support transparency and
reproducibility of the computational workflow.
