import sys
import os
import uvicorn


# Ensure the project root directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

# Run the application
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
