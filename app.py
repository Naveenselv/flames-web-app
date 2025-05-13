from flask import Flask, render_template, request

app = Flask(__name__)

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
def index():
    result = None
    if request.method == "POST":
        name1 = request.form["name1"]
        name2 = request.form["name2"]
        if name1 and name2:
            count = remove_common_letters(name1, name2)
            result_letter = flames_result(count)
            result = f"{name1} and {name2} are: {get_relationship(result_letter)}"
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
