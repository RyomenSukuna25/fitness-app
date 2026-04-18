from flask import Flask, render_template, request, redirect
from config import Config
from models import db, User, Progress
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return redirect("/dashboard")

# REGISTER
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            password=request.form["password"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect("/dashboard")

    return render_template("login.html")

# LOGOUT
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

# DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    data = Progress.query.filter_by(user_id=current_user.id).all()
    
    latest = data[-1].weight if data else "No data"

    return render_template("dashboard.html", data=data, latest=latest)

# ADD WEIGHT
@app.route("/add_weight", methods=["POST"])
@login_required
def add_weight():
    try:
        weight = float(request.form["weight"])

        # ❌ reject invalid values
        if weight <= 0 or weight > 300:
            return "Invalid weight entered"

        entry = Progress(weight=weight, user_id=current_user.id)
        db.session.add(entry)
        db.session.commit()

    except:
        return "Error in input"

    return redirect("/dashboard")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)