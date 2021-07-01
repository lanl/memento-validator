# Memento Validator
 TODO: Add description
 
## CLI Tool

## Web API

1. Install Dependencies

```shell
$ pip install -r requirements.txt
```

2. Export Flask Module (REMOVE)

```shell
$ export FLASK_APP=mementoweb/validator/web/server.py
```

3. Run Server (Add Port and config)

```shell
$ flask run
```

### Original
**[GET] /original**

| Parameter     |  Description | Example  |
|---            |---|---|
| uri           |   | https://arquivo.pt/wayback/20080215125110/http://www.facebook.com/ |
| datetime      |   | Sun, 01 Apr 2010 12:00:00 GMT  |

### Timegate

**[GET] /timegate**

### Timemap

**[GET] /timemap**

### Memento

**[GET] /memento**

## Web Front-end


## Package Installation (ADD)

## Documentation
Generate documentation
```shell
$ cd docs

$ make html
```

```shell
$ firefox build/html/index.html
```