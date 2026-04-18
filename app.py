from flask import Flask, render_template, request, redirect
from config import Config
from models import db, User, Progress
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import date
from models import DailyTracker

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
@app.route("/tracker", methods=["GET", "POST"])
@login_required
def tracker():
    today = str(date.today())

    if request.method == "POST":
        diet = True if request.form.get("diet") else False
        workout = True if request.form.get("workout") else False
        water = int(request.form["water"])

        existing = DailyTracker.query.filter_by(user_id=current_user.id, date=today).first()

        if not existing:
            entry = DailyTracker(
                date=today,
                diet=diet,
                workout=workout,
                water=water,
                user_id=current_user.id
            )
            db.session.add(entry)

            # 🔥 STREAK LOGIC
            if diet and workout:
                current_user.streak += 1
            else:
                current_user.streak = 0

            db.session.commit()

    return render_template("tracker.html")

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
    latest = data[-1].weight if data else 0

    # 🧠 SMART FEEDBACK
    message = ""
    if len(data) >= 2:
        if data[-1].weight > data[-2].weight:
            message = "⚠️ You gained weight. Stay strict."
        else:
            message = "🔥 Good job! Keep going."

    return render_template("dashboard.html",
                           data=data,
                           latest=latest,
                           streak=current_user.streak,
                           message=message)
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