from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.secrets import SecretManager
from app.srv.api.controller import router

app = FastAPI(
    title="Hotel Reservation ML Service",
    description="A simple microservice to guardrail against hotel reservation abuse",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Krib"}


app.include_router(router)



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=SecretManager.ENV.is_local)
