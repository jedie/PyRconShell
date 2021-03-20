import sys
from pathlib import Path

import cmd2
from cmd2 import CommandSet
from dev_shell.base_cmd2_app import DevShellBaseApp
from dev_shell.command_sets.dev_shell_commands import DevShellCommandSet as OriginDevShellCommandSet
from dev_shell.command_sets.dev_shell_commands import run_linters
from dev_shell.config import DevShellConfig
from dev_shell.utils.colorful import blue, bright_blue, bright_yellow
from dev_shell.utils.subprocess_utils import verbose_check_call
from poetry_publish.publish import poetry_publish

import py_rcon_shell
from py_rcon_shell.rcon_client import LazyRconClient


PACKAGE_ROOT = Path(py_rcon_shell.__file__).parent.parent


@cmd2.with_default_category('PyRcon shell commands')
class RconShellCommandSet(CommandSet):
    def __init__(self, rcon_client: LazyRconClient):
        super().__init__()
        self.rcon_client = rcon_client

    def do_rcon(self, statement: cmd2.Statement):
        """
        Send command to rcon
        """
        print(f'Send: {bright_yellow(statement.args)}')
        response = self.rcon_client.run(*statement.arg_list)
        print(bright_blue('Response:'))
        print('-' * 100)
        print(blue(response))
        print('-' * 100)


class PyRconShellCmd2App(DevShellBaseApp):
    pass


class DevShellCommandSet(OriginDevShellCommandSet):
    def do_publish(self, statement: cmd2.Statement):
        # don't publish if test fails:
        verbose_check_call('pytest', '-x')

        poetry_publish(
            package_root=PACKAGE_ROOT,
            version=py_rcon_shell.__version__,
        )


def get_app_kwargs(rcon_client: LazyRconClient):
    """
    Generate the kwargs for the cmd2 App.
    (Separated because we needs the same kwargs in tests)
    """
    config = DevShellConfig(package_module=py_rcon_shell)

    app_kwargs = dict(
        config=config,
        command_sets=[
            RconShellCommandSet(rcon_client=rcon_client),
            DevShellCommandSet(config=config),
        ]
    )
    return app_kwargs


def rcon_shell_cmdloop():
    """
    Entry point to start the "dev-shell" cmd2 app.
    Used in: [tool.poetry.scripts]
    """
    with LazyRconClient() as rcon_client:
        c = PyRconShellCmd2App(**get_app_kwargs(rcon_client))
        sys.exit(c.cmdloop())
