from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Spectre(db.Model):
  __tablename__ = "spectres"

  id = db.Column(db.Integer, primary_key=True)
  gid = db.Column(db.String(8), unique=True)
  tree_id = db.Column(db.Integer)
  parent_id = db.Column(db.Integer, db.ForeignKey("spectres.id"))

  is_root = db.Column(db.Boolean(), default=False)
  children = db.relationship("Spectre", backref=db.backref('parent', remote_side=[id]))
