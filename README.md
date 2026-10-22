# HealthPulse AI

### Smart Health Monitoring and Prediction System Using Machine Learning and Artificial Intelligence

HealthPulse AI is a health-monitoring project designed to help users understand key health indicators and explore machine-learning-based health risk predictions through a web-based interface.

The project combines a web frontend, Python backend, machine learning, data processing, and planned AI-assisted interaction to demonstrate the potential of intelligent technologies in health awareness.

**Project Status:** Under Development

## Overview

HealthPulse AI aims to provide a centralized interface for basic health calculations, health indicator monitoring, and machine-learning-based prediction experiments.

The project follows a modular approach, separating frontend components, backend services, data processing, and machine-learning workflows.

## Key Features

- **Health Monitoring:** BMI calculation and basic health indicator inputs.
- **Machine Learning:** Dataset preparation, model training, and evaluation.
- **Backend API:** Python backend using FastAPI.
- **Data Management:** Pandas for data processing and SQLite with SQLAlchemy for database support.
- **AI Assistant:** Planned integration with Google's Gemini API.
- **Dashboard Prototype:** Streamlit-based interface for experimentation.

*Some features may require further integration and testing before they are fully operational.*

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas |
| Model Persistence | Joblib |
| Database | SQLite, SQLAlchemy |
| AI Integration | Google Gemini API |
| Prototype Dashboard | Streamlit |
| Version Control | Git, GitHub |

## Project Structure

```text
Health-Pulse/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── who_risk.py
├── data/
│   ├── cardio_cleaned.csv
│   ├── cardio_train.csv
│   └── who_south_asia_risk.csv
├── frontend/
│   ├── index.html
│   ├── chatbot.js
│   ├── chatbot.css
│   ├── css/
│   └── js/
├── ml/
│   ├── eda.py
│   ├── prepare_data.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   └── healthpulse_model.pkl
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

- Python compatible with the project dependencies
- Git
- A code editor such as Visual Studio Code

### 1. Clone the Repository

```bash
git clone https://github.com/srivastavaujjwal733-crypto/Health-Pulse.git
cd Health-Pulse
```

### 2. Create a Virtual Environment

On Windows:

```cmd
py -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```cmd
py -m pip install -r requirements.txt
```

## Running the Application

### Streamlit Prototype

```cmd
py -m streamlit run app.py
```

### FastAPI Backend

Open a separate terminal, activate the virtual environment, and run:

```cmd
py -m uvicorn backend.main:app --reload
```

When the backend starts successfully, its API documentation should be available at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

The available API endpoints depend on the implementation in `backend/main.py`.

## Machine Learning Workflow

The intended machine-learning workflow includes:

1. Data preparation and preprocessing.
2. Exploratory data analysis.
3. Model training.
4. Model evaluation using appropriate metrics.
5. Saving the trained model.
6. Integrating predictions with the backend.

Actual evaluation results should be added after running the model evaluation scripts.

## AI Integration

The project is designed to support Google's Gemini API for AI-assisted interaction.

If this integration is enabled, store the API key in a local `.env` file and access it through the backend.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit API keys or other secrets to the repository. Gemini integration must be tested before it is described as fully operational.

## Security and Privacy

- Keep API keys and credentials private.
- Do not expose secrets in frontend JavaScript.
- Validate user inputs before processing.
- Avoid collecting unnecessary personal health information.
- Clearly communicate the limitations of machine-learning predictions.

## Future Enhancements

- Complete frontend and backend integration.
- Interactive health data visualizations.
- Improved model evaluation and comparison.
- Expanded health monitoring capabilities.
- Enhanced AI chatbot functionality.
- Automated testing and online deployment.

## Author

**Ujjwal Srivastava**

GitHub: [srivastavaujjwal733-crypto](https://github.com/srivastavaujjwal733-crypto)

Project Repository: [HealthPulse AI](https://github.com/srivastavaujjwal733-crypto/Health-Pulse)

## Disclaimer

HealthPulse AI is an educational project and is not intended to provide medical diagnoses or replace professional healthcare advice. Model predictions and AI-generated responses may be inaccurate. Consult a qualified healthcare professional for medical concerns.
