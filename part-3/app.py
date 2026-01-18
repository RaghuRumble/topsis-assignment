from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os
import re
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    file = request.files["file"]
    weights_input = request.form["weights"]
    impacts_input = request.form["impacts"]
    email = request.form["email"]

    # Validate email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format"

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    # Read input file
    df = pd.read_csv(input_path)
    data = df.iloc[:, 1:]

    # Parse weights and impacts
    weights = list(map(float, weights_input.split(",")))
    impacts = impacts_input.split(",")

    if len(weights) != len(impacts) or len(weights) != data.shape[1]:
        return "Number of weights, impacts and columns must be equal"

    for i in impacts:
        if i not in ["+", "-"]:
            return "Impacts must be either + or -"

    # TOPSIS calculation
    norm_data = data / np.sqrt((data ** 2).sum())
    weighted_data = norm_data * weights

    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == "+":
            ideal_best.append(weighted_data.iloc[:, i].max())
            ideal_worst.append(weighted_data.iloc[:, i].min())
        else:
            ideal_best.append(weighted_data.iloc[:, i].min())
            ideal_worst.append(weighted_data.iloc[:, i].max())

    dist_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    df["Topsis Score"] = dist_worst / (dist_best + dist_worst)
    df["Rank"] = df["Topsis Score"].rank(ascending=False).astype(int)

    output_path = os.path.join(OUTPUT_FOLDER, "result.csv")
    df.to_csv(output_path, index=False)

    # Send email (USE APP PASSWORD)
    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result"
    msg["From"] = "yourgmail@gmail.com"
    msg["To"] = email
    msg.set_content("Please find the TOPSIS result attached.")

    with open(output_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="octet-stream",
            filename="result.csv"
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("yash.19.r04@gmail.com", "rydlioauwrsnoezu")
        smtp.send_message(msg)

    return "Result sent successfully to email"

if __name__ == "__main__":
    app.run(debug=True)
