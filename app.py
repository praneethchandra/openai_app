from flask import Flask, render_template
# import connexion
import config
from models import Person

# app = Flask(__name__)

# app = connexion.App(__name__, specification_dir="./")
app = config.connex_app
# app.add_api("swagger.yml")
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    # return render_template("home.html")
    people = Person.query.all()
    return render_template("home.html", people=people)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)