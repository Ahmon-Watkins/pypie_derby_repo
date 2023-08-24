from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

from flask import render_template, request, redirect, session, flash
# import the class from friend.py


from flask_app.models.user import User
from flask_app.models.pie import Pie
from flask_app.models.vote import Vote
# from flask_app.models.friend import Friend



@app.route('/')
def index():
    return render_template('login_registration.html')
#Create new users

@app.route("/user/register", methods=["POST"])
def user_register():
    # Validation
    if not User.validate_user(request.form):
        # Redirect back to the registration form if validation fails
        return redirect('/')

    # Hash the password
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    # Prepare user data
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    # Create user and store user_id in session
    user_id = User.create(data)
    session['user_id'] = user_id

    # Redirect to the user profile page
    return redirect(f'/dashboard/{user_id}')

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    user_id = user_in_db.id
    # never render on a post!!!

    return redirect(f"/dashboard/{user_id}")

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):

    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/')

    user = User.get_one(user_id)
    if user is None:
        flash("User not found")
        return redirect('/')
    
    user_id = session['user_id']
    user_pies = Pie.get_pies_by_user_id(user_id) 

    all_the_pies = Pie.get_all_pies_with_creator()  # Fetch all pies with their creators
    all_the_pies.reverse()

    vote_counts = {}  # Dictionary to store vote counts for each pie

    for pie in all_the_pies:
        vote_counts[pie.id] = Vote.get_vote_count(pie.id)

    return render_template("dashboard.html", user=user, user_pies=user_pies)



