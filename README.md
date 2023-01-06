### Installation

#### Install requirements:
```python -m pip install -r requirements.txt```
#### Configure headers.json:
[https://ytmusicapi.readthedocs.io/en/stable/setup.html](https://ytmusicapi.readthedocs.io/en/stable/setup.html)
#### Configure endpoint api
Start:\
```gunicorn api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker```
#### Configure API_TOKEN and HOST vars in main.py
<br>
That's it.