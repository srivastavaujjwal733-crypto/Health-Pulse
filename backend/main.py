
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import os

from dotenv import load_dotenv
from google import genai

from backend.schemas import (
    HealthData,
    WHORiskData,
    ChatRequest,
    HealthReportRequest,
    HealthAgeRequest,
)
from backend.who_risk import calculate_who_risk

load_dotenv()

app = FastAPI(
    title="HealthPulse API",
    description="Smart Health Monitoring and Cardiovascular Prediction API",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained ML model
model = joblib.load("ml/healthpulse_model.pkl")


def get_gemini_client():
    """Create a Gemini client using the key stored in .env."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key .env file mein nahi mili."
        )

    return genai.Client(api_key=api_key)


@app.get("/")
def home():
    return {
        "message": "HealthPulse API is running successfully"
    }


# --------------------------------------------------
# 1. EXISTING ML PREDICTION
# --------------------------------------------------

@app.post("/predict")
def predict_health(data: HealthData):

    input_data = pd.DataFrame([{
        "age": data.age,
        "gender": data.gender,
        "height": data.height,
        "weight": data.weight,
        "ap_hi": data.ap_hi,
        "ap_lo": data.ap_lo,
        "cholesterol": data.cholesterol,
        "gluc": data.gluc,
        "smoke": data.smoke,
        "alco": data.alco,
        "active": data.active,
        "bmi": data.bmi
    }])

    prediction = model.predict(input_data)[0]

    if prediction == 1:
        result = "Cardiovascular Disease Predicted"
    else:
        result = "No Cardiovascular Disease Predicted"

    return {
        "prediction": int(prediction),
        "result": result,
        "message": (
            "This prediction is for educational purposes only "
            "and is not a medical diagnosis."
        )
    }


# --------------------------------------------------
# 2. EXISTING WHO RISK ASSESSMENT
# --------------------------------------------------

@app.post("/who-risk")
def who_risk(data: WHORiskData):

    try:
        result = calculate_who_risk(
            age=data.age,
            sex=data.sex,
            smoking=data.smoking,
            systolic_bp=data.systolic_bp,
            total_cholesterol=data.total_cholesterol,
            diabetes=data.diabetes
        )

        return {
            "success": True,
            "risk_percentage": result["risk_percentage"],
            "risk_category": result["risk_category"],
            "age_group": result["age_group"],
            "systolic_bp_group": result["systolic_bp_group"],
            "cholesterol_group": result["cholesterol_group"],
            "smoking_status": result["smoking_status"],
            "diabetes_status": result["diabetes_status"],
            "message": (
                "This assessment is for educational purposes only "
                "and is not a medical diagnosis."
            )
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# --------------------------------------------------
# 3. EXISTING GEMINI AI CHATBOT
# --------------------------------------------------

@app.post("/ai-chat")
def ai_chat(data: ChatRequest):

    try:
        client = get_gemini_client()

        prompt = f"""
        You are HealthPulse AI, a health education assistant.
        Answer in the same language as the user's question.
        Explain health topics in simple words.
        Do not diagnose diseases or prescribe medicines.
        Do not invent medical results or risk percentages.
        Explain that your response is not a medical diagnosis.
        For severe chest pain, serious breathing difficulty,
        or possible stroke symptoms, advise immediate emergency care.

        User question: {data.message}
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="Gemini ne empty response diya."
            )

        return {
            "success": True,
            "reply": response.text,
            "source": "Google Gemini"
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Gemini API error:", repr(e))
        raise HTTPException(
            status_code=502,
            detail="Gemini request failed. Check the VS Code terminal."
        )


# --------------------------------------------------
# 4. NEW AI HEALTH REPORT EXPLAINER
# --------------------------------------------------

@app.post("/ai-report-explainer")
def explain_health_report(data: HealthReportRequest):

    try:
        client = get_gemini_client()

        # Include only measurements the user actually supplied.
        report = data.model_dump(exclude_none=True)

        prompt = f"""
        You are the HealthPulse AI Health Report Explainer.

        Explain the following user-provided health information
        in simple, clear language. Use headings and short bullet points.

        User-provided information:
        {report}

        Important rules:
        1. Explain only the values actually provided.
        2. Never invent missing measurements or test results.
        3. Do not diagnose a disease or prescribe medicines.
        4. Do not invent disease probabilities or risk percentages.
        5. Explain that measurement interpretation depends on context.
        6. If a result may be concerning, recommend discussing it
           with a qualified healthcare professional.
        7. Blood glucose interpretation depends on whether the test
           was fasting, after a meal, or another type of test.
        8. State clearly that this is educational information,
           not a medical diagnosis.
        9. For severe chest pain, serious breathing difficulty,
           or possible stroke symptoms, advise immediate emergency care.
        10. Do not claim that you have reviewed any document or lab
            report beyond the values listed above.

        Default language: simple English.
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="AI report explainer returned an empty response."
            )

        return {
            "success": True,
            "report": report,
            "explanation": response.text,
            "disclaimer": (
                "Educational information only. This is not a medical "
                "diagnosis. Consult a qualified healthcare professional."
            )
        }

    except HTTPException:
        raise

    except Exception as e:
        print("AI report explainer error:", repr(e))
        raise HTTPException(
            status_code=502,
            detail="Could not explain the report. Check the backend terminal."
        )


# --------------------------------------------------
# 5. NEW HEALTH AGE CHECKER (DEMO INDICATOR ONLY)
# --------------------------------------------------

@app.post("/health-age")
def health_age_checker(data: HealthAgeRequest):

    score = 0
    factors = []

    # BMI indicator
    if data.bmi >= 30:
        score += 2
        factors.append("BMI is in a high range")
    elif data.bmi >= 25:
        score += 1
        factors.append("BMI is above the usual healthy adult range")

    # Systolic blood pressure indicator
    if data.systolic_bp is not None:
        if data.systolic_bp >= 140:
            score += 2
            factors.append("Systolic blood pressure is high")
        elif data.systolic_bp >= 130:
            score += 1
            factors.append("Systolic blood pressure is elevated")

    # Total cholesterol indicator
    if data.total_cholesterol is not None:
        if data.total_cholesterol >= 240:
            score += 2
            factors.append("Total cholesterol is high")
        elif data.total_cholesterol >= 200:
            score += 1
            factors.append("Total cholesterol is borderline high")

    # Glucose indicator: context and test type matter
    if data.blood_glucose is not None:
        if data.blood_glucose >= 126:
            score += 2
            factors.append(
                "Glucose value needs interpretation based on test type"
            )
        elif data.blood_glucose >= 100:
            score += 1
            factors.append(
                "Glucose value needs interpretation based on test type"
            )

    # Smoking indicator
    if data.smoking is True:
        score += 2
        factors.append("Smoking was reported")

    # Simple demonstration calculation, NOT a validated health-age model.
    demo_indicator_age = data.age + score

    if not factors:
        factors.append(
            "No additional indicators were flagged by this simple demo rule"
        )

    return {
        "success": True,
        "chronological_age": data.age,
        "demo_health_age_indicator": demo_indicator_age,
        "indicator_points": score,
        "factors": factors,
        "method": (
            "A simple demonstration rule that adds indicator points "
            "to chronological age. It is not scientifically validated."
        ),
        "disclaimer": (
            "This is not a biological-age estimate, medical assessment, "
            "or prediction of lifespan. Glucose interpretation depends "
            "on test type and clinical context. Consult a healthcare "
            "professional for individual interpretation."
        )
    }
