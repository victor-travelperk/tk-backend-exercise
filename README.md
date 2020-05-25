# Recipe app backend

## Assumptions

- For simplicity sake, this application will not need need for authentication or authorization.
- Docstrings have only been added when there is additional context needed for a method.
- There cannot be a recipe without ingredients.

## Requirements

This Project requires the use of docker and docker-compose

## How to startup the application

Run the following commands

```sh
docker-compose build
docker-compose up
```

## Project structure

The project is separated between 2 django apps:

- Core: Stores the models of the application
- Recipe: Has the serialization and views for recipe related endpoints 

## Scripts

To facilitate development, helper scripts have been created inside the `scripts` folder  

- `start.sh`: Runs the application locally.
- `test.sh`: Runs all the tests in the application. 
- `makemigrations.sh`: Generates migrations for the application.
  