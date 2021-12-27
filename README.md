# trino-exercise
This repo is my (Frank KUligowski) solution for the [Starburst Data Test](https://starburst.io) to create a Trio cloud deployment.  
This solution was built on the [Google Cloud Platform](https://cloud.google.com/). 
A GKE Cluster was created in the GCP Console using default cluster settings, and Trino was deployed to that cluster. See the Appendix for more details on the GKE cluster. 
Trino is deployed to the k8s cluster via a Helm chart.  A Python utility is used to query the Trino deployment for performance metrics, which are displayed to stdout. 
The Python utility, and all of the commands shown in this document were run from the GCP [Cloud Shell](https://cloud.google.com/shell/docs?hl=en).  

# Repo Files
- The [clients/metrics-handler](clients/metrics-handler) folder holds the Python client utility.  
- The [helm](helm) folder holds custom values settings that were supplied to the Helm chart for this solution.  

# Build and Deploy a Trino Docker Image  
To create the container image of the Trino application, I first created an [Artifact Registry](https://cloud.google.com/artifact-registry/docs) in GCP.  
```
gcloud artifacts repositories create trino-docker --repository-format=docker --location=us-central1 \
--description="Docker repository"
```

Next, I created a 'trino-test' directory to hold all my work and then downloaded the Trino Git repo. 
```
mkdir -p ~/trino-test; cd ~/trino-test
git clone https://github.com/trinodb/trino.git
```
The [core/docker](https://github.com/trinodb/trino/tree/master/core/docker) folder of that repo holds the commands for creating a new Trino container image. There is a shell script that will create it for you, but it has commands to create both an 'amd' and an 'arm' compatible executable, and the 'arm' command won't work in the GCP Cloud Shell (it uses an amd type processor), so I commented this line (31) out of the [core/docker/build-remote.sh](https://github.com/trinodb/trino/blob/master/core/docker/build-remote.sh) script.  
```
#docker build ${WORK_DIR} --pull --platform linux/arm64 -f arm64.dockerfile -t ${CONTAINER}-arm64 --build-arg "TRINO_VERSION=${TRINO_VERSION}"
```
With that, I could build the container image with the build-remote.sh script, tag the image with the GCP Artifact Registry path, and push the container image to that 'trino-docker' Artifact Repo. Version '365' was chosen because it seem to be a recent and stable build.  
```
cd ~/trino-test/trino/core/docker
./build-remote.sh 365   # Have to comment out the docker build stmt for arm first
docker tag trino:365-amd64 us-central1-docker.pkg.dev/$DEVSHELL_PROJECT_ID/trino-docker/trino:365-amd64
docker push us-central1-docker.pkg.dev/$DEVSHELL_PROJECT_ID/trino-docker/trino:365-amd64
```

# Run the Container Image  
To deploy Trino, I found a [nice Helm chart](https://github.com/trinodb/charts) to do the work, so I cloned its repo.  
```
git clone https://github.com/trinodb/charts.git
```
Then I created my own copy of the [values.yaml](helm/values.yaml) file, and made these changes.  
- Set image.repository and image.tag to point to the container image I created above.  
- Set server.workers to 1 (instead of 2).  
- Added settings for the jmx connector under the additionalCatalogs setting, to meet the Trino JMX requirement of the test.  
- Changed service.type from ClusterIP to LoadBalancer, so that Trino would be exposed to the internet, per the test requirement.  
```
cd ~/trino-test
cp charts/charts/trino/values.yaml trino-exercise/helm/values.yaml
vi trino-exercise/helm/values.yaml  # Use your favorite editor.
```
With that (and a connection to the GKE cluster), I could run the command to deploy the Trino application.  
```
helm install trino charts/charts/trino --namespace trino --create-namespace -f trino-exercise/helm/values.yaml
```
After a few moments, the Load Balancer will come up and we can get its address with this command.  
```
kubectl get svc -n trino
```
And Trino can be reached at that address on port 8080 (i.e. http://34.72.58.19:8080).  

# Metrics Handler Client
As a client process to query the JMX metrics from the Trino install, I used a Python library to query the endpoint and parse the results. The [trino-python-client](https://github.com/trinodb/trino-python-client) provides an easy to use library to query Trino with SQL.  
The [clients/metrics-handler](clients/metrics-handler) folder houses the resulting Python solution. The command sequence below will run the utility.  
```
cd ~/trino-test/trino-exercise/clients
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
export PYTHONPATH=$(pwd)
python -m metrics-handler -u trino -a 1.2.3.4
```
Where "1.2.3.4" is the external IP address of the Trino deployment.  
This utility will print out the requested metrics to stdout, similar to below.  
```
ActiveNodes=1
HeapSize=232635616
HeapSize=314759472
RunningQueries=1
```
See the [main_process.py](clients/metrics-handler/main_process.py) script file for the actual queries that are used.  
Here is the usage information for the metrics-handler utility.  
```
Metrics Handler for Trino - part of the test for Starburst Data

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  User Id to connect to the XCDE API (default: None)
  -a API_HOST, --api_host API_HOST
                        Trino API Hostname (default: localhost)
  -p PORT, --port PORT  Trino API Port (default: 8080)

Logging Verbosity:
  -v                    Set verbosity level (default: 0)
  ```

# External Resources  
These document sites were particularly helpful in building this solution.  
- [Trino Architecture](https://www.oreilly.com/library/view/trino-the-definitive/9781098107703/ch04.html)
- [Trino documentation](https://trino.io/docs/current/overview/concepts.html)
- [JMX Connector](https://trino.io/docs/current/connector/jmx.html#configuration)
- [Trino Docker Image](https://github.com/trinodb/trino/tree/master/core/docker)
- [Trino Helm Chart](https://github.com/trinodb/charts)
- [Trino Python Client](https://github.com/trinodb/trino-python-client)

# Services and Tools  
These GCP resources were used by this solution.
- [Google Cloud Platform](https://cloud.google.com/)
- [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/docs)
- GCP [Artifact Registry](https://cloud.google.com/artifact-registry/docs)
- GCP [Cloud Shell](https://cloud.google.com/shell/docs?hl=en)

# Time Log  
Here is an estimate of the time spent on this solution, broken down by major task.  
- Review documentation: 1 hour
- Build container image: 1 hour
- Find and use Helm chart: 1 hour
- Setup GCP and GKE cluster: 1 hour
- Learn JMX and create client: 2 hours
- Finalize and Document: 2 hour

# If There Was More Time  
If we wanted to expand the usability of this solution, here are some candidates for improvement.  
- Figure out how to setup Trino for HTTPS and deploy.  
- Configure Trino for User Authentication.  
- Build the Python client as its own image.  

# Appendix  
## GKE Cluster  
Here is the equivalent command line to create the k8s cluster used in this exercise (falls within GCP free limits).  
```
gcloud beta container --project "trino-336014" clusters create "trino-cluster" --zone "us-central1-c" \
--no-enable-basic-auth --cluster-version "1.21.5-gke.1302" --release-channel "regular" --machine-type "e2-medium" \
--image-type "COS_CONTAINERD" --disk-type "pd-standard" --disk-size "100" --metadata disable-legacy-endpoints=true \
--scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write",\
"https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol",\
"https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" \
--max-pods-per-node "110" --num-nodes "3" --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias \
--network "projects/trino-336014/global/networks/default" --subnetwork "projects/trino-336014/regions/us-central1/subnetworks/default" \
--no-enable-intra-node-visibility --default-max-pods-per-node "110" --no-enable-master-authorized-networks \
--addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver \
--enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 \
--enable-shielded-nodes --node-locations "us-central1-c"
```
This command will get the login credentials for that cluster, and allow the kubectl command to be used on the cluster.  
```
gcloud container clusters get-credentials trino-cluster --zone us-central1-c --project trino-336014
```
