This is a flask app.

To set up this project, you may set up a python virtual environment:
```
python -m venv <environment_name>
```
Then activate it:
```
# Linux command
source venv/bin/activate
# Windows command
.\venv\Scripts\activate
```

Now regardless if a python venv was used, you may install the dependencies. This code was developed using Python 3.12.1

```
pip install -r requirements.txt
```

After this, create your own .env file, there is a .env.example as a base for it, not that it has many secrets, only holding the Flask secret.

Then the app can be started by executing app.py
```
python app.py
```
