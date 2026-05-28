from flask import Flask, render_template, request
from inference import generate_response

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    user_input = ""

    if request.method == "POST":
        user_input = request.form["question"]
        # Calls the function from inference.py
        response = generate_response(user_input)

    return render_template(
        "index.html",
        user_input=user_input,
        response=response
    )

if __name__ == "__main__":
    # Standard debug mode initialization
    app.run(debug=True)
