from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db,User


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY']='JISOO'
debug = DebugToolbarExtension(app)

#set database
connect_db(app)
db.create_all()



@app.route('/',methods=['GET'])
def root():
  """# GET / : Redirect to list of users."""
  return redirect("/users")

@app.route('/users',methods=['GET'])
def list():

  """"Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form. """
  users= User.query.all()

  return render_template('list.html',users = users)

@app.route('/users/new',methods=['GET'])
def add_button():
  """Link to the addform"""
  return render_template('newUser.html')
  

@app.route('/users/new',methods=['POST'])
def addUser():
  """Show an add form for users"""
  first_name= request.form.get("first_name")
  last_name= request.form.get("last_name")
  image_url = request.form.get("image_url")

  if not image_url:
      image_url = 'https://blog.kakaocdn.net/dn/bCXLP7/btrQuNirLbt/N30EKpk07InXpbReKWzde1/img.png'

  new_user = User(first_name=first_name,last_name=last_name, image_url=image_url)
  
  db.session.add(new_user)
  db.session.commit()

  return redirect('/users')
  
@app.route('/users/<int:user_id>',methods=['GET'])
def detail(user_id):
  user= User.query.get_or_404(user_id)
  return render_template('details.html', user=user)

@app.route('/users/<int:user_id>/edit',methods=['GET'])
def edit_page(user_id):
  user= User.query.get_or_404(user_id)
  return render_template('edit.html',user=user)

@app.route('/users/<int:user_id>/edit',methods=['POST'])
def edit_update(user_id):
  user =User.query.get_or_404(user_id)
  user.first_name= request.form.get("first_name")
  user.last_name= request.form.get("last_name")
  user.image_url = request.form.get("image_url")

  db.session.add(user)
  db.session.commit()

  return redirect("/users")


@app.route('/users/<int:user_id>/delete',methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')










if __name__ == "__main__":
    app.run(debug=True)