# Futsta API
Welcome to the repository of the AWS Lambda based API for the Futsta project!

This project serves as the backend for Futsta, a Flutter application for keeping track of my futsal team statistics (goals/assists).

Mainly this project is used to learn about AWS Lambda, AWS S3 and FastAPI.

To see the frontend part of this app, head over to [futsta-flutter](https://github.com/Thijss/futsta-flutter).

## Local installation
This project's Python version is locked to python 3.10 to keep it compatible with AWS Lambda. 
If you want to run the API locally, you need to have python 3.10 installed.

If you do not plan to deploy the API on AWS Lambda, you can update the python version constraint in `pyproject.toml` and use any python version >= 3.6.

### Install dependencies
```
poetry env use 3.10
poetry install
```

### Set environment variables
copy .env.example to .env and fill in the values
```
cp .env.example .env
```


## AWS Deployment
Checkout [DEPLOYMENT](docs/DEPLOYMENT.md) for a detailed guide on how to deploy the Futsta API on AWS Lambda.


## Roadmap/ToDo
- [ ] Increase test coverage from 80% to 100%
- [ ] Add integration with AWS Cognito for authentication
- [ ] Move setup to an AWS Cloudformation Template
- [ ] Split JSON files of each model into multiple files to allow concurrent writes.
