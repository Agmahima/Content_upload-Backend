# Movie Database API

This is a Flask-based API for managing a movie database. The API allows for uploading movie data from CSV files, as well as retrieving and filtering movie records from a PostgreSQL database.

## Features

- Upload movie data via CSV files.
- Retrieve movie data with pagination, sorting, and filtering options.
- Create a PostgreSQL database table to store movie information.

## Requirements

- Python 3.x
- Flask
- psycopg2
- pandas
- python-dotenv

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
## Run the application:
- python app.py

## Upload a CSV file:
- Make a POST request to /upload with the file included in the form-data. Example using Postman:

- URL: http://localhost:5000/upload
- Method: POST
- Body: Form-data
- Key: file, Value: <select your CSV file>

## Get movies:
- Make a GET request to /movies with optional query parameters:

- URL: http://localhost:5000/movies?page=1&per_page=10&sort_by=id&sort_order=asc&filter_by=original_language&filter_value=en
- Method: GET
