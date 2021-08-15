import random

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from yaml import safe_load

from utils import init_data, delete_all

with open("config.yml") as file:
    config = safe_load(file)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config["db_path"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config["track_modifications"]
db = SQLAlchemy(app)


class LaunchedFlag(db.Model):
    flag_id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.Boolean, unique=True)


class Annotation(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    approved = db.Column(db.Boolean, index=True)


class Record(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    id_lu_1 = db.Column(db.Integer)
    word_1 = db.Column(db.String(32))
    pos_1 = db.Column(db.String(16))
    fn_definition_1 = db.Column(db.String(256))
    relation = db.Column(db.String(64))
    id_lu_2 = db.Column(db.Integer)
    word_2 = db.Column(db.String(32))
    pos_2 = db.Column(db.String(16))
    fn_definition_2 = db.Column(db.String(256))


db.create_all()


def set_launched_flag():
    db.session.add(LaunchedFlag(**{"flag_id": 0, "flag": True}))
    db.session.commit()


def reload_data():
    delete_all([Record, Annotation, LaunchedFlag])
    init_data(config["data_path"], db.session, Record)


first_launch = LaunchedFlag.query.first() is None


if first_launch:
    reload_data()
    set_launched_flag()


@app.route("/")
def index():
    return "WIP"


@app.route("/annotations")
def view_annotations():
    annotations = Annotation.query\
        .join(Record, Annotation.record_id == Record.record_id)\
        .add_columns(Record.record_id,
                     Record.word_1,
                     Record.fn_definition_1,
                     Record.relation,
                     Record.word_2,
                     Record.fn_definition_2,
                     Annotation.approved)
    return render_template("view_annotations.html", annotations=annotations)


@app.route("/data")
def view_data():
    records = Record.query
    return render_template("view_records.html", records=records)


@app.route("/annotations/export")
def export():
    return "WIP"


@app.route("/data/reset")
def reset():
    return "WIP"


@app.route("/annotate")
def annotate():
    annotated = set([annotation.record_id for annotation in Annotation.query.all()])
    ids_to_annotate = set([record.record_id for record in Record.query.all()])
    record_id = random.choice(list(ids_to_annotate.difference(annotated)))
    record = Record.query.filter(Record.record_id == record_id).first()
    return render_template("annotate.html", record=record)


@app.route("/annotate/submit")
def submit():
    record_id = request.args.get("id", None)
    approved = request.args.get("a", None)
    if not record_id or not approved:
        return jsonify({
            "data": {
                "result": f"Incorrect input",
                "status": "reject"
            }
        })
    else:
        if approved == "ok":
            approved = True
        elif approved == "wrong":
            approved = False
        else:
            return jsonify({
                "data": {
                    "result": f"No option selected",
                    "status": "reject"
                }
            })

        db.session.merge(Annotation(**{"record_id": record_id, "approved": approved}))
        db.session.commit()

        return jsonify({
            "data": {
                "result": f"Annotation for record `{record_id}` stored successfully",
                "status": "ok"
            }
        })


if __name__ == '__main__':
    app.run(debug=True)
