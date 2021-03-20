import configparser
from pathlib import Path

from rcon import Client

from py_rcon_shell.constants import PY_RCON_SHELL_INI


INI_FILE_PATH = Path(PY_RCON_SHELL_INI).expanduser()


class LazyRconClient:
    def __init__(self):
        config = configparser.ConfigParser()
        if INI_FILE_PATH.is_file():
            print('Read config from:', INI_FILE_PATH)
            config.read(INI_FILE_PATH)
        else:
            config['DEFAULT'] = {
                'rcon_host': '127.0.0.1',
                'rcon_port': '25575',
                'rcon_password': '',
            }
            with INI_FILE_PATH.open('w') as configfile:
                config.write(configfile)
            print(f'Create "{INI_FILE_PATH}" with defaults. Please check settings!!!')

        self.rcon_host = config.get('DEFAULT', 'rcon_host')
        self.rcon_port = int(config.get('DEFAULT', 'rcon_port'))
        self.rcon_password = config.get('DEFAULT', 'rcon_password')

        self.client = None

    def __enter__(self):
        return self

    def run(self, *args):
        if self.client is None:
            self.client = Client(
                self.rcon_host,
                self.rcon_port,
                passwd=self.rcon_password
            ).__enter__()
        return self.client.run(*args)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client is not None:
            self.client.__exit__(exc_type, exc_val, exc_tb)
