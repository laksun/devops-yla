from flask import Flask, render_template, request, redirect, url_for

# Initialize the Flask app
app = Flask(__name__)


# Define a route for the home page
@app.route("/")
def home():
    return render_template("index.html")


# Define a route that handles form submission (e.g., user inputs)
@app.route("/submit", methods=["POST"])
def submit():
    # Get the form data (input field name is 'username')
    username = request.form.get("username")

    # Simple logic based on user input
    if username:
        return f"Hello, {username}!"
    else:
        return "Please provide a username."


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
