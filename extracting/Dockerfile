FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY extract_data.py .
COPY parse_data_cloud.py .
COPY load_data.py .
COPY pipeline.py .

CMD [ "pipeline.lambda_handler" ]