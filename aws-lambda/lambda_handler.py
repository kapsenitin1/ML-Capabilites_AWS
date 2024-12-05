import json
import boto3

def lambda_handler(event, context):
    """
    Lambda function to invoke SageMaker endpoint for diabetes prediction.
    """
    try:
        # Check if the input is passed in the 'body' key (API Gateway)
        if 'body' in event:
            # Parse the body as JSON
            input_data = json.loads(event['body'])
        else:
            # If no 'body', assume the input is directly in the event
            input_data = event

        # Positive:
        # {"x1":1, "x2":0, "x3":5.7, "x4":0, "x5":110, "x6":80, "x7":32, "x8":15.0, "x9":28.0, "x10":0.6, "x11":45, "x12":1,"x13":0, "x14":0}

        # Negative:
        # {"x1":0, "x2":1, "x3":5.6, "x4":4, "x5":135, "x6":78, "x7":23, "x8":16.7, "x9":28.6, "x10":0.6, "x11":37, "x12":0,"x13":1, "x14":0}

        # Extract the value of x1
        x1 = input_data.get('x1', None)
        x2 = input_data.get('x2', None)
        x3 = input_data.get('x3', None)
        x4 = input_data.get('x4', None)
        x5 = input_data.get('x5', None)
        x6 = input_data.get('x6', None)
        x7 = input_data.get('x7', None)
        x8 = input_data.get('x8', None)
        x9 = input_data.get('x9', None)
        x10 = input_data.get('x10', None)
        x11 = input_data.get('x11', None)
        x12 = input_data.get('x12', None)
        x13 = input_data.get('x13', None)
        x14 = input_data.get('x14', None)

        predition_data = '{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14)

        # SageMaker runtime client
        sagemaker_runtime = boto3.client('sagemaker-runtime', region_name='us-east-2')
    
        # Old End Point: sagemaker-xgboost-2024-12-04-10-52-55-225
        endpoint_name = "sagemaker-xgboost-2024-12-04-13-23-58-809"

         # Invoke the SageMaker endpoint
        response = sagemaker_runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType="text/csv",  # Specify the format of your input
            #Body=json.dumps(input_data)      # Convert the input to JSON string
            Body=predition_data
        )

        # Decode the response
        prediction = response['Body'].read().decode('utf-8')
        print(prediction)

        return {
            "statusCode": 200,
            "body": json.loads(prediction) 
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
