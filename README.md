# midtermproject
Spotify Hit Predictor

This is a ML project done for the Midterm project for Datatalk MLZoomCamp.

The goal is to predict hits using song features only!
Dataset is from Kaggle.

The project is pretty simple:
1. ReadME
2. notebook.ipynb - A jupyter notebook consisting of EDA, Model Training, Parameter Tuning and Saving the Model
3. predict.py - A script containing a runnable version of the best model (no tuning, graphs or eda)
4. bentofile.yaml - I have chosen BentoML as the framework to containarize the project -
 all that you need to do to serve the model to a localhost is:
 4.1 -> pip install bentoml
 4.2 -> bentoml serve service.py:svc
 4.3 check your localhost port in your browser

 5. you can containerize and deploy the service using Docker:
 5.1 -> bentoml build
 5.2 -> you should get a message Successfully built Bento(tag="spotify_hit_classifier:kdelkqsqms4i2b6d")
 5.2 -> bentoml containerize tag (Use the tag from the previous message)
 5.3 -> docker run -it --rm -p 3000:3000 containerize spotify_hit_classifier:kdelkqsqms4i2b6d

 6. You can deploy this to AWS or other cloud providers:
 6.1 -> bentoml containerize model:tag --platform=linux/amd64
 6.2 Once the container is built, we need to setup ECR container repository where we can store the docker image:
    Create Identity and Access Management (IAM) user.
    Get the Security credentials (if don't have already):
    From top right drop-down menu > Security credentials > Access keys
    Install AWS CLI.
    Connect AWS with local machine by running aws configure command to provide credentials.
    Create Amazon Elastic Container Registry (ECR):
    Click Get Started > General settings > Create repository
    Authenticate and push docker image to ECR:
    Click on the repo name > View push commands > follow the instructions and tag the docker image built with bentoml (skip the step 2 because we have already built the docker image).
    Now we need to setup Amazon Elastic Container Service (ECS) to run our docker image:

    Search and click Elastic Container Service in the search bar.
    Create and Configure Cluster:
    Click Create Cluster > Networking only (CPU only) > follow the instructions.
    Create Task Definitions:
    Click Create new Task Definition > FARGRATE > Task memory (0.5GB), Task CPU (0.25 vCPU) > Add container (follow instructions and paste the image URI of ECR repo into the Image section, also increase the Soft limit to 256 and set Port mappings to 3000) > create task
    Run the Task:
    From ECS dashboard > Clusters > select the cluster we just created > Tasks > Run new Task > follow instructions (also select Launch type FARGATE, Operating system family Linux, Security groups set custom tcp to 3000) > create Task
    Once the Task is running we can click on it to see all of the information including the Public IP which we can entry in the browser to access the service.

    If we want to share the model or saving it to cloud, we can do so with bentoml export model:tag path_to_store/modelname.bento command and with this we can save the model in a local or push the model on save in the cloud (e.g., on Amazon S3 bucket). Beside the native .bento format, we can also save the model in ('tar'), tar.gz ('gz'), tar.xz ('xz'), tar.bz2 ('bz2'), and zip.

    In addition we can also import bentoml models from cloud or other sources using bentoml import path_to_access_/model_name.bento.
