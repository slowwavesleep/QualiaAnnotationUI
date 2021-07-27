from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Annotation(db.Model):
    relation_id = db.Column(db.Integer, primary_key=True)
    approved = db.Column(db.Boolean, index=True)


class Record:
    pass


db.create_all()


@app.route("/")
def index():
    return render_template("annotate.html")


@app.route("/annotate/submit")
def submit():
    rel_id = request.args.get("id", None)
    annotation = request.args.get("a", None)

    return jsonify({"a": f"all good {rel_id} {annotation}"})


if __name__ == '__main__':
    app.run(debug=True)
