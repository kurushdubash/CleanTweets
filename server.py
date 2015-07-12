from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/help/")
def help_page(name=None):
	return render_template('help.html', name=name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)


## EXAMPLE ON USING ON-THE-FLY URLS
# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)