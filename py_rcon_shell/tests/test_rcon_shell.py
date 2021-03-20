import subprocess
from unittest.mock import patch

from cmd2 import CommandResult
from cmd2_ext_test import ExternalTestMixin
from dev_shell.tests.fixtures import CmdAppBaseTestCase

from py_rcon_shell.rcon_client import LazyRconClient
from py_rcon_shell.rcon_shell import PyRconShellCmd2App, get_app_kwargs


class PyRconShellCmd2AppTester(ExternalTestMixin, PyRconShellCmd2App):
    pass


class RconClientMock(LazyRconClient):
    def __init__(self):  # noqa
        self.calls = []

    def run(self, *args):
        self.calls.append(args)
        return f'Mock response for: {args!r}'

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def tearDown(self):
        self.calls = []


class BaseTestCase(CmdAppBaseTestCase):
    def get_app_instance(self):
        self.client_mock = RconClientMock()
        app = PyRconShellCmd2AppTester(**get_app_kwargs(rcon_client=self.client_mock))
        return app

    def tearDown(self):
        super().tearDown()
        self.client_mock.tearDown()


class PyRconShellTestCase(BaseTestCase):
    def test_help_raw(self):
        out = self.app.app_cmd('help')

        assert isinstance(out, CommandResult)
        assert 'Documented commands' in out.stdout

        assert 'Documented commands' in out.stdout

    def test_help_via_execute(self):
        stdout, stderr = self.execute('help')
        assert stderr == ''
        assert 'Documented commands' in stdout

    def test_do_pytest(self):
        with patch.object(subprocess, 'check_call') as check_call_mock:
            stdout, stderr = self.execute(command='pytest')

        assert stderr == ''
        check_call_mock.assert_called_once()
        popenargs = check_call_mock.call_args[0][0]
        command = popenargs[0]
        assert command.endswith('/.venv/bin/pytest')

        # The call will be printed:
        assert '.venv/bin/' in stdout
        assert 'pytest' in stdout

    def test_do_rcon(self):
        stdout, stderr = self.execute('rcon foo bar')
        assert stderr == ''
        assert "Send: \x1b[93mfoo bar\x1b[39m\n" in stdout
        assert "Mock response for: ('foo', 'bar')" in stdout
