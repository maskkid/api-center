"""Entrypoint that runs the FastAPI app with uvicorn.

Usage: `python main.py` or `uvicorn api_center:app --reload`
"""
import sys
import os
import uvicorn

# Add app directory to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from api_center.config import Config


def main():
    host = getattr(Config, 'HOST', '0.0.0.0')
    port = int(getattr(Config, 'PORT', 8000))
    debug = bool(getattr(Config, 'DEBUG', False))

    uvicorn.run("api_center:app", host=host, port=port, reload=debug, log_level="info")


if __name__ == '__main__':
    main()
