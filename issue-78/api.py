from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/")
def result_display():

    with open("results.txt", "r") as result:
        return result.readlines()


if __name__ == "__main__":
    app.run(debug=True, port=8000)
