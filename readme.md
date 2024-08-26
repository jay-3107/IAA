

## Running Project Locally
### Backend(api)
Clone repo and create a virtual environment
```
$ git clone https://github.com/python-engineer/IAA.git
$ cd api
$ python3 -m venv venv
$ . venv/bin/activate
```
Install dependencies
```
$ (venv) pip3 install Flask torch torchvision nltk
```
Install nltk package
```
$ (venv) python
>>> import nltk
>>> nltk.download('punkt')
```

Run
```
$ (venv) python model.py
```
### Frontend
```
$ npm install
$ npm run dev
```

