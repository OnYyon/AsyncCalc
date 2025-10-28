import fastapi # type: ignore
import uvicorn # type: ignore

from src.manager import Manager

mgr = Manager()
app = fastapi.FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
