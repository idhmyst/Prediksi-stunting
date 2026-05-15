from flask import Flask, render_template, request
import joblib
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)

# =========================
# Load Models
# =========================
try:
    # Stunting
    stunting_model = joblib.load("Stunting/model_knn_stunting.pkl")
    stunting_scaler = joblib.load("Stunting/scaler.pkl")

    # Eye health (mata minus)
    eye_model = joblib.load("mata minus/model_knn_eye_health.pkl")
    eye_scaler = joblib.load("mata minus/scaler_eye_health.pkl")
except Exception as e:
    print(f"error saat memuat file: {e}")
    stunting_model = None
    stunting_scaler = None
    eye_model = None
    eye_scaler = None

# =========================
# Mapping / Config
# =========================
LABEL_MAPPING_STUNTING = {
    0: "Normal",
    1: "Sangat Pendek",
    2: "Pendek",
    3: "Tinggi",
}

LABEL_MAPPING_EYE = {
    0: "Rendah",
    1: "Sedang",
    2: "Tinggi",
    3: "Sangat Tinggi",
}

EYE_FEATURES = [
    "exercise_hours",
    "mental_health_score",
    "screen_time_hours",
    "screen_brightness_avg",
    "age",
    "height_cm",
    "outdoor_light_exposure_hours",
    "night_mode_usage",
    "screen_distance_cm",
    "glasses_number",
]

# =========================
# Routes
# =========================
@app.route("/")
def home():
    return render_template(
        "index.html",
        # stunting
        umur="",
        jenis_kelamin="",
        tinggi="",
        # eye health
        exercise_hours="",
        mental_health_score="",
        screen_time_hours="",
        screen_brightness_avg="",
        age="",
        height_cm="",
        outdoor_light_exposure_hours="",
        night_mode_usage="",
        screen_distance_cm="",
        glasses_number="",
        # outputs
        prediction_text_stunting="",
        prediction_text_eye="",
    )

@app.route("/predict_stunting", methods=["POST"])
def predict_stunting():
    umur = request.form.get("umur", "")
    jenis_kelamin = request.form.get("jenis_kelamin", "").lower()
    tinggi = request.form.get("tinggi", "")

    error_message = None
    prediction_text_stunting = ""

    try:
        umur_value = float(umur)
        tinggi_value = float(tinggi)
        if umur_value < 0:
            raise ValueError("Umur tidak boleh negatif.")
        if jenis_kelamin not in ["laki-laki", "perempuan"]:
            raise ValueError("Jenis kelamin tidak valid.")
        if stunting_model is None or stunting_scaler is None:
            raise RuntimeError("Model stunting belum tersedia.")

        jk = 1 if jenis_kelamin == "laki-laki" else 0
        features = np.array([[umur_value, jk, tinggi_value]], dtype=float)
        features_scaled = stunting_scaler.transform(features)
        prediction = stunting_model.predict(features_scaled)[0]
        prediction_text_stunting = (
            f"Prediksi status gizi: {LABEL_MAPPING_STUNTING.get(prediction, prediction)}"
        )
    except ValueError as exc:
        error_message = str(exc)
    except Exception:
        error_message = "Terjadi kesalahan saat memproses data input stunting."

    if error_message:
        prediction_text_stunting = f"Error: {error_message}"

    # pass-through eye inputs (so the page doesn't reset them)
    def form_keep(key):
        return request.form.get(key, "")

    return render_template(
        "index.html",
        umur=umur,
        jenis_kelamin=jenis_kelamin,
        tinggi=tinggi,
        prediction_text_stunting=prediction_text_stunting,
        prediction_text_eye="",
        exercise_hours=form_keep("exercise_hours"),
        mental_health_score=form_keep("mental_health_score"),
        screen_time_hours=form_keep("screen_time_hours"),
        screen_brightness_avg=form_keep("screen_brightness_avg"),
        age=form_keep("age"),
        height_cm=form_keep("height_cm"),
        outdoor_light_exposure_hours=form_keep("outdoor_light_exposure_hours"),
        night_mode_usage=form_keep("night_mode_usage"),
        screen_distance_cm=form_keep("screen_distance_cm"),
        glasses_number=form_keep("glasses_number"),
    )

@app.route("/predict_eye", methods=["POST"])
def predict_eye():
    error_message = None
    prediction_text_eye = ""

    try:
        if eye_model is None or eye_scaler is None:
            raise RuntimeError("Model eye health belum tersedia.")

        values = []
        for f in EYE_FEATURES:
            raw = request.form.get(f, "")
            if raw is None or raw == "":
                raise ValueError(f"Input {f} wajib diisi.")
            values.append(float(raw))

        features = np.array([values], dtype=float)
        features_scaled = eye_scaler.transform(features)
        prediction = eye_model.predict(features_scaled)[0]
        # LABEL_MAPPING_EYE memakai kelas 0-3, sementara model eye berupa regression.
        # Pastikan yang tampil selalu teks/label, bukan float raw.
        mapped = LABEL_MAPPING_EYE.get(int(round(prediction)))
        if mapped is not None:
            prediction_text_eye = f"Prediksi skor kesehatan mata: {mapped}"
        else:
            prediction_text_eye = f"Prediksi skor kesehatan mata: {float(prediction):.2f}"
    except ValueError as exc:
        error_message = str(exc)
    except Exception:
        error_message = "Terjadi kesalahan saat memproses data input eye health."

    if error_message:
        prediction_text_eye = f"Error: {error_message}"

    # pass-through stunting inputs (so the page doesn't reset them)
    return render_template(
        "index.html",
        umur=request.form.get("umur", ""),
        jenis_kelamin=request.form.get("jenis_kelamin", ""),
        tinggi=request.form.get("tinggi", ""),
        prediction_text_stunting="",
        prediction_text_eye=prediction_text_eye,
        exercise_hours=request.form.get("exercise_hours", ""),
        mental_health_score=request.form.get("mental_health_score", ""),
        screen_time_hours=request.form.get("screen_time_hours", ""),
        screen_brightness_avg=request.form.get("screen_brightness_avg", ""),
        age=request.form.get("age", ""),
        height_cm=request.form.get("height_cm", ""),
        outdoor_light_exposure_hours=request.form.get("outdoor_light_exposure_hours", ""),
        night_mode_usage=request.form.get("night_mode_usage", ""),
        screen_distance_cm=request.form.get("screen_distance_cm", ""),
        glasses_number=request.form.get("glasses_number", ""),
    )


if __name__ == "__main__":
    app.run(debug=True)

