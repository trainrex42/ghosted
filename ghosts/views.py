from ghosts.database import Spectre, db, Haunt
from ghosts import generator
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, session, abort, jsonify
import random, os

views = Blueprint('views', __name__)

def generate_gids(n):
  ids = []

  while len(ids) < n:
    nid = "".join([chr(random.randint(65,90)) for _ in range(8)])

    if Spectre.query.filter_by(gid=nid).first() == None:
      ids.append(nid)
  
  return tuple(ids)

def generate_ghosts(parent_gid):
  parent = Spectre.query.filter_by(gid=parent_gid).first()

  gids = generate_gids(2)
  
  for gid in gids:
    new_spectre = Spectre(gid=gid, haunt=parent.haunt, parent=parent)
    db.session.add(new_spectre)
  
  db.session.commit()

  filename = generator.generate(gids)

  path = os.path.join(os.getcwd(), filename)


  def generate():
    with open(path, 'rb') as f:
        yield from f

    os.remove(path)
  
  r = current_app.response_class(generate(), mimetype='application/pdf')
  r.headers.set('Content-Disposition', 'attachment', filename='ghosts.pdf')

  return r

@views.route('/')
def index():
  if "gid" in session:
    gid = True
  else:
    gid = False
  return render_template('main/index.html', gid=gid)

@views.route('/continue', methods=['POST'])
def cont():
  gid = request.form["gid"].upper()

  s = Spectre.query.filter_by(gid=gid).first()
  
  if s == None:
    flash("Ghost ID %s not found" % gid, 'danger')
    return redirect(url_for('views.index'))
  else:
    if not s.active:
      s.active = True
      db.session.commit()

    session["gid"] = gid
    return redirect(url_for('views.profile'))

@views.route('/new')
def new():
  h = Haunt()
  db.session.add(h)
  db.session.commit()

  new_root = Spectre(gid=generate_gids(1)[0], is_root=True, active=True, haunt=h)
  db.session.add(new_root)
  db.session.commit()

  session["gid"] = new_root.gid
  flash("Your ghost ID is: %s" % new_root.gid, 'info')
  return redirect(url_for('views.profile'))

@views.route('/dashboard')
def profile():
  if "gid" not in session:
    return redirect(url_for('views.index'))
  else:
    s = Spectre.query.filter_by(gid=session["gid"]).first()
    return render_template("main/profile.html", user=s)


@views.route('/generate')
def make_ghosts():
  if "gid" not in session:
    return redirect(url_for('views.index'))
  else:
    return generate_ghosts(session["gid"])

@views.route('/network')
def network():
  if "gid" not in session:
    abort(403)
  else:
    s = Spectre.query.filter_by(gid=session["gid"]).first()
    n = Spectre.query.filter_by(haunt=s.haunt).all()

    d = [i.as_dict() for i in n]

    return jsonify(d)
