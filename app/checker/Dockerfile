# stage 1: install python dependencies in an isolated folder
FROM public.ecr.aws/lambda/python:3.12 AS deps
# copy requirements first so docker caches the pip install layer when only code changes
COPY app/checker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target /install

# stage 2: build the clean runtime image
FROM public.ecr.aws/lambda/python:3.12
# copy installed packages from stage 1 into lambda's working directory (/var/task)
COPY --from=deps /install ${LAMBDA_TASK_ROOT}
# copy application source files and yaml config
COPY app/checker/*.py ${LAMBDA_TASK_ROOT}/app/checker/
COPY app/config/ ${LAMBDA_TASK_ROOT}/app/config/
# tell aws lambda which module and function to invoke
CMD ["app.checker.handler.lambda_handler"]