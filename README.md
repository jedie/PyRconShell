# PyRconShell

Minecraft rcon shell in Python using:

* https://github.com/conqp/rcon
* https://github.com/jedie/dev-shell

Works on Linux, macOS and Windows. It requires Python 3.8 or higher.
Note on Debian based Linux the `python3-venv` package is needed.


## usage

Bootstrap and use PyRconShell, e.g.:

```bash
~$ git clone https://github.com/jedie/PyRconShell.git
~$ cd PyRconShell
~/PyRconShell$ ./rcon-shell.py

...

Developer shell - py_rcon_shell - v0.0.1

...

(py_rcon_shell) rcon list
Send: list
Response:
----------------------------------------------------------------------------------------------------
There are 3 of a max of 10 players online: Foo, Bar, JohnDoe
----------------------------------------------------------------------------------------------------

(py_rcon_shell) rcon op JohnDoe
Send: op JohnDoe
Response:
----------------------------------------------------------------------------------------------------
Made JohnDoe a server operator
----------------------------------------------------------------------------------------------------
```


## Activate rcon server

To enable rcon in your `server.properties` change this:
```
enable-rcon=true
rcon.port=25575
rcon.password=a-password-is-needed
```
Note a password must be set! A empty password will disable rcon!


Add these settings into: `~/.PyRconShell.ini`, e.g.:

```ini
[DEFAULT]
rcon_host = 127.0.0.1
rcon_port = 25575
rcon_password = a-password-is-needed
```


## hints

Check if rcon listen with e.g.:

```bash
$ lsof -i
```


## Links

* https://minecraft.gamepedia.com/Commands#List_and_summary_of_commands


## Project links

* Github: https://github.com/jedie/PyRconShell
* PyPi: https://pypi.org/project/rcon-shell/