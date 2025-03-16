# Gaia Lifestyle Tracker API

A comprehensive API for tracking daily activities, mood, and receiving AI-powered insights.

## Features

- User authentication and profile management
- Daily activity and mood tracking
- Food, exercise, work, and event logging
- AI-powered analysis of lifestyle patterns and mood correlations
- Personalized activity recommendations

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Anthropic API key (for AI features)

### Installation

1. Clone the repository
2. Create a `.env` file with the following variables:
   ```
   DATABASE_URL=postgresql://postgres:postgres@db:5432/activity_api
   SECRET_KEY=your_secret_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key
   SEED_DB=true
   ```
3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /token   | Obtain JWT token |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /users/ | Create a new user |
| GET    | /users/ | Get all users |
| GET    | /users/{user_id} | Get user by ID |

### Daily Logs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /daily-logs/ | Create a new daily log |
| GET    | /daily-logs/ | Get all daily logs for current user |
| GET    | /daily-logs/{log_id} | Get daily log by ID |
| PUT    | /daily-logs/{log_id} | Update daily log |
| DELETE | /daily-logs/{log_id} | Delete daily log |

### Food Entries

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /daily-logs/{log_id}/food | Add food entry to daily log |
| GET    | /daily-logs/{log_id}/food | Get all food entries for a daily log |

### Exercise Entries

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /daily-logs/{log_id}/exercise | Add exercise entry to daily log |
| GET    | /daily-logs/{log_id}/exercise | Get all exercise entries for a daily log |

### Work Entries

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /daily-logs/{log_id}/work | Add work entry to daily log |

### Event Entries

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /daily-logs/{log_id}/events | Add event entry to daily log |

### Mood Entries

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /daily-logs/{log_id}/mood | Add mood entry to daily log |

### AI Insights

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /insights/analyze/{user_id} | Generate AI insights for user data (requires 7+ days of data) |
| GET    | /insights/recommendations/{user_id} | Get all activity recommendations for a user |
| POST   | /insights/recommendations/{user_id} | Generate a new activity recommendation |
| PUT    | /insights/recommendations/{recommendation_id} | Update recommendation status (mark as completed, add rating) |

### Activities

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /activities/recommendations | Get activity recommendations for current user |
| POST   | /activities/recommendations | Generate a new activity recommendation |
| PUT    | /activities/recommendations/{recommendation_id} | Update recommendation status |

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ANTHROPIC_API_KEY`: API key for Anthropic's Claude
- `SEED_DB`: Whether to seed the database on startup (true/false)

## Development

### Running Tests

```bash
python -m pytest app/tests/
```

### Database Migrations

```bash
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.