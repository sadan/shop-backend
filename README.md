# Shop

A simple e-commerce shop backend built with Django.

# Services

It supports following APIs.

|Function        |API                            |
|----------------|-------------------------------|
|Products list.  |`GET /api/products/`           |
|Product detail. |`GET /api/products/<id>/`      |
|Orders list.	 |`GET /api/orders/`			 |
|Orders detail.	 |`GET /api/orders/<order_id>/`  |
|Order create.	 |`POST /api/orders/<order_id>/` |

## Authentication

All the endpoints are require auth protected and only work by providing a JWT token. There are two endpoints which support authentication.

|Function        |API                            |
|----------------|-------------------------------|
|Get token.      |`POST /api/token/`             |
|Refresh token.  |`POST /api/token/refresh/`     |

1. `token` endpoint uses *username* and *password* and returns **refresh** and **access** token with 1 day and 5 minutes of lifetime respectively. 
    ```
    curl --location --request POST 'http://localhost:8000/api/token/' \
    --header 'Content-Type: application/json' \
    --data '{
        "username": "username",
        "password": "password"
    }'
    ```
2. If **access** token expires, you can use **refresh** token to get the new token.
    ```
    curl --location --request POST 'http://localhost:8000/api/token/refresh/' \
    --header 'Content-Type: application/json' \
    --data '{
        "refresh": "refresh-token-from-api-token"
    }'
    ```
3. Once you have a valid **access** token you can use that to make other API calls by passing it in the *Authorization* headers.
    ```
    curl --location --request GET 'http://localhost:8000/api/products/' \
    --header 'Authorization: Bearer valid-access-token'
    ```

# Components

This application has following major components.

## Product(s)
Stores all the information regarding products. Users can view available products in a paginated form and their quantity in stock and place orders. 

## Order(s)
Users can place orders by providing list of products and the quantity. If the product has sufficient quantity in stock the orders will be placed and products will be deducted from the database. Users can also view their previous orders.

# Development

Application is built with Python3.9 and you need Docker to run the application locally. Once you have the Docker installed run following command to start the application. It will run the Django server and create a database.
```
make docker/compose/up
```

Run following command to create database schema.
```
make docker/compose/migrate
```

There is a management command that can be used to create some test data to play with. 
```
docker-compose exec web /app/venv/bin/python src/manage.py add_products
```

When application is running, you can run unittest with following command.
```
make docker/compose/unittest
```

Following are some useful commands from Makefile:
1. `make docker/compose/up` to start the server.
2. `make docker/compose/build` to build the docker image.
3. `make docker/compose/migrate` run migrations.
4. `make docker/compose/makemigrations` make migrations after model changes.
5. `make venv` create development environment locally.
6. `make format` formats the code.

## Requirements
**requirements.txt** at the root directory is generated with *pip-compile*. Whenever you have to update the requirements, remove the file and run following command 
```
make requirements.txt
```

# Improvements

This is not a production level application yet. There are still lots of things that should be improved.
1. Logging and monitoring. We can implement Sentry for logging and should write API metrics for monitoring.
2. Enhancements in data models. For example we can include `status` in the order to keep track of it's progress.
3. Feature enhancements, like right now product stock is deducted all the time an order is placed but if order is getting updated we may have to add items back to stock.
4. Test coverage.
5. CI/CD pipelines.
6. API documentation. We can use tools like swagger combined with drf-yasg to build interactive docs.

# Deployment

We have already containerized this application with multiple stages in Dockerfile for each environment. With that in place we can deploy this application to AWS managed services like EKS (elastic kubernetes service) or ECS (elastic container services). On Github we can write actions to easily deploy the application and add steps in our actions to check code quality and tests coverage. During deployment we can build a container with **prod** stage in Dockerfile and push that to ECR (elastic container registry) and from there it can be used in EKS or ECS.