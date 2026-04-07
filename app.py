from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load model
model = pickle.load(open("rent_model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict_page")
def predict_page():
    return render_template("form.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form values
        bhk = int(request.form["BHK"])
        size = int(request.form["Size"])
        bathroom = int(request.form["Bathroom"])

        city = request.form["City"]
        area_type = request.form["Area Type"]
        furnishing = request.form["Furnishing Status"]
        tenant = request.form["Tenant Preferred"]
        contact = request.form["Point of Contact"]

        if not (1 <= bhk <= 6 and 100 <= size <= 5000 and 1 <= bathroom <= 5):
            return render_template("form.html", prediction_text="Invalid input values!")

        # Manual encoding (IMPORTANT — must match training columns)
        features = [
            bhk, size, bathroom,
            
            # Area Type
            1 if area_type == "Carpet Area" else 0,
            1 if area_type == "Super Area" else 0,

            # City
            1 if city == "Chennai" else 0,
            1 if city == "Delhi" else 0,
            1 if city == "Hyderabad" else 0,
            1 if city == "Kolkata" else 0,
            1 if city == "Mumbai" else 0,

            # Furnishing
            1 if furnishing == "Semi-Furnished" else 0,
            1 if furnishing == "Unfurnished" else 0,

            # Tenant
            1 if tenant == "Bachelors/Family" else 0,
            1 if tenant == "Bachelors" else 0,

            # Contact
            1 if contact == "Contact Builder" else 0,
            1 if contact == "Contact Owner" else 0
        ]

        prediction = model.predict([features])[0]

        return render_template("form.html", prediction_text=f"Estimated Rent: ₹ {int(prediction)}")

    except:
        return render_template("form.html", prediction_text="Error in input!")

if __name__ == "__main__":
    app.run(debug=True)
