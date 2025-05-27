# FastAPI and AWS lambda

 python -m venv myenv
 python3.11 -m venv myenv
 source myenv/bin/activate
 python --version
 pip install uvicorn mangum fastapi
 pip install --upgrade pip
 pip freeze > requirments.txt
 uvicorn main:app --reload

 docker run --rm \       
  --platform linux/amd64 \
  --entrypoint /bin/sh \
  -v "$PWD":/var/task \
  -w /var/task \
  public.ecr.aws/lambda/python:3.13 \
  -c "\
    pip install --upgrade pip && \
    pip install -r requirements.txt -t build/ \
  "


 \t\t\t\tcd dependencies
 dir
 ls -l
 zip aws_fastapi_lambda.zip -r .