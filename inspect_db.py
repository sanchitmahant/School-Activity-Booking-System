from app import app, db
from sqlalchemy import inspect

with app.app_context():
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('tutor')]
    for col in columns:
        print(col)
