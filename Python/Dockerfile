FROM python:alpine3.11

# gcc for multidict dependency (for PyGithub)
RUN apk add --no-cache gcc build-base 
# Install Python dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt ./repo/requirements.txt
RUN pip3 install --no-cache-dir -r ./repo/requirements.txt --no-binary :all:

# Add entrypoint
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]