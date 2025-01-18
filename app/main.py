from fastapi import FastAPI
app = FastAPI(title="FastAPI MongoDB App")



@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI MongoDB API"} 