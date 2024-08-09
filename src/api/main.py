from fastapi import FastAPI
from models.location_models import Base
from connection import engine
from routes.location_routes import router as location_router
from routes.forecast_routes import router as forecast_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(location_router)
app.include_router(forecast_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)