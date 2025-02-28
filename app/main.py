import utils.transport
import utils.session
from fastapi import FastAPI
from app.controllers import user_controller
from app.config.database import Base, engine

app = FastAPI()

# Include routers
app.include_router(user_controller.router)

# Create database tables
Base.metadata.create_all(bind=engine)
