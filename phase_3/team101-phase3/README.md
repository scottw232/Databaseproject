# Team 101 Project -- Technical Notes

Members: , Scott Wofford (swofford6), Yutaro Watanabe (ywatanabe31)

## Tech Stack

The web application is built using the following technologies:

- Docker & Docker Compose for containerization and orchestration
- React for the frontend
- MySQL 8.0 for the database

## Spinning up the application

### Prerequisites

- Docker + Docker Compose

### Running the application

```bash
docker-compose up --build
```

Then make sure that the stacks are up:

```bash
docker ps
```

You should see the following containers:
- server
- client
- db

### Browse the application

The application is available at http://localhost:3000
The backend and API documentation is available at http://localhost:8080/docs
The DB is available at http://localhost:3306, with credentials `root`/`password`

Keep in mind that the best practice in terms of backend development, frontend development, and secret management are all completely out of the scope of the project, and is being used here for demonstration purposes only.