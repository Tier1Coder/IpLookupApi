# REST API for IP Tagging Service

This repository contains the implementation of a REST API for managing and querying IP-based tags.

## Table of Contents

1. [Project Description](#project-description)
2. [Getting Started](#getting-started)
3. [Testing](#testing)

---

## Project Description

The service is implemented in Python 3.13 using the `Django` framework. 
It provides two main endpoints for fetching tags associated with IPv4 addresses based on a knowledge base.

### Example Usage  
Below is an example request and response for fetching IP tags using this API.  

Request:
```bash
curl -X GET http://localhost:8080/ip-tags/192.168.1.1
```
Response
```JSON
{
  "ip": "192.168.1.1",
  "tags": ["corporate", "vpn", "trusted"]
}
```

---

### Key Features

- **Supports two endpoints:**
  - `GET /ip-tags/{ip}`: Returns a JSON list of tags for the given IPv4 address.
  - `GET /ip-tags-report/{ip}`: Returns an HTML table with tags for the given IPv4 address.
- **Tags are stored in a Patricia Trie** using [Pytricia](https://github.com/jsommers/pytricia) library for efficient querying.
- **The knowledge base is read from a JSON file** during service initialization.
- **Database** is not needed.

---

## Getting Started

### Prerequisites

- Docker
- Python v3.13
- .env file in IpLookupApi directory, with these variables:
  - `SECRET_KEY` - long random string used for security-related operations (Django),
  - `KNOWLEDGE_BASE_PATH` - path to the JSON file containing the specific data to read, e.g. 
  `/IpLookupApi/data.json` (remember about proper localization if used with Docker).

### Running

1. Navigate to the `IpLookupApi` directory.
2. Execute the script: `docker-compose up --build` or `python manage.py runserver {PORT}`.
3. Service will be ready on: `localhost:8080` address.


---

## Testing

Tests can be run using `pytest` command.
Some of the tests require having running service. 

In order to check crucial logs:
1. In e.g. Terminal, execute: `docker ps`.
2. Find your container and execute: `docker exec -it {container_ID} /bin/bash`.
3. Now you can use `cat errors.log` which will show you possible errors.
