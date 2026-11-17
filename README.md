# Personal PDF Chatbot – AI-Powered PDF Question Answering with AWS DevOps

An AI-powered PDF chatbot that allows users to upload PDF documents and ask questions about their content. Built with React, FastAPI, ChromaDB, Sentence Transformers and Google Gemini, and deployed on AWS using Docker, Amazon ECR and EC2.

The project also implements automated CI/CD using GitHub Actions, AWS OIDC and Systems Manager, with infrastructure and container monitoring using Prometheus and Grafana.

## Project Architecture

```text
                 Developer
                     |
                     v
               GitHub Repository
                     |
                     v
              GitHub Actions
                     |
              AWS OIDC Authentication
                     |
                     v
             Build Docker Images
                     |
                     v
                Amazon ECR
                     |
                     v
              AWS Systems Manager
                     |
                     v
                 Amazon EC2
                     |
                Docker Compose
                     |
          +----------+----------+
          |                     |
          v                     v
     React Frontend        FastAPI Backend
          |                     |
          |                ChromaDB
          |                     |
          |              Sentence Transformers
          |                     |
          |               Gemini API
          |                     |
          +----------+----------+
                     |
                  Users

              Monitoring Stack
                     |
          +----------+----------+
          |          |          |
          v          v          v
      Prometheus  Node       cAdvisor
                  Exporter      |
          |          |          |
          +----------+----------+
                     |
                     v
                   Grafana
```

## Technology Stack

| Category | Technologies |
|---|---|
| Frontend | React 19, Vite |
| Backend | Python, FastAPI, Uvicorn |
| AI | Google Gemini API |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| Web Server | Nginx |
| Containerization | Docker, Docker Compose |
| Cloud | AWS EC2, Amazon ECR |
| CI/CD | GitHub Actions |
| Authentication | AWS IAM, GitHub OIDC |
| Remote Deployment | AWS Systems Manager (SSM) |
| Monitoring | Prometheus, Grafana |
| Infrastructure Metrics | Node Exporter, cAdvisor |
| Operating System | Ubuntu Linux |

## Application Features

- Upload PDF documents through a React-based user interface.
- Extract and process PDF content.
- Generate document embeddings using Sentence Transformers.
- Store document vectors in ChromaDB.
- Retrieve relevant document chunks based on user questions.
- Generate AI-powered responses using Google Gemini.
- Persistent storage for uploaded PDFs and vector database data.
- Containerized frontend and backend services.

## AWS Deployment

The application is deployed on an Amazon EC2 Ubuntu instance.

### Amazon ECR

- Created separate ECR repositories for frontend and backend.
- Built Docker images for both application components.
- Tagged images using Git commit SHA values.
- Pushed images to Amazon ECR.
- Configured EC2 to pull images using its IAM instance role.

### Amazon EC2

- Hosted the application using Docker Compose.
- Deployed frontend and backend containers.
- Used Nginx to serve the React frontend and proxy API requests.
- Configured persistent Docker volumes for application data.

### IAM and Security

- Created an EC2 IAM role for AWS access.
- Configured ECR permissions for image pulling.
- Used GitHub OIDC to authenticate GitHub Actions with AWS.
- Avoided storing long-lived AWS access keys in GitHub.
- Used AWS Systems Manager for remote deployment.
- Kept application secrets in an environment file rather than source code.

## CI/CD Pipeline Using GitHub Actions

The project uses GitHub Actions to automate application deployment.

### Pipeline Workflow

1. Developer pushes changes to the `main` branch.
2. GitHub Actions workflow is triggered.
3. GitHub authenticates with AWS using OIDC.
4. Backend and frontend Docker images are built.
5. Docker images are pushed to Amazon ECR.
6. GitHub Actions sends deployment commands through AWS Systems Manager.
7. EC2 pulls the newly built images.
8. Docker Compose recreates the application containers.
9. The deployment workflow checks the command execution status.

### CI/CD Benefits

- Automated Docker image builds.
- Automated image publishing to ECR.
- Automated deployment to EC2.
- No static AWS access keys in GitHub.
- Consistent deployments using Git commit SHA tags.

## Monitoring and Observability

