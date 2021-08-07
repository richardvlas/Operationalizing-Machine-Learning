# Operationalizing-Machine-Learning

In this project we use Microsoft Azure Cloud Computing Services to configure a cloud-based machine learning production model, deploy it, and consume it. We will also create, publish, and consume a pipeline. 

The dataset used to train the ML model consists of Bank Marketing data and can be found [here](https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv).

## Architectural Diagram
The figure below shows steps that will be implemented in this project:

<img src="images/end-to-end-ml.png" width=75%>

## Key Steps

### 1. Authentication
In this step, we need to install the Azure Machine Learning Extension which allows us to interact with Azure Machine Learning Studio, part of the `az` command. After having the Azure machine Learning Extension, we create a Service Principal account and associate it with specific workspace. 

**Note**: I am using provided project lab with authentication done, so I skiped this step.

### 2. Automated ML Experiment
In this step, we create an experiment using Automated ML, configure a compute cluster, and use that cluster to run the experiment.
We need to upload the [dataset](https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv) to Azure Machine Learning Studio so that it can be used when training the model.

**Registered Datasets**
<img src="images/placeholder" width=75%>

**AutoML Experiment Completed**
<img src="images/placeholder" width=75%>

**Completed Experiment**
<img src="images/placeholder" width=75%>


### 3. Deploy the best model
After the experiment run completes, the Best Model is selected for deployment. Deploying the Best Model will allow to interact with the HTTP API service and interact with the model by sending data over POST requests.

The Best Model is shown in the Details tab and it will also come up in the Models tab at the top. 

**Deploying the Best Model**
<img src="images/placeholder" width=75%>

**Deployed Best Model**

The Best Model is deployed with Authentication enabled using Azure Container Instance (ACI) 
<img src="images/placeholder" width=75%>


**Endpoint**

After the model is deployed, Endpoint and Swagger URI were created. This can be seen in the Endpoint tab. We can notice that the Application Insights hasn't been created yet.
<img src="images/placeholder" width=75%>









### 4. Enable logging
### 5. Swagger Documentation
### 6. Consume model endpoints
### 7. Create and publish a pipeline
### 8. Documentation




