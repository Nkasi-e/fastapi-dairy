# MY DAIRY

[![Dairy FastAPI](https://github.com/Nkasi-e/fastapi-dairy/actions/workflows/build-deploy.yml/badge.svg)](https://github.com/Nkasi-e/fastapi-dairy/actions/workflows/build-deploy.yml) <a href='https://coveralls.io/github/Nkasi-e/fastapi-dairy?branch=deploy'><img src='https://coveralls.io/repos/github/Nkasi-e/fastapi-dairy/badge.svg?branch=deploy' alt='Coverage Status' /></a>

An API that helps users keep records of their daily ordeals or activities.

## Features

- [x] Users can create account.
- [x] Authenticated users can create diary log entries to keep their daily records of activities.
- [x] Users Can delete entry records.
- [x] Users can update entry records.
- [x] Users can get all the entry records belonging to their account.
- [x] Users can get a single entry record with the unique id.

## Getting Started

### Prerequisites

In order to run this project locally, you would need to have the following installed on your local machine.

- Python ^3.10,
- PostgreSQL
- Docker (Optional)

### Installation

- Clone this repository

```bash
git clone [https://github.com/Nkasi-e/fastapi-dairy.git]

```

- update env with .env.example.txt
- Download all dependecies using ```pip install -r requirements.txt``` or ```poetry install``` that's if you have poetry package manager installed already on your machine

### to start up server

- run ```uvicorn app.main:app --reload```

### to start up container in detached mode

- run ```docker-compose -f decker-compose-dev.yml up -d```
