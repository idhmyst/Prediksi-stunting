from flask import Flask, render_template, request
import joblib
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)

try:
    model = joblib.load("model_knn_stunting.pkl")
    scaler = joblib.load("scaler.pkl")
    print("Model dan Scaler berhasil dimuat")
except Exception as e:
    print(f"error saat memuat file: {e}")
    model = None
    scaler = None

LABEL_MAPPING = {
    0: "Normal",
    1: "Sangat Pendek",
    2: "Pendek",
    3: "Tinggi",
}

@app.route("/")
def home():
    return render_template(
        "index.html",
        umur="",
        jenis_kelamin="laki-laki",
        tinggi="",
        prediction_text="",
    )

@app.route("/predict", methods=["POST"])
def predict():
    umur = request.form.get("umur", "")
    jenis_kelamin = request.form.get("jenis_kelamin", "").lower()
    tinggi = request.form.get("tinggi", "")

    error_message = None
    prediction_text = ""

    try:
        umur_value = float(umur)
        tinggi_value = float(tinggi)
        if umur_value < 0:
            raise ValueError("Umur tidak boleh negatif.")
        if jenis_kelamin not in ["laki-laki", "perempuan"]:
            raise ValueError("Jenis kelamin tidak valid.")

        jk = 1 if jenis_kelamin == "laki-laki" else 0
        features = np.array([
            [umur_value, jk, tinggi_value]
        ], dtype=float)
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]
        prediction_text = f"Prediksi status gizi: {LABEL_MAPPING.get(prediction, prediction)}"
    except ValueError as exc:
        error_message = str(exc)
    except Exception as exc:
        error_message = "Terjadi kesalahan saat memproses data input."

    if error_message:
        prediction_text = f"Error: {error_message}"

    return render_template(
        "index.html",
        prediction_text=prediction_text,
        umur=umur,
        jenis_kelamin=jenis_kelamin,
        tinggi=tinggi,
    )

if __name__ == "__main__":
    app.run(debug=True)
