from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "secret123"

@app.route("/", methods=["GET", "POST"])
def index():
    if "number" not in session:
        session["number"] = random.randint(1, 100)
        session["chances"] = 10
        session["message"] = "Start guessing!"

    if request.method == "POST":
        try:
            guess = int(request.form["guess"])
        except:
            session["message"] = "Enter a valid number!"
            return render_template("index.html",
                                   message=session["message"],
                                   chances=session["chances"])

        number = session["number"]

        if guess > number:
            session["message"] = "Too high!"
        elif guess < number:
            session["message"] = "Too low!"
        else:
            session["message"] = "🎉 You win!"
            session.clear()
            return render_template("index.html", message="🎉 You win!", chances=0)

        session["chances"] -= 1

        if session["chances"] == 0:
            msg = f"Game Over! Number was {number}"
            session.clear()
            return render_template("index.html", message=msg, chances=0)

    return render_template("index.html",
                           message=session.get("message"),
                           chances=session.get("chances"))

if __name__ == "__main__":
    app.run(debug=True)