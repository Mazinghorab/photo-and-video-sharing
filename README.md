# Photo and Video Sharing Platform

A full-stack, web application built with **FastAPI** and **Streamlit** that allows users to securely register, log in,share photos, and videos. Media uploads and dynamic transformations (like image captions) are handled seamlessly through the **ImageKit** API.

## Features

* **Secure Authentication**: JWT-based user registration and login powered by `fastapi-users`.
* **Media Uploads**: Direct backend integration with ImageKit for optimized photo and video hosting.
* **Dynamic Transformations**: Image captions are rendered dynamically using ImageKit's URL transformation parameters.
* **Personalized Feed**: Asynchronous SQLite database (via SQLAlchemy) to fetch and display posts.
* **Protected Routes**: Users can only delete their own posts, and media uploads require a valid JWT token.
* **Modern Tooling**: Managed via `uv`, the extremely fast Python package and project manager.

## Tech Stack

* **Backend**: FastAPI, Python 3
* **Frontend**: Streamlit
* **Database & ORM**: SQLite, SQLAlchemy (Async), `aiosqlite`
* **Authentication**: `fastapi-users` (JWT Strategy)
* **Media Storage**: ImageKit via `imagekitio`
* **Package Manager**: `uv`

---

##  Getting Started

### Prerequisites
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python package manager).
2. Create a free account on [ImageKit.io](https://imagekit.io/) and navigate to your **Developer Options** to get your API keys.

### 1. Clone the Repository

```bash
git clone https://github.com/Mazinghorab/photo-and-video-sharing.git
cd photo-and-video-sharing
```

### 2. Configure Environment Variables
Create a `.env` file in the root of the project and add your ImageKit credentials:

```env
IMAGEKIT_PRIVATE_KEY=your_private_key_here
IMAGEKIT_PUBLIC_KEY=your_public_key_here
IMAGEKIT_URL=your_url_endpoint_here
```

### 3. Install Dependencies
Let `uv` resolve and install the dependencies into an isolated virtual environment:
```bash
uv sync
```

### 4. Run the Backend API
Start the FastAPI server.
```bash
uv run main.py
```
*The API will be available at `http://localhost:8000`.*

### 5. Run the Streamlit Frontend
Open a **new terminal window**, ensure you are in the project root, and launch the user interface:
```bash
uv run streamlit run frontend.py
```
*The application will automatically open in your default web browser.*

---

## Project Structure

```text
photo-and-video-sharing/
├── src/
│   ├── __init__.py
│   ├── app.py          # FastAPI application routing and endpoints
│   ├── db.py           # SQLAlchemy models and async engine setup
│   ├── images.py       # ImageKit configuration and file processing logic
│   ├── schemas.py      # Pydantic models for data validation
│   └── users.py        # JWT auth strategy and UserManager setup
├── frontend.py         # Streamlit user interface
├── main.py             # Uvicorn entry point for the backend
├── pyproject.toml      # Project metadata and uv dependencies
├── uv.lock             # Exact dependency versions
└── .env                # Secret keys (ignored by git)
```

## Core API Endpoints

* `POST /auth/register`: Register a new user.
* `POST /auth/jwt/login`: Authenticate and receive a JWT access token.
* `GET /feed`: Retrieve all media posts (requires JWT).
* `POST /upload`: Upload an image or video to ImageKit and save the post (requires JWT).
* `DELETE /post/{id}`: Delete a specific post (requires JWT & ownership).