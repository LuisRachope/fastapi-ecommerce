"""
Router V1 da API
Agrupa todos os routers da versão 1 da API
"""
from fastapi import APIRouter
from app.presentation.api.v1.endpoints.product_controller import router as product_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(product_router)
