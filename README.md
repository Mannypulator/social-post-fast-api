# Simple Social - FastAPI Social Media App

A lightweight social media application built with FastAPI and Streamlit. Share images and videos with your friends in a clean, simple interface.

> **Note**: This project was built following [this YouTube tutorial](https://www.youtube.com/watch?v=SR5NYCdzKkc) on building FastAPI applications.

## Features

- 🔐 **User Authentication** - Secure JWT-based authentication with FastAPI Users
- 📸 **Media Upload** - Upload and share images and videos
- 🏠 **Feed** - View posts from all users in chronological order
- 🗑️ **Post Management** - Delete your own posts
- ☁️ **Cloud Storage** - Media stored on ImageKit CDN
- 🎨 **Modern UI** - Clean Streamlit interface

## Tech Stack

### Backend

- **FastAPI** - Modern, fast web framework
- **FastAPI Users** - Authentication and user management
- **SQLAlchemy** - ORM with async support
- **SQLite** - Database (easily swappable)
- **ImageKit** - Media storage and CDN
- **Uvicorn** - ASGI server

### Frontend

- **Streamlit** - Interactive web interface
- **Requests** - HTTP client

## Prerequisites

- Python 3.13+
- ImageKit account (for media storage)
- `uv` package manager (recommended) or `pip`

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd book-fast-api
   ```

2. **Install dependencies**

   Using `uv`:

   ```bash
   uv sync
   ```

   Or using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:

   ```env
   SECRET=your-jwt-secret-here
   IMAGEKIT_PRIVATE_KEY=your-imagekit-private-key
   IMAGEKIT_PUBLIC_KEY=your-imagekit-public-key
   IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your-imagekit-id
   ```

   Generate a secure JWT secret:

   ```bash
   openssl rand -base64 32
   ```

## Usage

### Start the Backend API

```bash
uvicorn app.app:app --host 0.0.0.0 --port 8080 --reload
```

The API will be available at `http://localhost:8080`

### Start the Frontend

In a new terminal:

```bash
streamlit run frontend.py
```

The app will open in your browser at `http://localhost:8501`

## API Documentation

Once the backend is running, visit:

- **Interactive API docs**: http://localhost:8080/docs
- **Alternative docs**: http://localhost:8080/redoc

## Project Structure

```
book-fast-api/
├── app/
│   ├── app.py          # Main FastAPI application
│   ├── db.py           # Database models and setup
│   ├── schemas.py      # Pydantic schemas
│   ├── users.py        # User authentication setup
│   └── images.py       # ImageKit configuration
├── frontend.py         # Streamlit frontend application
├── main.py            # Entry point
├── pyproject.toml     # Project dependencies
├── .env               # Environment variables (not in git)
└── README.md          # This file
```

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/jwt/login` - Login and get access token
- `POST /auth/jwt/logout` - Logout

### Users

- `GET /users/me` - Get current user info

### Posts

- `POST /upload` - Upload media and create post
- `GET /feed` - Get all posts (newest first)
- `DELETE /posts/{post_id}` - Delete your post

## Development

### Database Migrations

The database is automatically created on first run. To reset the database:

```bash
rm test.db
```

The tables will be recreated on the next API request.

### Configuration

To change the database from SQLite to PostgreSQL or another database:

1. Update `DATABASE_URL` in [app/db.py](app/db.py)
2. Install the appropriate database driver
3. Update dependencies in [pyproject.toml](pyproject.toml)

## Environment Variables

| Variable                | Description                       | Required |
| ----------------------- | --------------------------------- | -------- |
| `SECRET`                | JWT secret key for authentication | Yes      |
| `IMAGEKIT_PRIVATE_KEY`  | ImageKit private API key          | Yes      |
| `IMAGEKIT_PUBLIC_KEY`   | ImageKit public API key           | Yes      |
| `IMAGEKIT_URL_ENDPOINT` | ImageKit CDN endpoint URL         | Yes      |

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For issues and questions, please open an issue on GitHub.

## Roadmap

- [ ] Add comments on posts
- [ ] Add likes/reactions
- [ ] User profiles with bio
- [ ] Follow/unfollow users
- [ ] Private/public posts
- [ ] Image filters and editing
- [ ] Direct messaging
- [ ] Notifications

---

Built with ❤️ using FastAPI and Streamlit
