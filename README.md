# Single Sign-On Example

This project demonstrates a basic implementation of Single Sign-On (SSO) using Flask in Python. It consists of an SSO server and a service application, showcasing how authentication can be centralized and shared across multiple services.

## Project Structure

The project is divided into two main components:

1. **SSO Server**: Handles user authentication and token generation.
2. **Service**: A sample application that relies on the SSO server for user authentication.

## Features

- User registration and login through the SSO server
- Token-based authentication
- Secure password hashing using bcrypt
- Simple service integration with SSO

## UI Flow

The Single Sign-On process follows this general flow:

1. User attempts to access the service application.
2. Service redirects the user to the SSO server login page.
3. User enters credentials on the SSO server login page.
4. SSO server authenticates the user and generates a token.
5. SSO server redirects the user back to the service with the token.
6. Service verifies the token with the SSO server.
7. If valid, the service grants access to the user.

## Prerequisites

- Python 3.x
- Flask
- bcrypt
- requests

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/jeffreyleeon/single-sign-on-example.git
   cd single-sign-on-example
   ```

2. Install the required dependencies:
   ```
   pip install flask bcrypt requests
   ```

## Usage

1. Start the SSO server:

   ```
   python sso_server.py
   ```

2. In a separate terminal, start the service:

   ```
   python service.py
   ```

3. The SSO server will run on `http://localhost:5000`, and the service will run on `http://localhost:5001`.

## API Endpoints

### SSO Server

- `POST /register`: Register a new user
- `POST /login`: Authenticate a user and receive a token
- `GET /verify`: Verify a token

### Service

- `GET /`: Access the service (requires authentication)

## Testing

You can use cURL or any API testing tool to interact with the SSO server and service. For example:

1. Register a user:

   ```
   curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser","password":"password123"}' http://localhost:5000/register
   ```

2. Login and obtain a token:

   ```
   curl -X POST -H "Content-Type: application/json" -d '{"username":"testuser","password":"password123"}' http://localhost:5000/login
   ```

3. Access the service using the obtained token:
   ```
   curl -H "Authorization: Bearer <your_token>" http://localhost:5001/
   ```

## Security Considerations

This is a basic example and should not be used in production without further security enhancements. Consider implementing:

- HTTPS for all communications
- More robust token management (e.g., JWT with expiration)
- Additional security headers
- Rate limiting
- Input validation and sanitization
