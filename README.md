# QualiaAnnotationUI
A flask-based prototype UI for annotation of qualia relations between FrameNet Lexical Units inferred from an external knowledge base

![image](https://user-images.githubusercontent.com/44175589/129951197-606d8a53-3db3-4f4e-b69c-e8758d9a8c62.png)


## How to install and run

Clone the repository `cd` to it.

```
git clone https://github.com/slowwavesleep/QualiaAnnotationUI.git
```

```
cd QualiaAnnotationUI
```
Create and activate a virtual environment for the project. I suggest using Anaconda.

```
conda env --n qualia python=3.7
```
```
conda activate qualia
```

Install the requirements.

```
pip install -r requirements.txt
```

Run the application.

```
flask run
```

## Annotating a different dataset

To annotate a different dataset replace `qualia_relations.csv` in `resources` directory with a new file.
Or alternatively, change `data_path` in config.yml to point to the new file. In both cases the file must in CSV format (comma-separated specifically)
with the following columns:
- `index`
- `id_lu_1`
- `word_1`
- `pos_1`
- `fnDefinition_1`
- `relation`
- `id_lu_2`
- `word_2`
- `pos_2`

## Data persistence

The tool uses SQLite to persist user annotations between the launches. Made annotations may be downloaded in CSV format.
