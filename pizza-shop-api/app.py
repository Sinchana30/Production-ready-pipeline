import os
import socket
from flask import Flask, jsonify

# Create a new Flask application
app = Flask(__name__)

# --- Configuration ---
# You can change this version number to see your CI/CD pipeline in action!
APP_VERSION = "1.0"

# --- API Endpoints ---

@app.route('/')
def home():
    """The main endpoint, greets the user."""
    # Get the hostname of the container this code is running in
    container_hostname = socket.gethostname()
    
    # Return a simple HTML message
    return f"""
    <html>
        <head>
            <title>Pizza Shop API</title>
        </head>
        <body style='font-family: sans-serif; text-align: center; padding-top: 50px;'>
            <h1>Welcome to the Pizza Shop API! 🍕</h1>
            <p><strong>Version:</strong> {APP_VERSION}</p>
            <p><em>Served by container: {container_hostname}</em></p>
        </body>
    </html>
    """

@app.route('/health')
def health_check():
    """A health check endpoint for Kubernetes to use."""
    # This tells Kubernetes that the application is alive and well.
    return jsonify(
        status="ok",
        version=APP_VERSION
    ), 200


# --- Main execution ---

if __name__ == '__main__':
    # The app will listen on port 5000.
    # The host '0.0.0.0' means it will be accessible from outside the Docker container.
    # This is very important!
    app.run(host='0.0.0.0', port=5000, debug=True)