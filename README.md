# ideal-spoon


# rabbitmq configs

https://www.svix.com/resources/guides/rabbitmq-docker-setup-guide/

python manage.py migrate records zero

python manage.py makemigrations
python manage.py migrate

python manage.py runserver


pip install django-filter

/Users/kaushikshamantha/Documents/MSc/Cloud computing/CW/ideal-spoon/appointment_service
python manage.py start_consumer



minikube start

docker build -t consumer-service-app:latest .

docker build -t patient-consumer-service:latest .

kubectl create secret generic redshift-migration-app-env --from-env-file=.env

kubectl apply -f consumer-deployment.yaml

kubectl get deployment
kubectl delete deployment patient-service

kubectl delete service patient-service

kubectl delete secret redshift-migration-app-env

kubectl delete pod consumer-service-769cf95f5c-v9ck2

docker rmi consumer-service-app

kubectl apply -f deployment.yaml

kubectl apply -f service.yaml

kubectl get pods

kubectl logs consumer-service-6dd95ddd47-85jm5

docker build -t patient-service-app:latest .

kubectl port-forward service/rabbitmq 15672:15672


kubectl port-forward service/patient-service 8000:8000

kubectl get secret redshift-migration-app-env -o yaml

eval $(minikube docker-env)

kubectl logs --tail=20


kubectl port-forward service/patient-service 8080:8080

kubectl port-forward service/appointment-service 8090:8090


kubectl apply -f cronjob.yaml


docker build -t redshift-migration-service-app:latest .


docker build -t patient-service-app:latest .