# Bristol Regional Food Network - Digital Marketplace

## Setup & Running Instructions

### Prerequisites
- Docker Desktop installed and running

### Running the Application
```bash
docker-compose up --build
```

### First Time Setup (in a second terminal)
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Access
- Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

### Stopping
```bash
docker-compose down
```
