from flask import abort, Flask, jsonify, request
import json

app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return 'Hello from Martin!'


# Typical 404 error in json when page doesn't exist
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404


# For the UI
@app.route("/alphabet-checker", methods=['GET', 'POST'])
def alphabet_checker():
    if request.method == 'POST':
        form_input = request.form.get('input')
        result_json = has_all_alphabets(form_input)
        result = json.loads(result_json)["result"]

        return '''<h1>The input value is: {}</h1>
                  <h1>The result is: {}</h1>'''.format(form_input, result)

    return '''<form method="POST">
                  Input: <input type="text" name="input"
                  placeholder="Enter your input">
                  <br><input type="submit" value="Submit"><br>
              </form>'''


# For Restful api
# Get the input from the url and call the checker
@app.route("/api/alphabet-checker", methods=['GET', 'POST'])
def alphabet_checker_api():
    input = request.args.get('input')
    return has_all_alphabets(input)


# To check if an input contain every letter in the alphabet
def has_all_alphabets(input: str):
    if input is None:
        abort(400, description="Input cannot be None")

    elif len(input) < 26:
        result = False

    else:
        # put any alphabet into a set in upper case
        # then make sure the size of the set is 26,
        # the total number of alphabet letters
        result = len(set([x.upper() for x in input if x.isalpha()])) == 26

    return json.dumps({"input": input, "result": result})
