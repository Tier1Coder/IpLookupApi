# Build
FROM python:3.13

# Install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy source code of the project
COPY . /IpLookupApi

# Set working directory
WORKDIR /IpLookupApi

# Entrypoint shell scripts to be executed
COPY ./entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["sh", "/entrypoint.sh"]
