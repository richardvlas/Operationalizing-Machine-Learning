from azureml.core import workspace
from azureml.core.webservice import Webservice

# Requires the config to be downloaded first to the current working directory
ws = workspace.from_config()

# Set with the deployment name
name = "automl-votingensemble"

# load existing web service
service = Webservice(name=name, workspace=ws)

service.update(enable_app_insights=True)

log = service.get_logs()

for line in logs.split('\n'):
    print(line)
