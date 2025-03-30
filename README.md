# GraphQL API

## Description
- __Simple GraphQL API, built with [Strawberry](https://strawberry.rocks/) and [FastAPI](https://fastapi.tiangolo.com/)__  
- __[Strawberry](https://strawberry.rocks/) is a developer friendly [GraphQL](https://graphql.org/) library for Python, designed for modern development.__  
- __[GraphQL](https://graphql.org/) is a query language for APIs and a runtime for fulfilling queries with existing data. GraphQL provides a complete and understandable description of the data in API, gives clients the power to ask for exactly what they need and nothing more, makes it easier to evolve APIs over time, and enables powerful developer tools.__

## Brief overview

![image](https://github.com/KERELKO/Strawberry-fastapi-product-service/assets/89779202/493f4c2e-25ed-462d-b018-822fd7e03169)

## Technologies
- [FastAPI](https://fastapi.tiangolo.com/)
- [Postgresql](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Strawberry](https://strawberry.rocks/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/)
- [GraphQL](https://graphql.org/)

## How To Use
### Requirements
- Docker
- Docker-compose
- Maketools
### Installation
1. Install the project with
```
git clone https://github.com/KERELKO/strawberry-fastapi-product-service
```
2. Move to directory with __Dockerfile__ and create **.env** file based on **.env.example**
```
touch .env
cat .env.example > .env
```
3. In the same directory run
```
docker compose up
```
4. Go to http://localhost:8000/graphql in your browser and make your queries!

![image](https://github.com/KERELKO/Fastapi-Graphql-product-service/assets/89779202/0546bd5c-2e63-4995-a77f-e776faf8ba6f)

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Please follow the existing code style and ensure that all tests pass before submitting your changes.

## Project structure
```
.
├── alembic.ini
├── docker-compose.yaml
├── Dockerfile
├── entrypoint.sh
├── LICENSE
├── Makefile
├── poetry.lock
├── pyproject.toml
├── README.md
├── src
│   ├── api
│   │   ├── graphql
│   │   │   ├── __init__.py
│   │   │   └── v1
│   │   │       ├── converters
│   │   │       │   ├── __init__.py
│   │   │       │   ├── product.py
│   │   │       │   ├── review.py
│   │   │       │   └── user.py
│   │   │       ├── exceptions.py
│   │   │       ├── __init__.py
│   │   │       ├── interfaces.py
│   │   │       ├── mutations
│   │   │       │   ├── __init__.py
│   │   │       │   ├── inputs.py
│   │   │       │   ├── mutation.py
│   │   │       │   ├── product.py
│   │   │       │   ├── review.py
│   │   │       │   └── user.py
│   │   │       ├── queries
│   │   │       │   ├── __init__.py
│   │   │       │   ├── product.py
│   │   │       │   ├── query.py
│   │   │       │   ├── review.py
│   │   │       │   └── user.py
│   │   │       ├── resolvers
│   │   │       │   ├── base.py
│   │   │       │   ├── __init__.py
│   │   │       │   ├── product.py
│   │   │       │   ├── review.py
│   │   │       │   └── user.py
│   │   │       └── utils.py
│   │   └── __init__.py
│   ├── core
│   │   ├── constants.py
│   │   ├── db
│   │   │   ├── __init__.py
│   │   │   └── sqlalchemy
│   │   │       ├── base.py
│   │   │       ├── extensions.py
│   │   │       ├── __init__.py
│   │   │       └── models.py
│   │   ├── di.py
│   │   ├── dto.py
│   │   ├── exceptions.py
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── utils.py
│   ├── __init__.py
│   ├── main.py
│   └── repositories
│       ├── base.py
│       ├── __init__.py
│       └── sqlalchemy
│           ├── __init__.py
│           ├── product.py
│           ├── review.py
│           └── user.py
└── tests
```

## TODO
- [ ] Tests
- [x] Mutations
- [ ] Logging
- [ ] Pointer-based Pagination
- [x] At least partly solve the N+1 problem
- [x] Remake folder structure
