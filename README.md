# trino-exercise
Starburst Data Test


```
gcloud artifacts repositories create trino-docker --repository-format=docker --location=us-central1 --description="Docker repository"
cd ~/trino-test/trino/core/docker
./build-remote.sh 365   # Have to comment out the docker build stmt for arm first
docker tag trino:365-amd64 us-central1-docker.pkg.dev/$DEVSHELL_PROJECT_ID/trino-docker/trino:365-amd64
docker push us-central1-docker.pkg.dev/$DEVSHELL_PROJECT_ID/trino-docker/trino:365-amd64
```

Required Services
- Artifact Repository
- Source Code Repositories
- GKE

Downloaded Helm Charts from here - https://github.com/trinodb/charts
```
 helm install trino charts/charts/trino --namespace trino --create-namespace
```

Setup for the Client
```
cd ~/trino-test/trino-exercise/clients
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
export PYTHONPATH=$(pwd)
python -m metrics-handler -u frank -a myurl:8080
```


Others?
```
gcloud services enable artifactregistry.googleapis.com
```
