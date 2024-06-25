import uvicorn
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    uvicorn.run("server.main:app", host="0.0.0.0", port=3333, reload=True)
