import bentoml
from bentoml.io import JSON


# Pull the model as model reference (it pulls all the associate metadata of the model)
model_ref = bentoml.xgboost.get('spotify_hit_model:latest')

# Create the model runner (it can also scale the model separately)
model_runner = model_ref.to_runner()

# Create the service 'spotify_hit_classifier' and pass the model
svc = bentoml.Service('spotify_hit_classifier', runners=[model_runner])


# Define an endpoint on the BentoML service
@svc.api(input=JSON(), output=JSON()) # decorate endpoint as in json format for input and output
def classify(app_data):

    # make predictions using 'runner.predict.run(input)' instead of 'model.predict'
    prediction = model_runner.predict.run(app_data)
    
    result = prediction[0] # extract prediction from 1D array
    print('Prediction:', result)

    if result > 0.7:
        return {'Status': 'HIT!'}
    elif result > 0.5:
        return {'Status': 'MAYBE'}
    else:
        return {'Status': 'NOT A HIT'}