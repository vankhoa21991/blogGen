

# FastAPI & Streamlit Blogging Application with Google OAuth
This repository hosts a SaaS application built with FastAPI and Streamlit, providing a blogging platform where users can log in or sign up using their Google accounts, create and manage blog posts, and access personal dashboards. This project is structured to be deployed on Google Cloud Platform (GCP) with Kubernetes and PostgreSQL.

## Project Overview
- Part 1: Google OAuth Login and Signup with FastAPI and Streamlit.
- Part 2: PostgreSQL Database Integration and CRUD Operations for User Posts.
- Part 3: Deployment of the Backend on Kubernetes.
- Part 4: Deployment of the Frontend on Cloud Run.

## Features
- OAuth Authentication: Secure login and signup using Google OAuth.
- Personal Dashboard: Each user can access their dashboard to add, view, and manage blog posts.
- Post Management: CRUD functionality for blog posts stored in PostgreSQL.
- Scalable Deployment: Backend on Kubernetes and frontend on Cloud Run for scalable cloud hosting.

## Getting Started
### Prerequisites
- Python 3.9+
- Docker
- Google Cloud SDK (for deployment)
- GCP Project with billing enabled
- OAuth 2.0 Credentials for Google API

### Local Setup
Clone the Repository:
```
git clone https://github.com/yourusername/fastapi-streamlit-blog.git
cd fastapi-streamlit-blog
```

Environment Variables: Create a .env file in the root directory with the following:

```
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
SECRET_KEY=your_session_secret_key
SQLALCHEMY_DATABASE_URL=your_database_url
FRONTEND_URL=http://localhost:8501
BACKEND_URL=http://localhost:7000
```

```bash
docker-compose up -d --build --force-recreate
```

### Project Structure
- backend: Contains FastAPI backend with authentication (auth) and API endpoints (api).
    - apps: Contains FastAPI backend with authentication (auth) and API endpoints (api).
    - database: Models, schemas, and CRUD operations for PostgreSQL integration.
- frontend: Streamlit code for the user interface.

## Deployment
1. Google Kubernetes Engine (GKE)
Create a GKE cluster:

bash
Copy code
gcloud container clusters create my-cluster --num-nodes=3
Deploy the backend using Kubernetes configurations in k8s/backend-deployment.yaml.

2. Cloud SQL (PostgreSQL)
Create a PostgreSQL instance on Cloud SQL.
Configure SQLALCHEMY_DATABASE_URL in .env with the Cloud SQL connection string.

3. Cloud Run
Deploy the Streamlit frontend with gcloud:
bash
Copy code
gcloud run deploy streamlit-frontend --source ./frontend --platform managed
Usage
After deploying, users can access the application via the frontend URL. They’ll be able to log in with Google, create posts, and view posts on their dashboard.

Contributing
Fork this repository.
Create a feature branch.
Commit your changes and open a pull request.
License
This project is licensed under the MIT License.

Feel free to reach out with questions or feedback. Enjoy building and scaling your blogging application on GCP!


# Backlog
- [ ] Make a front page
- [ ] Make a database of user account
- [ ] Make a database of blog post
- [ ] Make an admin page to manage blog post and user account

