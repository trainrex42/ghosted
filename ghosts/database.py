from flask_sqlalchemy import SQLAlchemy
from flask import current_app

db = SQLAlchemy(current_app)

class Spectre(db.Model):
  __tablename__ = "spectres"

  id = db.Column(db.Integer, primary_key=True)
  gid = db.Column(db.String(8), unique=True)
  active = db.Column(db.Boolean, default=False)
  is_root = db.Column(db.Boolean(), default=False)

  haunt_id = db.Column(db.Integer, db.ForeignKey("haunts.id"))
  parent_id = db.Column(db.Integer, db.ForeignKey("spectres.id"))

  children = db.relationship("Spectre", backref=db.backref('parent', remote_side=[id]))

  def as_dict(self):
    return dict(id=self.id, parent_id=self.parent_id, active=self.active, is_root=self.is_root, children=[i.id for i in self.children])

class Haunt(db.Model):
  __tablename__ = "haunts"

  id = db.Column(db.Integer, primary_key=True)

  ghosts = db.relationship("Spectre", backref=db.backref('haunt', remote_side=[id]))
