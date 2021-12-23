# trino-exercise
Starburst Data Test


```
cd ~/trino-test/trino/core/docker
./build-remote.sh 365   # Have to comment out the docker build stmt for arm first
docker tag trino:365-amd64 us-central1-docker.pkg.dev/triino-test/quickstart-docker-repo/trino:365-amd64
docker push us-central1-docker.pkg.dev/triino-test/quickstart-docker-repo/trino:365-amd64
```

Required Services
- Artifact Repository
- Source Code Repositories
- GKE

Others?
```
gcloud services enable artifactregistry.googleapis.com
```
