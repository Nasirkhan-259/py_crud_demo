# Python (Flask) User CRUD API

## Project Overview
This project implements a CRUD (Create, Read, Update, Delete) API for managing users using Python and Flask. The API supports operations for user management, such as adding new users, updating user information, deleting users, and retrieving the list of all users. The backend uses MySQL for data storage and provides endpoint functionalities to perform these operations.

## Objectives
- **CRUD Operations**: Implement basic CRUD functionalities (Create, Read, Update, Delete) for managing users.
- **Data Validation**: Ensure that the input data is validated for required fields and correct formats.
- **Password Encryption**: Implement password hashing and encryption to secure user passwords.
- **Error Handling**: Provide meaningful error messages for invalid requests and edge cases.
- **Pagination**: Implement pagination for listing users to handle large datasets efficiently.
- **API Testing**: Ensure the API is easily testable using Postman or similar tools.

## Technology Stack
- **Backend**: Python (Flask)
- **Database**: MySQL
- **Password Hashing**: bcrypt
- **API Testing**: Postman

## Features
- **User Creation**: Add new users with unique usernames and securely hashed passwords.
- **User Retrieval**: Fetch all users with pagination support.
- **User Update**: Update user information, including username, password, and active status.
- **User Deletion**: Delete users by their unique ID.
- **Error Handling**: Return appropriate error responses for invalid input or user not found.

## API Endpoints
- `POST /user`: Create a new user.
- `GET /user`: Retrieve all users with pagination.
- `GET /user/{id}`: Retrieve a user by ID.
- `PUT /user/{id}`: Update a user's information by ID.
- `DELETE /user/{id}`: Delete a user by ID.

## Algorithm Used
- **Password Encryption**: bcrypt is used for securely hashing user passwords before storing them in the database.
- **Pagination**: The API supports paginated results when listing users to ensure efficient handling of large datasets.
- **Data Validation**: User inputs are validated for required fields, unique constraints (e.g., username), and correct formats.

## Conclusion
This project provides a simple, yet secure, Python-based CRUD API for managing user data with Flask and MySQL. The system ensures data integrity through validation, secures sensitive information using password encryption, and supports efficient data retrieval with pagination.
