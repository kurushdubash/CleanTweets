from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('sign_in.html')

@app.route("/hello/")
def help_page(name=None):
	return render_template('hello_world.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)


## EXAMPLE ON USING ON-THE-FLY URLS
# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html', name=name)