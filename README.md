# URL Shortener Take-Home Project
Welcome to the Pocket Worlds URL Shortener Take-Home Project! In this repository, we'd like you to demonstrate your
engineering skills by creating a small Python project that implements a URL Shortener web service.

This project will serve as the primary jumping off point for our technical interviews. We expect you to spend a 
couple of hours building an MVP that meets the requirements in the Product Description. You are free to implement 
your solution and modify the provided template in the way that makes the most sense to you, but make sure to 
update the README accordingly so that it's clear how to run and test your project. During the interviews, you will 
be asked to demo your solution and discuss the reasoning behind your implementation decisions and their trade-offs. 
Be prepared to share your screen for live coding and problem solving with your interviewers based on this discussion.

## Project Description
Using the provided Python project template, your task is to implement a URL Shortener web service that exposes
the following API endpoints:

* POST `/url/shorten`: accepts a URL to shorten (e.g. https://www.google.com) and returns a short URL that 
  can be resolved at a later time (e.g. http://localhost:8000/r/abc)
* GET `r/<short_url>`: resolve the given short URL (e.g. http://localhost:8000/r/abc) to its original URL
  (e.g. https://www.google.com). If the short URL is unknown, an HTTP 404 response is returned.

Your solution must support running the URL shortener service with multiple workers.

For example, it should be possible to start two instances of the service, make a request to shorten a URL
to one instance, and be able to resolve that shortened URL by sending subsequent requests to the second instance. 

## Getting Started

To begin the project, clone this repository to your local machine:

```commandline
git clone https://github.com/pocketzworld/url-shortener-tech-test.git
```

This repository contains a skeleton of the URL Shortener web service written in Python 3.11
using the [FastAPI](https://fastapi.tiangolo.com/) framework.

The API endpoints can be found in `server.py`.

A Makefile and Dockerfile are also included for your convenience to run and test the web service.

Note that you are not required to use Docker or the provided FastAPI skeleton for your implementation, if you are 
more comfortable with other tools or frameworks. Your solution must still meet the requirements described in the 
Project Description. The following sections will assume that you are using Docker and FastAPI, but feel free to 
update the project and make sure to modify the README to reflect how your implementation should be run and tested. 

### Running the service

To run the web service in interactive mode, use the following command:
```commandline
make run
```

This command will build a new Docker image (`pw/url-shortener:latest`) and start a container
instance in interactive mode.

By default, the web service will run on port 8000.

### Testing

Swagger UI is available as part of the FastAPI framework that can be used to inspect and test
the API endpoints of the URL shortener. To access it, start run the web service and go to http://localhost:8000/docs

## Submission Guidelines
When you have completed the project, please follow these guidelines for submission:

1. Commit and push your code to your GitHub repository.
2. Update this README with any additional instructions, notes, or explanations regarding your implementation, if necessary.
3. Provide clear instructions on how to run and test your project.
4. Share the repository URL with the hiring team or interviewer.

## Additional Information
Feel free to be creative in how you approach this project. Your solution will be evaluated based on code quality,
efficiency, and how well it meets the specified requirements. Be prepared to discuss the reasoning behind your
implementation decisions and their trade-offs.

Remember that this project is the basis for the technical interviews, which do include live coding. We will not
ask you to solve an algorithm, but you will be expected to demo your solution and explain your thought process.

Good luck, and we look forward to seeing your URL Shortener project! If you have any questions or need
clarifications, please reach out to us.

## Project Summary

This project implements a **URL Shortener Service** using **FastAPI** with Redis as the storage backend. It exposes two key API endpoints for shortening and resolving URLs, with multiple worker support and handling for various edge cases.

### API Endpoints:
1. **POST** `/url/shorten`: 
   - Accepts a valid HTTP/HTTPS URL and returns a shortened URL.
   - Example input: `{ "url": "https://www.google.com" }`
   - Example output: `{ "short_url": "http://localhost:8000/r/abc123" }`

2. **GET** `/r/<short_url>`: 
   - Resolves the shortened URL to its original URL.
   - Example: `GET /r/abc123` resolves the shortened URL and redirects the user to the original URL (e.g., `https://www.google.com`).
   - If the short URL is unknown, an **HTTP 404 Not Found** response is returned.

---

## How This Solution Meets the Project Requirements

### 1. **API Endpoints:**

- **POST `/url/shorten`**:
   - This endpoint accepts a URL via a POST request and generates a shortened URL.
   - The shortened URL can be later resolved using the `/r/<short_url>` endpoint.
   - Example Request:
     ```bash
     curl -X POST "http://localhost:8000/url/shorten" \
          -H "Content-Type: application/json" \
          -d '{"url": "https://www.google.com"}'
     ```
   - Example Response:
     ```json
     { "short_url": "http://localhost:8000/r/abc123" }
     ```

- **GET `/r/<short_url>`**:
   - This endpoint resolves a previously generated short URL and redirects to the original URL.
   - If the short URL is invalid or does not exist, a **404 Not Found** response is returned.
   - Example Request:
     ```bash
     curl -L "http://localhost:8000/r/abc123"
     ```

### 2. **Multiple Worker Support**:

The solution supports running the service with **multiple workers** as required. This is achieved using **Docker Compose**, which spins up multiple instances of the FastAPI app, allowing the service to handle requests across different instances.

- **How It Works**:
   - You can run two instances of the service using `docker-compose` with multiple workers (`url-shortener-1` and `url-shortener-2`).
   - A request can be made to shorten a URL on one instance (`url-shortener-1`), and the shortened URL can be resolved by making a request to another instance (`url-shortener-2`).
   - Redis is used as the centralized data store, ensuring consistency across all workers.

- **Testing**: 
   - Start the system with Docker Compose:
     ```bash
     docker-compose up --build
     ```
   - Make a request to shorten a URL using one instance, and resolve the shortened URL using the other instance. Both instances communicate with the same Redis instance, ensuring the service behaves correctly across multiple workers.

### 3. **Handling Edge Cases**:

The service has been built to handle several edge cases:

1. **Duplicate URL Handling**: 
   - If the same URL is shortened multiple times, the service returns the same short URL instead of generating a new one. This avoids duplicate entries in Redis.

2. **Collision Handling**: 
   - The system ensures that there are no key collisions when generating short URLs. If a collision is detected, a new short URL is generated until a unique one is found.

3. **Redis Outage Handling**: 
   - If Redis is unavailable, the service returns a **503 Service Unavailable** response, ensuring that the application doesn't crash and users receive a meaningful error message.

4. **Case-Insensitive Short URLs**: 
   - Shortened URLs are case-insensitive. Regardless of how the user inputs the shortened URL (e.g., `abc123`, `ABC123`), it will resolve correctly to the original URL.

5. **URL Validation**: 
   - Only valid HTTP/HTTPS URLs are accepted. Malformed URLs are rejected with a **422 Unprocessable Entity** response and a clear error message.

---

## How to Run the Service

1. **Running with Docker Compose**:
   - To start the service with multiple workers and Redis, use the following command:
     ```bash
     docker-compose up --build
     ```
   - This will start two instances of the URL shortener service and a Redis instance.

2. **Testing the Service**:
   - The service can be tested via **Swagger UI** available at `http://localhost:8000/docs` or using `curl` commands.
   - Example `curl` request to shorten a URL:
     ```bash
     curl -X POST "http://localhost:8000/url/shorten" \
          -H "Content-Type: application/json" \
          -d '{"url": "https://www.google.com"}'
     ```
   - Example `curl` request to resolve a shortened URL:
     ```bash
     curl -L "http://localhost:8000/r/abc123"
     ```

---

## Environment and Dependencies

- **FastAPI**: The web framework used to build the service.
- **Redis**: Used as a centralized key-value store for storing URL mappings. Ensure Redis is running as part of the Docker Compose setup.
- **Pydantic**: Used for data validation to ensure that only valid HTTP/HTTPS URLs are accepted.
- **Docker**: The service is containerized with Docker and can be easily run with multiple workers using Docker Compose.

### Notes:
- Make sure **Redis** is installed or available via Docker to run the service successfully.
- All dependencies are listed in `requirements.txt`. To install them manually, run:
  ```bash
  pip install -r requirements.txt

