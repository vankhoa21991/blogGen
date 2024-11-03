

docker build -f Dockerfile -t loup21991/bloggen-front .
docker build -t eu.gcr.io/moodmap-440120/bloggen-front:latest .
docker run -p 7000:7000 loup21991/bloggen
docker run -p 8501:8501 loup21991/bloggen-front

docker push loup21991/bloggen-front:latest
docker push eu.gcr.io/moodmap-440120/bloggen-front:latest


# Tutorial

1. build app in local, use docker-compose to run the app, DB in local

sudo docker compose down
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml logs -f
sudo docker compose logs -f backend

2. create DB in GCP, download credentials, use backend in local, DB in GCP



streamlit run app.py
uvicorn main:app --host 0.0.0.0 --port 7000

3. create GCP project, create GKE cluster, deploy backend in GKE, DB in GCP

docker build -f Dockerfile -t loup21991/bloggen .
docker push loup21991/bloggen:latest

kubectl get svc -n nginx-ingress
kubectl get pods
kubectl describe pod bloggen-748f9df6cf-dzjcp
kubectl logs bloggen-77987bf7cc-b279x
kubectl get svc -n nginx-ingress
http://34.91.188.26.nip.io/docs#/

kubens model-serving
helm upgrade --install bloggen . --force

kubectl scale deployment bloggen --replicas=0
kubectl scale deployment bloggen --replicas=1



4. deploy frontend in GCP, add domain name

gcloud builds submit --tag gcr.io/moodmap-440120/bloggen-front
gcloud run deploy bloggen-front --image gcr.io/moodmap-440120/bloggen-front 
https://medium.com/@faizififita1/how-to-deploy-your-streamlit-web-app-to-google-cloud-run-ba776487c5fe