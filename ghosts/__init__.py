from flask import Flask
from sqlalchemy_utils import database_exists
from sqlalchemy.engine.url import make_url

def create_app(config='ghosts.config.Config'):
  app = Flask(__name__)
  app.config.from_object(config)

  with app.app_context():
    # Database Setup
    from ghosts.database import db
    url = make_url(app.config['SQLALCHEMY_DATABASE_URI'])
    if not database_exists(url):
      db.create_all()

    # Views Setup
    from ghosts.views import views
    app.register_blueprint(views)

  return app
