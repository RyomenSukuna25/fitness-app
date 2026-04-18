from flask import Flask, render_template, request, redirect, url_for
from config import Config
from models import db, User, Progress, Tracker
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return redirect("/dashboard")

# 🔐 AUTH
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = User(username=request.form["username"], password=request.form["password"])
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

# 📊 DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    progress = Progress.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", progress=progress)

# ⚖️ ADD WEIGHT
@app.route("/add_weight", methods=["POST"])
@login_required
def add_weight():
    weight = request.form["weight"]
    entry = Progress(weight=weight, user_id=current_user.id)
    db.session.add(entry)
    db.session.commit()
    return redirect("/dashboard")

# 🧾 TRACKER
@app.route("/tracker", methods=["GET","POST"])
@login_required
def tracker():
    if request.method == "POST":
        t = Tracker(
            diet_done=True if request.form.get("diet") else False,
            workout_done=True if request.form.get("workout") else False,
            water=int(request.form["water"]),
            user_id=current_user.id
        )
        db.session.add(t)
        db.session.commit()
    return render_template("tracker.html")

# 📄 STATIC PAGES
@app.route("/diet")
@login_required
def diet():
    return render_template("diet.html")

@app.route("/workout")
@login_required
def workout():
    return render_template("workout.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)