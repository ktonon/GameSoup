GameSoup
========

GameSoup is a two stage board game development environment.

It is a Django website.

It is a dead project, but I plan on documenting it well enough to

* explain its goals
* describe how to install it
* describe how to build the game of boggle

Until then, feel free to tinker with it.

Take care,

Kevin

Getting Started
---------------

In the following example, only enter what you see following the `$`. All other
text is example output that results from the commands you enter.

First clone the repo and then `cd` to the root directory of your copy. From the
command line

```bash
$ pwd
```

Remember what you see. Now,

```bash
$ cd server/gamesoup
$ cp localsettings_example.py localsettings.py
```

and edit `localsettings.py`, following the instructions. For the `PROJECT_ROOT`
setting you will replace `/path/to` with whatever you saw when you ran `pwd`.

### Preparing the Database

The default local settings configuration uses SQLite, so you will need to
install SQlite3 and also python bindings for SQLite3. Once you have done that,
do a migration. `cd` to the `PROJECT_ROOT/server` directory and run,

```bash
$ python gamesoup/manage.py syncdb
Creating table django_admin_log
Creating table auth_permission
Creating table auth_group_permissions
...

Would you like to create one now? (yes/no): yes
Username (Leave blank to use 'kevin'): 
E-mail address: your@email.com
Password: 
Password (again): 
Superuser created successfully.
Installing index for admin.LogEntry model
...
```

At this point the database will be empty except for the user account you just
created. To populate it with some example data,

```bash
$ script/loaddata
Loading dev user data
Loading dev library data
Loading dev games data
Loading dev matches data
```

Now you enough components in your gamesoup installation to play a game of
boggle.

### Running the Server

From the `PROJECT_ROOT/server` directory run,

```bash
python gamesoup/manage.py runserver
```

### Playing

In your browser visit http://localhost:8000/admin and login using the account
you creating while preparing the database.

* To play a game of boggle visit
  http://localhost:8000/admin/matches/match/1/play/
* To see the guts of the boggle game visit
  http://localhost:8000/admin/games/game/1/assemble/
* To dig deeper and see what the guts themselves are made of visit
  http://localhost:8000/admin/library/
