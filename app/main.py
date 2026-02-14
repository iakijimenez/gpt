from __future__ import annotations

from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="CasaGen AI API",
    description="MVP para generar imágenes/planos/video de una casa a partir de texto.",
    version="0.1.0",
)


class HouseRequest(BaseModel):
    prompt: str = Field(..., min_length=20, description="Descripción de la casa deseada")


class GeneratedImage(BaseModel):
    title: str
    prompt: str


class RoomPlan(BaseModel):
    name: str
    approx_area_m2: float


class GeneratedPlan(BaseModel):
    style: str
    total_area_m2: float
    rooms: List[RoomPlan]
    notes: str


class GeneratedVideo(BaseModel):
    storyboard: List[str]
    prompt: str


class HouseGenerationResponse(BaseModel):
    summary: str
    images: List[GeneratedImage]
    plan: GeneratedPlan
    video: GeneratedVideo


class HouseDesignService:
    """Servicio mock para MVP.

    En producción este servicio debe orquestar:
    - parsing del brief con un LLM
    - generación de imágenes
    - generación de plano estructurado
    - generación de storyboard/video
    """

    def generate(self, request: HouseRequest) -> HouseGenerationResponse:
        base = request.prompt.strip()

        images = [
            GeneratedImage(
                title="Fachada principal",
                prompt=f"Render arquitectónico realista, {base}, vista frontal, golden hour",
            ),
            GeneratedImage(
                title="Sala y comedor",
                prompt=f"Interiorismo realista, {base}, sala-comedor integrados, iluminación natural",
            ),
        ]

        plan = GeneratedPlan(
            style="Moderno contemporáneo",
            total_area_m2=145.0,
            rooms=[
                RoomPlan(name="Sala-comedor", approx_area_m2=34.0),
                RoomPlan(name="Cocina", approx_area_m2=16.0),
                RoomPlan(name="Dormitorio principal", approx_area_m2=22.0),
                RoomPlan(name="Dormitorio secundario", approx_area_m2=14.0),
                RoomPlan(name="Baño", approx_area_m2=8.0),
            ],
            notes=(
                "Distribución preliminar para validación conceptual. "
                "Requiere revisión técnica por arquitecto/ingeniero antes de construir."
            ),
        )

        video = GeneratedVideo(
            storyboard=[
                "Toma aérea del lote y fachada.",
                "Recorrido de ingreso a sala-comedor.",
                "Transición a cocina y patio.",
                "Cierre con vista nocturna de fachada iluminada.",
            ],
            prompt=(
                "Video arquitectónico tipo walkthrough, 30 segundos, movimientos suaves de cámara, "
                f"estilo cinematográfico, basado en: {base}"
            ),
        )

        return HouseGenerationResponse(
            summary="Propuesta conceptual generada desde tu descripción.",
            images=images,
            plan=plan,
            video=video,
        )


service = HouseDesignService()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate", response_model=HouseGenerationResponse)
def generate_house_assets(request: HouseRequest) -> HouseGenerationResponse:
    return service.generate(request)
