
from pydantic import BaseModel, Field
from typing import Optional


class HealthData(BaseModel):
    age: float
    gender: int
    height: float
    weight: float
    ap_hi: float
    ap_lo: float
    cholesterol: int
    gluc: int
    smoke: int
    alco: int
    active: int
    bmi: float


class WHORiskData(BaseModel):
    age: int
    sex: str
    smoking: bool
    systolic_bp: float
    total_cholesterol: float
    diabetes: bool


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)


# AI Health Report Explainer
class HealthReportRequest(BaseModel):
    age: int = Field(ge=18, le=120)
    sex: str = Field(min_length=1, max_length=30)

    systolic_bp: Optional[float] = Field(
        default=None, ge=50, le=300
    )
    diastolic_bp: Optional[float] = Field(
        default=None, ge=30, le=200
    )
    total_cholesterol: Optional[float] = Field(
        default=None, ge=50, le=600
    )
    blood_glucose: Optional[float] = Field(
        default=None, ge=20, le=800
    )
    bmi: Optional[float] = Field(
        default=None, ge=10, le=80
    )
    smoking: Optional[bool] = None
    diabetes: Optional[bool] = None


# Health Age Checker
class HealthAgeRequest(BaseModel):
    age: int = Field(ge=18, le=100)
    bmi: float = Field(ge=10, le=80)

    systolic_bp: Optional[float] = Field(
        default=None, ge=50, le=300
    )
    total_cholesterol: Optional[float] = Field(
        default=None, ge=50, le=600
    )
    blood_glucose: Optional[float] = Field(
        default=None, ge=20, le=800
    )
    smoking: Optional[bool] = None
