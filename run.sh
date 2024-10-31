streamlit run app.py

uvicorn main:app --host 0.0.0.0 --port 7000
docker build -f Dockerfile -t loup21991/bloggen .
docker push loup21991/bloggen:latest
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml logs -f