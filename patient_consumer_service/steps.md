minikube start

docker build -t consumer-service-app:latest .

kubectl create secret generic patient-app-env --from-env-file=.env

kubectl apply -f consumer-deployment.yaml

kubectl get deployment
kubectl delete deployment patient-service

kubectl delete service patient-service


kubectl delete pod consumer-service-769cf95f5c-v9ck2

docker rmi consumer-service-app

kubectl apply -f deployment.yaml

kubectl apply -f service.yaml

kubectl logs consumer-service-6dd95ddd47-85jm5

docker build -t consumer-service-app:latest .

kubectl port-forward service/rabbitmq 15672:15672


kubectl port-forward service/patient-service 8000:8000