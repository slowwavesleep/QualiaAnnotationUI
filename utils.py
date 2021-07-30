import pandas as pd


def load_from_df(df: pd.DataFrame, session, model):
    model.query.delete()
    records = []
    for row in df.iterrows():
        records.append(model(**row[1].to_dict()))
    session.add_all(records)
    session.commit()


def init_data(path, session, model):
    data = pd.read_csv(path)
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
    load_from_df(data, session, model)


def delete_all(models: list):
    for model in models:
        model.query.delete()
