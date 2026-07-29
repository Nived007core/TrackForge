from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key= "devtrack_secret_key"

# ---------------- MYSQL CONNECTION ----------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="icflix123",
    database="internship_db"
)

cursor = db.cursor()

print("✅ Connected to MySQL successfully!")

# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("loginpage.html")


# ---------------- REGISTER PAGE ----------------
@app.route("/register")
def register():
    return render_template("register.html")
# ------------------PROFILE PAGE-----------------
@app.route("/profile")
def profile():
    user_id = session["user_id"]
    cursor.execute(
        """SELECT *
        FROM users
        JOIN profile
        ON users.id=profile.user_id
        WHERE users.id=%s""",
        (user_id,)
    )
    user = cursor.fetchone()
    print(user)
    user_data ={
        "id":user[0],
        "firstname":user[1],
        "lastname":user[2],
        "username":user[3],
        "dob":user[7],
        "blood_group":user[8],
        "nationality":user[9],
        "language":user[10]
    }
    return render_template("profile.html", user=user_data)

# -----PROFILE UPDATE-------

@app.route("/update_profile",methods=["POST"])
def update_profile():
    firstname=request.form["firstname"]
    lastname=request.form["lastname"]
    dob = request.form["dob"]
    blood_group = request.form["blood_group"]
    nationality = request.form["nationality"]
    language = request.form["language"]
    user_id=session["user_id"]

    # ____update user table____

    query ="""UPDATE users SET firstname=%s, lastname=%s where id=%s"""
    values=(firstname,lastname,user_id)
    cursor.execute(query,values)

    # ------Update profile table------

    profile_query="""
    UPDATE profile
    SET dob=%s,
    blood_group=%s,
    nationality=%s,
    language=%s
    WHERE user_id=%s
    """
    profile_values=(
        dob,
        blood_group,
        nationality,
        language,
        user_id
    )
    cursor.execute(profile_query,profile_values)
    db.commit()
    return redirect("/profile")

# ---------------- SAVE USER ----------------
@app.route("/save_user", methods=["POST"])
def save_user():

    # Get form data
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    username = request.form["username"]
    password = request.form["password"]
    confirm_password = request.form["confirm_password"]

    # Check if passwords match
    if password != confirm_password:
        return "❌ Passwords do not match"

    # Check if username already exists
    cursor.execute(
        "SELECT * FROM users WHERE username = %s",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        return render_template("register.html",error="Username already exists")

    # Insert new user
    query = """
    INSERT INTO users(firstname, lastname, username, password)
    VALUES (%s, %s, %s, %s)
    """

    values = (firstname, lastname, username, password)

    cursor.execute(query, values)
    user_id = cursor.lastrowid
    cursor.execute("INSERT INTO profile(user_id) VALUES (%s)",(user_id,))
    db.commit()

    return redirect("/")


# ---------------- LOGIN ----------------
@app.route("/check_login", methods=["POST"])
def check_login():
    username = request.form["username"]
    password = request.form["password"]

    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )

    user = cursor.fetchone()

    if user:
        session["user_id"]= user[0]
        user_data = {
            "id": user[0],
            "firstname": user[1],
            "lastname": user[2],
            "username": user[3],
        }

        return render_template("dashboard.html", user=user_data)
    return "<h2>❌ Invalid Username or Password</h2>"


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    return redirect("/")

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)