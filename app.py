from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    # Simply show the form on GET request
    return render_template("index.html")

@app.route("/record", methods=["POST"])
def record():
    language = request.form.get('language')
    age = request.form.get('age')
    level = request.form.get('level')

    # Here you can add code to process the recording or other logic
    print(f"Language: {language}, Age: {age}, Level: {level}")

    # Redirect back to the main page or to another route after processing
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
