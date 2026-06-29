import os
from flask import Flask, request, jsonify
import numpy as np
import tensorflow as tf
from flask_cors import CORS

# ============================
# Flask Setup
# ============================

app = Flask(__name__)
CORS(app)  # Required for React frontend

# ============================
# Load ANN Model
# ============================

print("Loading ANN model...")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "ann_model.h5")
model = tf.keras.models.load_model(MODEL_PATH)

print("ANN Model Loaded Successfully")

# ============================
# Prediction Route
# ============================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.json

        print("Incoming Data:", data)

        # ============================
        # Categorical Mapping
        # ============================

        cp_map = {
            "Typical Angina": 0,
            "Atypical Angina": 1,
            "Non-anginal Pain": 2,
            "Asymptomatic": 3
        }

        thal_map = {
            "Normal": 1,
            "Fixed Defect": 2,
            "Reversible Defect": 3
        }

        slope_map = {
            "Upsloping": 0,
            "Flat": 1,
            "Downsloping": 2
        }

        # ============================
        # Prepare Features
        # ============================

        raw_values = {
            "age": float(data["age"]),
            "sex": int(data["sex"]),
            "cp": cp_map[data["cp"]],
            "trestbps": float(data["trestbps"]),
            "chol": float(data["chol"]),
            "fbs": int(data["fbs"]),
            "restecg": int(data["restecg"]),
            "thalach": float(data["thalach"]),
            "exang": int(data["exang"]),
            "oldpeak": float(data["oldpeak"]),
            "slope": slope_map[data["slope"]],
            "ca": float(data["ca"]),
            "thal": thal_map[data["thal"]]
        }

        training_ranges = {
            "age": (29, 77),
            "sex": (0, 1),
            "cp": (0, 3),
            "trestbps": (94, 200),
            "chol": (126, 564),
            "fbs": (0, 1),
            "restecg": (0, 2),
            "thalach": (71, 202),
            "exang": (0, 1),
            "oldpeak": (0.0, 6.2),
            "slope": (0, 2),
            "ca": (0, 3),
            "thal": (1, 3)
        }

        invalid_fields = [
            field for field, value in raw_values.items()
            if not (training_ranges[field][0] <= value <= training_ranges[field][1])
        ]

        if invalid_fields:
            print("Invalid input fields:", invalid_fields)
            return jsonify({
                "result": "Invalid input values",
                "probability": 0,
                "message": "Please enter values within the model's trained range."
            })

        features = np.array([[
            raw_values["age"],
            raw_values["sex"],
            raw_values["cp"],
            raw_values["trestbps"],
            raw_values["chol"],
            raw_values["fbs"],
            raw_values["restecg"],
            raw_values["thalach"],
            raw_values["exang"],
            raw_values["oldpeak"],
            raw_values["slope"],
            raw_values["ca"],
            raw_values["thal"]
        ]])

        print("Processed Features:", features)

        # ============================
        # Feature Scaling
        # ============================

        feature_min = np.array([29, 0, 0, 94, 126, 0, 0, 71, 0, 0.0, 0, 0, 1], dtype=float)
        feature_max = np.array([77, 1, 3, 200, 564, 1, 2, 202, 1, 6.2, 2, 3, 3], dtype=float)

        scaled_features = (features - feature_min) / (feature_max - feature_min)
        scaled_features = np.clip(scaled_features, 0, 1)

        print("Scaled Features:", scaled_features)

        # ============================
        # Model Prediction
        # ============================

        model_output = model.predict(scaled_features)[0][0]
        risk_probability = float(np.clip(1.0 - model_output, 0.0, 1.0))

        print("Model output (healthy probability):", model_output)
        print("Disease risk probability:", risk_probability)

        # ============================
        # Result Message
        # ============================

        if risk_probability > 0.7:
            result = "High Risk of Heart Disease"
        elif risk_probability > 0.4:
            result = "Moderate Risk"
        else:
            result = "Low Risk"

        return jsonify({
            "result": result,
            "probability": risk_probability
        })

    except Exception as e:

        print("❌ Prediction Error:", e)

        return jsonify({

            "result": "Prediction Error",
            "probability": 0

        })


# ============================
# Intelligent Chatbot with NLP
# ============================

from difflib import SequenceMatcher

