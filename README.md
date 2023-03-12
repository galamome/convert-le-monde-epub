# convert-le-monde-epub

## Créer un virtualEnv

## Create a new virtualenv named "convertlemonde"

### Python 3.3+

```python
python3 -m venv venv
```

### Activate the virtualenv (OS X & Linux)

```
source project_env/bin/activate
```

### Geler la configuration

```
pip freeze > requirements.txt
```

### Charger une configuration existente

```
pip install -r requirements.txt
```

pandoc -f html -t epub3 --epub-metadata=metadata.xml -o output.epub input.html


pandoc -f html -t epub2 -o output.epub Modif_juste_contenu_no_comment.html

## Call pandoc via Python

https://janakiev.com/blog/python-shell-commands/