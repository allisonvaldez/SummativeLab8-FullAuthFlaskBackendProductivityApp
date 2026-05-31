# Flask Productivity API

A secure Flask REST API for a personal notes productivity app with full authentication.

## Description

Users can sign up, log in, and manage their own private notes. All note endpoints are protected — users can only view, create, edit, and delete their own notes.

## Installation

```bash
pipenv install
pipenv shell
cd server
python3 -m flask db init
python3 -m flask db migrate -m "initial"
python3 -m flask db upgrade
python3 seed.py
```

## Running the App

```bash
python3 app.py
```

## Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | /signup | Create a new user account |
| GET | /check_session | Check if user is logged in |
| POST | /login | Log in with username and password |
| DELETE | /logout | Log out current user |
| GET | /notes?page=1 | Get paginated list of current user's notes |
| POST | /notes | Create a new note |
| GET | /notes/:id | Get a specific note |
| PATCH | /notes/:id | Update a specific note |
| DELETE | /notes/:id | Delete a specific note |