def get_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Comprehensive knowledge base
knowledge_base = {
    "symptoms": {
        "keywords": ["symptom", "sign", "feel", "pain", "chest", "shortness", "breath", "fatigue", "dizz", "irregular", "palpitation"],
        "response": "Common heart disease symptoms include:\n• Chest pain or discomfort (angina)\n• Shortness of breath\n• Fatigue and weakness\n• Dizziness or lightheadedness\n• Irregular heartbeat (palpitations)\n• Nausea or cold sweats\n\n⚠️ If you experience severe chest pain or difficulty breathing, seek emergency medical care immediately!"
    },
    "prevention": {
        "keywords": ["prevent", "avoid", "reduce risk", "stay healthy", "how to", "protect"],
        "response": "Key heart disease prevention strategies:\n✓ Regular Exercise: 150 min/week of moderate activity\n✓ Healthy Diet: Low in salt, saturated fats, and sugar\n✓ Quit Smoking: Major risk reduction\n✓ Manage Stress: Practice meditation or yoga\n✓ Healthy Weight: Maintain BMI 18.5-24.9\n✓ Regular Checkups: Monitor BP and cholesterol\n✓ Limit Alcohol: Moderate consumption only"
    },
    "diet": {
        "keywords": ["diet", "food", "eat", "nutrition", "meal", "what should", "what to eat"],
        "response": "Heart-healthy diet guidelines:\n🥗 Include: Vegetables, fruits, whole grains, lean fish, nuts, olive oil\n❌ Limit: Processed foods, salt, sugar, saturated fats, red meat\n\nRecommended foods:\n• Fatty fish (salmon, mackerel) - omega-3 fatty acids\n• Berries - antioxidants\n• Leafy greens - minerals and vitamins\n• Nuts and seeds - healthy fats\n• Whole grains - fiber"
    },
    "exercise": {
        "keywords": ["exercise", "workout", "activity", "physical", "move", "sport", "fitness"],
        "response": "Exercise recommendations for heart health:\n⏱️ Duration: At least 150 minutes per week of moderate intensity\n💪 Types of exercise:\n• Walking, jogging, cycling (cardio)\n• Swimming (low-impact)\n• Dancing\n• Strength training 2x/week\n\n⚠️ Consult your doctor before starting a new exercise program!"
    },
    "risk factors": {
        "keywords": ["risk", "factor", "cause", "why heart disease", "vulnerable"],
        "response": "Major heart disease risk factors:\n🔴 Non-modifiable: Age, family history, gender\n🟡 Modifiable: High blood pressure, high cholesterol, smoking, diabetes, obesity, sedentary lifestyle, stress, poor diet\n\nThe more risk factors you have, the higher your risk. Regular monitoring and healthy lifestyle changes can significantly reduce your risk!"
    },
    "cholesterol": {
        "keywords": ["cholesterol", "ldl", "hdl", "triglyceride"],
        "response": "Cholesterol management:\n📊 Healthy levels:\n• LDL (bad) < 100 mg/dL\n• HDL (good) > 40 mg/dL (men), > 50 mg/dL (women)\n• Total cholesterol < 200 mg/dL\n\n✅ How to lower cholesterol:\n• Exercise regularly\n• Eat healthy diet (reduce saturated fats)\n• Maintain healthy weight\n• Don't smoke\n• Limit alcohol\n\nConsult your doctor for blood tests and personalized advice."
    },
    "blood pressure": {
        "keywords": ["blood pressure", "hypertension", "systolic", "diastolic", "bp"],
        "response": "Blood pressure categories:\n✅ Normal: <120/80 mmHg\n⚠️ Elevated: 120-129/<80\n🟡 Stage 1 Hypertension: 130-139/80-89\n🔴 Stage 2 Hypertension: ≥140/90\n\nManagement tips:\n• Regular monitoring\n• Reduce sodium intake\n• Exercise daily\n• Manage stress\n• Maintain healthy weight\n• Limit alcohol\n\nHigh blood pressure often has no symptoms - get checked regularly!"
    },
    "stress": {
        "keywords": ["stress", "anxiety", "mental", "relax", "meditation", "calm"],
        "response": "Stress and heart health:\nChronic stress increases heart disease risk by:\n• Raising blood pressure\n• Increasing heart rate\n• Promoting inflammation\n\n🧘 Stress management techniques:\n• Meditation and mindfulness\n• Deep breathing exercises\n• Yoga\n• Regular exercise\n• Adequate sleep (7-9 hours)\n• Social connections\n• Hobbies and relaxation\n\nTake mental health seriously for better heart health!"
    },
    "emergency": {
        "keywords": ["emergency", "urgent", "danger", "attack", "severe", "call", "911", "ambulance"],
        "response": "🚨 HEART ATTACK SYMPTOMS - SEEK EMERGENCY HELP:\n❌ Severe chest pain or pressure\n❌ Difficulty breathing\n❌ Pain radiating to arm, shoulder, or jaw\n❌ Sudden dizziness or fainting\n❌ Nausea with chest discomfort\n\n📞 Call emergency services (911) immediately!\n\nTime is critical - don't delay or drive yourself. Call an ambulance for proper care."
    }
}

def get_best_response(user_message):
    """Intelligent response matching based on message content"""
    user_message_lower = user_message.lower()
    best_category = None
    highest_score = 0
    
    # Check keywords in knowledge base
    for category, data in knowledge_base.items():
        for keyword in data["keywords"]:
            if keyword in user_message_lower:
                score = get_similarity(user_message_lower, keyword)
                if score > highest_score:
                    highest_score = score
                    best_category = category
    
    if best_category and highest_score > 0.2:
        return knowledge_base[best_category]["response"]
    
    # Greeting responses
    if any(greeting in user_message_lower for greeting in ["hello", "hi", "hey", "greet", "help"]):
        return "👋 Hello! I'm your AI Heart Health Assistant. I can help you with information about:\n• Heart disease symptoms\n• Prevention strategies\n• Diet and nutrition\n• Exercise guidelines\n• Risk factors\n• Cholesterol and blood pressure\n• Stress management\n\nWhat would you like to know?"
    
    # General fallback with suggestions
    return "I'm your AI Heart Health Assistant! 🏥\n\nI can answer questions about:\n✓ Symptoms of heart disease\n✓ Prevention and lifestyle changes\n✓ Heart-healthy diet\n✓ Exercise recommendations\n✓ Risk factors and monitoring\n✓ Cholesterol and blood pressure\n✓ Stress management\n\nFeel free to ask any of these topics, or be more specific about what concerns you!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data["message"].strip()
        
        print(f"User Message: {user_message}")
        
        reply_text = get_best_response(user_message)
        
        return jsonify({"reply": reply_text})
    
    except Exception as e:
        print("❌ Chat Error:", e)
        return jsonify({"reply": "⚠️ I encountered an error processing your message. Please try again!"})


# ============================
# Health Check Route
# ============================

@app.route("/")
def home():

    return jsonify({

        "message": "Heart Disease API Running"

    })


# ============================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )