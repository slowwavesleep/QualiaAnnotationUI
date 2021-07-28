import random

import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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

data = pd.read_csv("resources/qualia_relations.csv")
data.columns = ['record_id',
                'id_lu_1',
                'word_1',
                'pos_1',
                'fn_definition_1',
                'relation',
                'id_lu_2',
                'word_2',
                'pos_2',
                'fn_definition_2']


def load_from_df(df: pd.DataFrame, session, model):
    model.query.delete()
    records = []
    for row in df.iterrows():
        records.append(Record(**row[1].to_dict()))
    session.add_all(records)
    session.commit()


load_from_df(data, db.session, Record)


@app.route("/")
def index():
    annotated = set([annotation.record_id for annotation in Annotation.query.all()])
    ids_to_annotate = set([record.record_id for record in Record.query.all()])
    record_id = random.choice(list(ids_to_annotate.difference(annotated)))
    record = Record.query.filter(Record.record_id == record_id).first()
    return render_template("annotate.html", record=record)


@app.route("/annotate/submit")
def submit():
    record_id = request.args.get("id", None)
    approved = request.args.get("a", None)
    if approved == "ok":
        approved = True
    else:
        approved = False

    db.session.merge(Annotation(**{"record_id": record_id, "approved": approved}))
    db.session.commit()

    return jsonify({"a": f"all good {record_id} {approved}"})


if __name__ == '__main__':
    app.run(debug=True)
