# catalog-dash

Dash application to plot graphs related to INPE-CDSR project.


## Installation

### Requirements

Make sure you have the following libraries installed:

- [`Python 3`](https://www.python.org/)

Install [`pyenv`](https://github.com/pyenv/pyenv#basic-github-checkout) and [`pyenv-virtualenv`](https://github.com/pyenv/pyenv-virtualenv#installing-as-a-pyenv-plugin). After that, install Python 3.7.4 using pyenv:

```
$ pyenv install 3.7.4
```

Create a Python environment with the Python version above through pyenv-virtualenv:

```
$ pyenv virtualenv 3.7.4 catalog-dash
```

Activate the environment:

```
$ pyenv activate catalog-dash
```

Install the requirements:

```
$ pip install -r requirements.txt
```


## Run the application

Run the application:

```
$ pyenv activate catalog-dash
$ set -a && source catalog_dash.env && set +a
$ python main.py
```


### Running with docker

Build image:

```
$ docker build -t inpe-cdsr-catalog-dash -f docker/dev.Dockerfile . --no-cache
$ docker build -t registry.dpi.inpe.br/inpe-cdsr/catalog-dash:0.0.4 -f docker/prod.Dockerfile . --no-cache
```

Push image to registry:

```
$ docker push registry.dpi.inpe.br/inpe-cdsr/catalog-dash:0.0.4
```
