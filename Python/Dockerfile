FROM python:alpine3.11

# gcc for multidict dependency (for PyGithub)
RUN apk add --no-cache gcc build-base 
# Install Python dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt ./repo/requirements.txt
RUN pip3 install --no-cache-dir -r ./repo/requirements.txt --no-binary :all:

# Run task
RUN python /repo/Python/main.py