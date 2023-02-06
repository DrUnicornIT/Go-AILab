from flask import Flask
#we import waitress here. 
from waitress import serve


app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'> A very simple flask server !</h1>"

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    #We now use this syntax to server our app. 
    serve(app, host='120.0.0.0', port=5000)
