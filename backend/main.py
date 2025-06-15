import os
from app import create_app
from dotenv import load_dotenv

# Determine environment and load appropriate .env file
env = os.getenv('FLASK_ENV', 'development')
env_file = f".env.{env}"

if os.path.exists(env_file):
    load_dotenv(env_file)
else:
    load_dotenv()

# Create app with environment configuration
app = create_app(env)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)