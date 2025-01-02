# **Project Setup and Deployment Guide**

This guide helps you set up and deploy services using Docker, Kubernetes, and Django.

## **1. Prerequisites**
- Ensure the required tools are installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [Kubectl](https://kubernetes.io/docs/tasks/tools/)
- Python (preferably with `virtualenv` for environment management)

---

## **2. Environment Setup**
1. Start Minikube:
   ```bash
   minikube start
   ```

2. Configure Docker to use Minikube's environment:
   ```bash
   eval $(minikube docker-env)
   ```

3. Create Kubernetes secrets from environment files:
   ```bash
   kubectl create secret generic redshift-migration-app-env --from-env-file=.env
   kubectl create secret generic appointment-app-env --from-env-file=.env
   kubectl create secret generic prescription-consumer-app-env --from-env-file=.env
   kubectl create secret generic patient-app-env --from-env-file=.env
   kubectl create secret generic lab-result-consumer-app-env --from-env-file=.env
   kubectl create secret generic patient-consumer-app-env --from-env-file=.env
   ```

---

## **3. Building Docker Images**
Build the Docker images for the services:
```bash
docker build -t consumer-service-app:latest .
docker build -t patient-service-app:latest .
docker build -t appointment-service-app:latest .
docker build -t redshift-migration-service-app:latest .
```

---

## **4. Django Application Setup**
1. Install dependencies:
   ```bash
   pip install django-filter
   ```

2. Prepare the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. (Optional) Reset a specific app's migrations:
   ```bash
   python manage.py migrate records zero
   ```

4. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

5. Start the Django consumer service:
   ```bash
   python manage.py start_consumer
   ```

---

## **5. Deploying Kubernetes Resources**
1. Apply Kubernetes deployment and service manifests:
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   kubectl apply -f consumer-deployment.yaml
   ```

2. Apply CronJob manifest:
   ```bash
   kubectl apply -f cronjob.yaml
   ```

---

## **6. Managing Kubernetes Resources**
1. Check active pods:
   ```bash
   kubectl get pods
   ```

2. Check deployments:
   ```bash
   kubectl get deployment
   ```

3. Check CronJobs:
   ```bash
   kubectl get cronjobs
   ```

4. View pod logs:
   ```bash
   kubectl logs consumer-service-6dd95ddd47-85jm5
   kubectl logs --tail=20
   ```

5. Port-forward services for local access:
   ```bash
   kubectl port-forward service/rabbitmq 15672:15672
   kubectl port-forward service/patient-service 8000:8000
   kubectl port-forward service/patient-service 8080:8080
   kubectl port-forward service/appointment-service 8090:8090
   ```

6. Inspect a secret:
   ```bash
   kubectl get secret redshift-migration-app-env -o yaml
   ```

---

## **7. Cleanup**
1. Delete a deployment:
   ```bash
   kubectl delete deployment patient-service
   ```

2. Delete a service:
   ```bash
   kubectl delete service patient-service
   ```

3. Delete a pod:
   ```bash
   kubectl delete pod consumer-service-769cf95f5c-v9ck2
   ```

4. Delete a secret:
   ```bash
   kubectl delete secret redshift-migration-app-env
   ```

5. Remove a Docker image:
   ```bash
   docker rmi consumer-service-app
   ```

---

## **8. Additional Resources**
For RabbitMQ setup, refer to [RabbitMQ Docker Setup Guide](https://www.svix.com/resources/guides/rabbitmq-docker-setup-guide/).
