from ghosts.database import Spectre, db
from ghosts.generator import generate
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
import random

views = Blueprint('views', __name__)

def generate_gids(n):
  ids = []

  while len(ids) < n:
    nid = "".join([chr(random.randint(65,90)) for _ in range(8)])

    if Spectre.query.filter_by(gid=nid).first() == None:
      ids.append(nid)
  
  return tuple(ids)

@views.route('/')
def index():
  return render_template('main/index.html')

@views.route('/continue', methods=['POST'])
def cont():
  old_gid = request.form["gid"].upper()

  s = Spectre.query.filter_by(gid=old_gid).first()
  
  if s == None:
    flash("Ghost ID %s not found" % old_gid, 'danger')
    return redirect(url_for('views.index'))
  
  gids = generate_gids(2)
  
  for gid in gids:
    new_spectre = Spectre(gid=gid, tree_id=s.tree_id, parent=s)
    db.session.add(new_spectre)
  
  db.session.commit()

  filename = generate(gids)

  return send_file(filename)

@views.route('/new')
def new():
  qry = Spectre.query.filter_by(is_root=True).order_by(Spectre.tree_id.desc()).first()

  print(qry)

  if qry == None:
    tree_id = 1
  else:
    tree_id = qry.tree_id + 1
  
  new_spectre = Spectre(gid=generate_gids(1)[0], tree_id=tree_id, is_root=True)
  db.session.add(new_spectre)
  db.session.commit()

  gids = generate_gids(2)
  
  for gid in gids:
    new_spectre = Spectre(gid=gid, tree_id=tree_id, parent=new_spectre)
    db.session.add(new_spectre)
  
  db.session.commit()

  filename = generate(gids)

  return send_file(filename)
