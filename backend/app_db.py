SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:admin@localhost:5432/diplom'

def get_current_db(app):
    with app.app_context():
        return app.db
