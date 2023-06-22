
# Gestion d'un virtualEnv Python

## Créer un virtualEnv

### Python 3.3+

```python
python3 -m venv venv
```

### Activate the virtualenv (OS X & Linux)

```
source venv/bin/activate
```

### Charger une configuration existante

```
pip install -r requirements.txt
```

### **Pour le développeur** Geler la configuration

```
pip freeze > requirements.txt
```
