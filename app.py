from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for sessions

# Dummy user for login
USERNAME = "admin"
PASSWORD = "password"

# FLAMES logic
def remove_common_letters(name1, name2):
    name1 = name1.lower().replace(" ", "")
    name2 = name2.lower().replace(" ", "")
    name1_list = list(name1)
    name2_list = list(name2)

    for letter in name1[:]:
        if letter in name2_list:
            name1_list.remove(letter)
            name2_list.remove(letter)

    return len(name1_list + name2_list)

def flames_result(count):
    flames = list("FLAMES")
    while len(flames) > 1:
        split_index = (count % len(flames)) - 1
        if split_index >= 0:
            right = flames[split_index + 1:]
            left = flames[:split_index]
            flames = right + left
        else:
            flames = flames[:len(flames) - 1]
    return flames[0]

def get_relationship(letter):
    return {
        "F": "Friends",
        "L": "Love",
        "A": "Affection",
        "M": "Marriage",
        "E": "Enemy",
        "S": "Siblings"
    }[letter]

# Routes
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/flames", methods=["GET", "POST"])
def index():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None
    if request.method == "POST":
        name1 = request.form["name1"]
        name2 = request.form["name2"]
        if name1 and name2:
            count = remove_common_letters(name1, name2)
            result_letter = flames_result(count)
            result = f"{name1} and {name2} are: {get_relationship(result_letter)}"
    return render_template("index.html", result=result)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
