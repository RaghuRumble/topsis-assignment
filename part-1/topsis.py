import sys
import pandas as pd
import numpy as np

if len(sys.argv) != 5:
    print("Usage: python topsis.py <InputFile> <Weights> <Impacts> <OutputFile>")
    sys.exit(1)

input_file = sys.argv[1]
weights_input = sys.argv[2]
impacts_input = sys.argv[3]
output_file = sys.argv[4]

try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print("Error: Input file not found")
    sys.exit(1)

if df.shape[1] < 3:
    print("Error: Input file must contain at least 3 columns")
    sys.exit(1)

data = df.iloc[:, 1:]

if not np.all(data.applymap(lambda x: isinstance(x, (int, float)))):
    print("Error: Columns from 2nd to last must be numeric")
    sys.exit(1)

try:
    weights = list(map(float, weights_input.split(',')))
    impacts = impacts_input.split(',')
except:
    print("Error: Weights and impacts must be comma separated")
    sys.exit(1)

if len(weights) != data.shape[1] or len(impacts) != data.shape[1]:
    print("Error: Number of weights, impacts and columns must be same")
    sys.exit(1)

for impact in impacts:
    if impact not in ['+', '-']:
        print("Error: Impacts must be either + or -")
        sys.exit(1)

# Step 1: Normalize the decision matrix
norm_data = data / np.sqrt((data ** 2).sum())

# Step 2: Apply weights
weighted_data = norm_data * weights

# Step 3: Determine ideal best and ideal worst
ideal_best = []
ideal_worst = []

for i in range(len(impacts)):
    if impacts[i] == '+':
        ideal_best.append(weighted_data.iloc[:, i].max())
        ideal_worst.append(weighted_data.iloc[:, i].min())
    else:
        ideal_best.append(weighted_data.iloc[:, i].min())
        ideal_worst.append(weighted_data.iloc[:, i].max())

# Step 4: Calculate distances from ideal best and worst
distance_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
distance_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

# Step 5: Calculate TOPSIS score
topsis_score = distance_worst / (distance_best + distance_worst)
df['Topsis Score'] = topsis_score
df['Rank'] = df['Topsis Score'].rank(ascending=False).astype(int)

# Step 6: Save output file
df.to_csv(output_file, index=False)
print("TOPSIS analysis completed successfully")

