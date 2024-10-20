import os
import json
import asyncio

from hume import AsyncHumeClient
from hume.expression_measurement.batch import Face, Models
from hume.expression_measurement.batch.types import InferenceBaseRequest

async def main():
    # Initialize an authenticated client
    client = AsyncHumeClient(api_key="")

    # Define the filepath(s) of the file(s) you would like to analyze

    local_filepaths = [
        open(r"C:\Users\lucas\Downloads\WIN_20241019_13_16_41_Pro.mp4", mode="rb")
    ]

    # Create configurations for each model you would like to use (blank = default)
    face_config = Face()

    # Create a Models object
    models_chosen = Models(face=face_config)
    
    # Create a stringified object containing the configuration
    stringified_configs = InferenceBaseRequest(models=models_chosen)

    # Start an inference job and print the job_id
    job_id = await client.expression_measurement.batch.start_inference_job_from_local_file(
        json=stringified_configs, file=local_filepaths
    )
    print(job_id)   

    job_predictions = await client.expression_measurement.batch.get_job_predictions(
        id="faea500c-dbff-4059-87d3-25331b59f5ab"
    )

    print(job_predictions)

if __name__ == "__main__":
    asyncio.run(main())