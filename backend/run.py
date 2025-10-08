"""Application runner script"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

if __name__ == "__main__":
    import uvicorn

    from src.main import app

    uvicorn.run(app, host="0.0.0.0", port=8000)