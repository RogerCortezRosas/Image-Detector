FROM python:3.10-bookworm

WORKDIR /dashboard

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .



CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0","--server.runOnSave=True"]