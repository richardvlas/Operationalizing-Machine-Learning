# Operationalizing-Machine-Learning

In this project we make a use of Microsoft Azure Cloud to configure a cloud-based machine learning production model, deploy it, and consume it. We first train a set of machine learning models leveraging AutoML to automaticaly train and tune a model using given target metric. The dataset used to train the ML model consists of Bank Marketing data and can be found [here](https://automlsamplenotebookdata.blob.core.windows.net/automl-sample-notebook-data/bankmarketing_train.csv).

Once the AutoML experiment is completed, we then select the best model in terms of accuracy out of all models trained and deploy it using `Azure Container Instance` (ACI). The model can now be consumed via a REST API and authentication key generated. 

To automate this process as much as possible, we leverage the use of Python SDK to create, publish, and consume a pipeline that will orchestrate all steps such as allocation of compute resources, creating an experiment in an workspace, loading data in a `TabularDataset`, setting up or calling existing ML model generated via AutoML that can be configured via `AutoMLConfig` and last but not least validation and testing. 

Once the pipeline is published, a REST endpoint enables to call and rerun the pipeline from any HTTP library on any platform.

Having a pipeline in place is an important step towards CI/CD automation. 

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

We need to upload the `bankmarketing_train.csv` dataset into Azure ML Studio before we can use AutoML to train different ML models.  

<img src="images/01_bank_marketing_dataset.PNG" width=100%>

Next we create a new Automated ML experiment, name it `automl-experiment-bank-marketing`, specify `y` as the target column from the dataset. We also need to create new compute cluster, for example using virtual machine `Standard_DS12_v2` and select minimum number of nodes to `1`.

<img src="images/02_create_automl_experiment.PNG" width=100%>

In `Configure run` section we select task type to `Classification` and check the `Explain best model` option. On `Exit criterion`, set `Training job time` to `1` hour and on `Concurency` set `Max. concurent iterations` to `5`.

<img src="images/03_automl_select_task.PNG" width=100%>

**AutoML Experiment Running**

The AutoML is running and training of multiple classication models is in progress.

<img src="images/04_automl_running.PNG" width=100%>

**AutoML Experiment Completed**

The experiment is completed and the Best Model Summary shows best performing model in terms of accuracy.

<img src="images/05_automl_completed.PNG" width=100%>

**Best Model**

The above figure showed Best Model Summary and the figure below shows some of the metrics of the best model from AutoML.

<img src="images/06_best_model.PNG" width=100%>


### 3. Deploy the best model
After the experiment run completes, the Best Model will be selected for deployment. Deploying the Best Model will allow to interact with it through the HTTP API service by sending data over POST requests.

The Best Model is shown in the Details tab and it will also come up in the Models tab at the top. 

**Deploying the Best Model**

After the AutoMl run is completed, select `Deploy` to deploy the best model, choose `Name`, select `Azure Container Instance` (ACI) as `Compute type` and check `Enable authentication`:

<img src="images/best_model_deploying.PNG" width=100%>

**Deployed Best Model**

The model summary is showing the Best Model deployed with Authentication enabled using Azure Container Instance (ACI) 

<img src="images/best_model_deployed.PNG" width=100%>


**Endpoint**

After the model is deployed, Endpoint and Swagger URI were created. This can be seen in the Endpoint tab. We can notice that the Application Insights hasn't been created yet and this is what we will do next.

<img src="images/best_model_deployed_endpoint.PNG" width=100%>


### 4. Enable logging
Now that the Best Model is deployed, enable Application Insights and retrieve logs. Although this is configurable at deploy time with a check-box, it is useful to be able to run code that will enable it for us. Here is a snippet of the code:

```python
from azureml.core import Workspace
from azureml.core.webservice import Webservice

# Requires the config to be downloaded first to the current working directory
ws = Workspace.from_config()

# Set with the deployment name
name = "automl-votingensemble"

# load existing web service
service = Webservice(name=name, workspace=ws)

service.update(enable_app_insights=True)

logs = service.get_logs()

for line in logs.split('\n'):
    print(line)
```

Prior to running the `logs.py` script, make sure to download and store the `config.json` file in the same folder.

**Application Insights Enabled**

The figure below shows that Application Insights is enabled in the Detail tab of the endpoint with url provided:

<img src="images/application_insights_enabled.PNG" width=100%>


**Logs from logs.py script**

The next figure shows the output from the logs.py script that enables the Application Insights among other logs information:

<img src="images/logs.PNG" width=100%>


### 5. Swagger Documentation

Swagger is an Interface Description Language for describing RESTful APIs expressed using JSON. Swagger is used together with a set of open-source software tools to design, build, document, and use RESTful web services.

In order to cosume the deployed model using Swagger, Azure provides a Swagger JSON file for deployed models. We can find and download it from the Endpoints section under the deployed model.

**Default Swagger page**

Below we can see default Swagger documentation before running the `serve.py` script.

<img src="images/swagger_default_page.PNG" width=100%>

**Swagger Model Documentation**

Once the script is run, we can see the documentation of our model, as shown below.

<img src="images/swagger_model_page.PNG" width=100%>

**API Methods of the Model**

The API methods is a crutial part of the documentation, as it allows us to check the structure of json file we can send to the model via POST request.

<img src="images/swagger_api_get.PNG" width=100%>

The figure below shows HTTP POST request parameters that specify the structure of the input message to be sent via the POST request:

<img src="images/swagger_api_methods.PNG" width=100%>

The next figure ilustrates the structure of successful response from POST request: 

<img src="images/swagger_api_responses.PNG" width=100%>


### 6. Consume model endpoints
Now it's time to interact with the deployed model and to test it, we use the `endpoint.py` script to call the trained model and feeding it with some test data. Before we run the script, we need to modify both the `scoring_uri` and the `key` to match the key for our service and the URI that was generated after deployment. This URI can be found in the Details tab, above the Swagger URI.

**Consuming Model Endpoints**

This shows that the `endpoint.py` script runs against the API producing JSON output from the model:

<img src="images/endpoint_script_output.PNG" width=100%>


### 7. Create and publish a pipeline
For this part of the project, we use a Jupyter Notebook to create and publish a pipeline. This notebook demonstrates the use of AutoMLStep in Azure Machine Learning Pipeline.
The notebook uses Python SDK to do the following:

- Create an Experiment in an existing Workspace.
- Create or Attach existing AmlCompute to a workspace.
- Define data loading in a TabularDataset.
- Configure AutoML using AutoMLConfig.
- Use AutoMLStep
- Train the model using AmlCompute
- Explore the results.
- Test the best fitted model.

In order to use the notebook we must make sure to have the same keys, URI, dataset, cluster, and model names already created

**Created Pipeline**

Pipeline is created and running as the Status in Aml indicates.

<img src="images/pipeline_in_azure.PNG" width=100%>

**Pipeline Overview**

Graphical represenation toghether with Pipeline run overview details is shown below:

<img src="images/pipeline_in_azure_2.PNG" width=100%>

**Pipeline Endpoint**

Python SDK is used to publish the pipeline and provides us with a REST endpoint to interact with it.

<img src="images/publish_endpoint.PNG" width=100%>

**Published Pipeline Endpoint**

Once the pipeline is published, we can view the REST endpoint in Azure ML Studio under the Pipeline tab:

<img src="images/published_pipeline_endpoint.PNG" width=100%>

**RunDetails Widget**

The RunDetails Widget retrieves information and monitors the pipeline run.

<img src="images/pipeline_run.PNG" width=100%>

RunDetails Widget showing graphical representation of our pipeline. Link to Azure ML Studio is also provides below to get more details through the Azure GUI.

<img src="images/pipeline_run_2.PNG" width=100%>


## Screen Recording
This [screencast](https://youtu.be/I2HV_blwz2Y) shows the entire process of the working ML application.

## Future Improvements
The project could be improved on by the following:

- Model accuracy could be potential increased by collecting more data, while making sure all classes are represented equaly.
- Try using Deep learning as a technique to achieve higher accuracy.
- Create a simple web app to interact with the deployed ML model. This would nicely demonstrate the whole end-to-end process from development until user interaction.





