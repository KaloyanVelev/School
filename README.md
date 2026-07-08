# Environment Configuration Guide

To run this application, you must configure a local `.env` file in the root directory of your project. This file houses database URLs, security signing keys, and initial setup variables.

Create a file named `.env` in your project root and paste the following parameters:

```text
DB_USER='postgres'
DB_PASSWORD='your_db_password'
DB_HOST='localhost'
DB_PORT='5432'

APP_PORT=8080

ADMIN_EMAIL='youremail@gmail.com'
ADMIN_PASSWORD='your@admin@password123FswSf'
ADMIN_FIRST_NAME='dummy'
ADMIN_LAST_NAME='shtain'
