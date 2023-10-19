import boto3
from sagemaker import Session
from sagemaker.sklearn import SKLearn
from models.utils import affinity_endpoint_name, affinity_model_name, delete_existing_model, delete_existing_endpoint, delete_existing_endpoint_config
from dotenv import load_dotenv
import os

load_dotenv()
role = os.getenv("SAGEMAKER_ROLE")

boto_session = boto3.Session()
sagemaker_session = Session(boto_session)

def deploy_model(training_data_uri):
    delete_existing_model(affinity_model_name)
    delete_existing_endpoint(affinity_endpoint_name)
    delete_existing_endpoint_config(affinity_endpoint_name)
    
    sklearn_estimator = SKLearn(
        entry_point='train.py',
        role=role,
        source_dir='models/',
        instance_count=1,
        instance_type='ml.c5.xlarge',
        framework_version='1.2-1',
        name=affinity_model_name
    )
    sklearn_estimator.fit({'train': training_data_uri})

    # Deploy the model
    predictor = sklearn_estimator.deploy(instance_type="ml.c4.xlarge", initial_instance_count=1, endpoint_name=affinity_endpoint_name)

    print(f"Model deployed at endpoint: {predictor.endpoint_name}")    