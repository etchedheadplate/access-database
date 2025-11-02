```bash
python -m venv .venv
pip install -r requirements.txt
python -m scripts.create_db
python -m scripts.seed_data
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```