Prometheus and Grafana were integrated into the existing Docker Compose deployment.

### Monitoring Components

| Component | Purpose |
|---|---|
| Prometheus | Collects and stores metrics |
| Node Exporter | Collects EC2 system metrics |
| cAdvisor | Collects Docker container metrics |
| Grafana | Visualizes monitoring metrics |

### Configured Monitoring

- Prometheus scrape interval: 15 seconds.
- Prometheus data retention: 15 days.
- Node Exporter Full dashboard for EC2 infrastructure monitoring.
- cAdvisor metrics collection for Docker containers.
- Grafana connected to Prometheus as its data source.

### Infrastructure Metrics

- CPU utilization.
- Memory utilization.
- Disk usage.
- Network traffic.
- System load.
- Server uptime.

Grafana is bound to EC2 localhost on port 3000 and can be accessed securely through an SSH tunnel.

## Repository Structure

```text
personal-pdf-chatbot/
│
├── app/
│   ├── main.py
│   ├── vector_store.py
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── nginx.conf
│
├── monitoring/
│   └── prometheus/
│       └── prometheus.yml
│
├── data/
│   └── uploads/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── Dockerfile
├── docker-compose.yml
├── docker-compose.override.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

## Deployment Prerequisites

- AWS account.
- Ubuntu EC2 instance.
- Docker Engine.
- Docker Compose plugin.
- AWS CLI.
- Amazon ECR repositories.
- EC2 IAM instance role.
- GitHub repository with Actions enabled.
- Google Gemini API key.

## Environment Configuration

Create a `.env` file in the project root.

Example:

```env
GEMINI_API_KEY=your_gemini_api_key
GRAFANA_ADMIN_PASSWORD=your_secure_grafana_password
```

Keep `.env` private. Never commit API keys, passwords, AWS credentials or other secrets to GitHub.

## Running the Application

After configuring Docker, AWS access and the required environment variables:

```bash
docker compose config --quiet
```

Pull the application and monitoring images:

```bash
docker compose pull
```

Start the services:

```bash
docker compose up -d
```

Check running containers:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs --tail=50
```

## Accessing the Services

| Service | Access |
|---|---|
| React Application | `http://EC2_PUBLIC_IP` |
| FastAPI API Documentation | `http://EC2_PUBLIC_IP/docs` |
| Grafana | `http://localhost:3000` through SSH tunnel |
| Prometheus | Internal Docker network |

Grafana is intentionally not exposed directly to the public internet.

## Project Verification

The following functionality was tested during deployment:

- React frontend successfully loads.
- PDF upload works.
- Questions about uploaded PDFs receive answers.
- Backend and frontend Docker containers run successfully.
- Docker images are pushed to Amazon ECR.
- GitHub Actions CI/CD workflow completes successfully.
- GitHub OIDC authentication works.
- AWS Systems Manager deployment works.
- Prometheus successfully scrapes its own metrics, Node Exporter and cAdvisor.
- Grafana successfully connects to Prometheus.
- Node Exporter Full dashboard displays EC2 metrics.

## Future Improvements

- Add application-specific Prometheus metrics.
- Configure Grafana alerts for high CPU and memory usage.
- Improve Docker container monitoring dashboards.
- Add centralized application logging.
- Add automated security scanning using Trivy.
- Add Terraform for reproducible AWS infrastructure provisioning.
- Introduce HTTPS using a domain and TLS certificate.
- Implement backup and recovery for persistent application data.

## Learning Outcomes

Through this project, I gained hands-on experience with:

- Full-stack application containerization.
- AWS EC2 and ECR deployment.
- Docker and Docker Compose.
- GitHub Actions CI/CD automation.
- AWS IAM roles and OIDC authentication.
- AWS Systems Manager.
- Prometheus and Grafana monitoring.
- Linux server administration.
- Container and infrastructure troubleshooting.

---

**Author:** Navaneeth Krishna

**GitHub:** [Navaneethkrishna-coder](https://github.com/Navaneethkrishna-coder)

**Repository:** [Personal PDF Chatbot](https://github.com/Navaneethkrishna-coder/personal-pdf-chatbot)
