import os
from app import create_app
from dotenv import load_dotenv

# need rmb set flask env in docker
env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env.production'))
else:
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env.development'))

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
