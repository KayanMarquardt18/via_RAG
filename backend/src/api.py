from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from src.ml_predict import load_model, prepare_input, predict
from src.rag_engine import get_rag_explanation, ask_knowledge

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model("models/galaxy_model.pkl")


class PredictRequest(BaseModel):
    u: float
    g: float
    r: float
    i: float
    z: float
    redshift: float


class Mensagem(BaseModel):
    autor: str
    texto: str


class AskRequest(BaseModel):
    pergunta: str
    historico: Optional[List[Mensagem]] = []


@app.post("/predict")
def predict_endpoint(req: PredictRequest):
    features = [req.u, req.g, req.r, req.i, req.z, req.redshift]
    input_df = prepare_input(features)
    prediction, probabilities = predict(model, input_df)
    explanation = get_rag_explanation(prediction)
    return {
        "prediction": prediction,
        "probabilities": {
            cls: float(prob) for cls, prob in zip(model.classes_, probabilities)
        },
        "explanation": explanation
    }


@app.post("/ask")
def ask_endpoint(req: AskRequest):
    historico = [{"autor": m.autor, "texto": m.texto} for m in req.historico]
    resposta = ask_knowledge(req.pergunta, historico=historico)
    return {"resposta": resposta}