# TOPSIS Assignment 

## PART-1

## Overview
This project implements the TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)
method in Python to rank alternatives based on multiple criteria.

---

## Methodology
1. Read input data from a CSV/Excel file.
2. Normalize the decision matrix.
3. Apply user-defined weights.
4. Determine ideal best and ideal worst based on impacts.
5. Compute Euclidean distances.
6. Calculate TOPSIS score and rank alternatives.

---

## Input Format
- First column: Alternative names
- Remaining columns: Numeric criteria
- Weights and impacts provided via command line

Example:
```bash
python topsis.py data.csv "1,1,1,1,1" "+,+,+,+,+" output.csv
```
---

## Output Format
![alt text](images/image.png)

