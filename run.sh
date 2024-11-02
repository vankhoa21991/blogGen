streamlit run app.py

uvicorn main:app --host 0.0.0.0 --port 7000
docker build -f Dockerfile -t loup21991/bloggen .
docker push loup21991/bloggen:latest
docker compose -f docker-compose.yml up -d
docker compose -f docker-compose.yml logs -f


kubectl get svc -n nginx-ingress
kubectl get pods
kubectl describe pod bloggen-748f9df6cf-dzjcp
kubectl logs bloggen-77987bf7cc-cc5jv
kubectl get svc -n nginx-ingress
http://34.91.188.26.nip.io/docs#/

kubens model-serving
helm upgrade --install bloggen . --force

kubectl scale deployment bloggen --replicas=0
kubectl scale deployment bloggen --replicas=1
