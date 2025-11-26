# API Center (FastAPI)

A complete FastAPI reimplementation of the previous Flask-based `0-saas-center` backend.

## Quick Start (using conda environment `open_manus`)

### 1. Activate environment

```bash
conda activate open_manus
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the FastAPI application

```bash
python main.py
```

The app will serve FastAPI routers mounted under `/api/v1` (e.g., `GET /api/v1/user/profile`, `POST /api/v1/qrcode/generate`).

### Development with uvicorn (hot reload)

```bash
uvicorn app.api_center:app --reload --host 0.0.0.0 --port 8000
```

### Run tests (uses FastAPI TestClient)

```bash
pytest tests/ -q
```

## Configuration

- Configuration values can be placed in `config.yml` at the project root to override defaults.
- Example configuration is provided in `config.yml`.

## Project Structure

```
api-center/
├── app/
│   └── api_center/
│       ├── __init__.py        # Main FastAPI app
│       ├── config.py          # Configuration
│       ├── routes/            # FastAPI routers
│       │   ├── user.py
│       │   ├── admin.py
│       │   ├── gateway.py
│       │   ├── qrcode.py
│       │   ├── chat.py
│       │   ├── genimg.py
│       │   ├── tts.py
│       │   ├── asr.py
│       │   └── ocr.py
│       ├── utils/             # Utilities
│       │   ├── response.py
│       │   └── decorators.py
│       └── vendors/           # Third-party integrations
│           └── ai_ocr/
├── main.py                    # Entrypoint for uvicorn
├── requirements.txt           # Python dependencies
├── config.yml                 # Configuration file
└── tests/                     # Test suite
```

## API Endpoints

All endpoints are under `/api/v1`:

- **User**: `/api/v1/user/register`, `/api/v1/user/login`, `/api/v1/user/profile`
- **Admin**: `/api/v1/admin/dashboard`
- **Gateway**: `/api/v1/gateway/config`
- **QR Code**: `/api/v1/qrcode/generate`
- **Chat**: `/api/v1/chat/send`
- **Image Generation**: `/api/v1/genimg/generate`
- **Text-to-Speech**: `/api/v1/tts/convert`
- **Speech-to-Text**: `/api/v1/asr/recognize`
- **OCR**: `/api/v1/ocr/recognize`, `/api/v1/ocr/wx/recognize`

## Notes

- The original `0-saas-center/` directory is preserved for reference.
- All routes have been converted from Flask-RestX to FastAPI with Pydantic models.
- Configuration is loaded from both environment variables and `config.yml`.
