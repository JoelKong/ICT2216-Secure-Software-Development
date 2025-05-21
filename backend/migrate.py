from app import create_app
from app.db import db

app = create_app()
with app.app_context():
    db.create_all()