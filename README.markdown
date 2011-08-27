GameSoup
========

GameSoup is a two stage board game development environment written using Django.

Prerequisites
-------------

The project dependencies can be easily installed using standard Python distribution tools. If you're not already using these tools, please install them now:

* [pip](http://pypi.python.org/pypi/pip)
* [virtualenv](http://pypi.python.org/pypi/virtualenv)
* [virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/)

After installing these tools you might want to set some environment variables. Assuming Bash, put this into your .bashrc file:

```bash
# virtualenvwrapper
export WORKON_HOME=~/Envs
source /usr/local/bin/virtualenvwrapper.sh
export PIP_VIRTUALENV_BASE=$WORKON_HOME
export PIP_RESPECT_VIRTUALENV=true
```

Getting Started
---------------

Create a virtual environment for gamesoup:

```bash
mkvirtualenv gamesoup --no-site-packages
```

Clone the repo into the virtual environment:

```bash
workon gamesoup
cdvirtualenv
git clone git://github.com/ktonon/GameSoup.git
```

Install the project dependencies with pip:

```bash
cd GameSoup
pip install -r gamesoup/requirements.txt
```

Copy the `local_settings` example file:

```bash
cp gamesoup/local_settings.py.template gamesoup/local_settings.py
```

Create the database:

```bash
gamesoup/manage.py syncdb
```

Install sample data:

```bash
script/loaddata
```

Run the server:

```bash
gamesoup/manage.py runserver
```

If you want to see the *flow* charts of game objects, you will need to install [GraphViz](http://www.graphviz.org/Download.php).

### Playing

In your browser visit http://localhost:8000/admin and login using the account
you creating while preparing the database.

* To play a game of boggle visit
  http://localhost:8000/admin/matches/match/1/play/
* To see the guts of the boggle game visit
  http://localhost:8000/admin/games/game/1/assemble/
* To dig deeper and see what the guts themselves are made of visit
  http://localhost:8000/admin/library/
