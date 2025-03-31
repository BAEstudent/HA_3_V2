### Readme cгенерирован при помощи LLM DeepSeek

# FastAPI URL Shortener Service

A lightweight URL shortener service with user authentication and link management capabilities, built with FastAPI and SQLite.

## Features

- 🔒 **JWT Authentication**: Secure user registration and login
- 🔗 **URL Shortening**: Create short codes for any valid URL
- 👤 **User Management**:
  - Registered users can manage their links (view/delete)
  - Support for anonymous link creation
- ⚡ **FastAPI Benefits**:
  - Automatic API documentation (Swagger UI)
  - Async ready
  - Production-ready foundation

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostreSQL (withSQLAlchemy ORM)
- **Authentication**: JWT tokens
- **Validation**: Pydantic models

## Installation

1. Clone repository:
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener

## API Documentation
