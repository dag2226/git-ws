# Copyright 2022 c0fec0de
#
# This file is part of Git Workspace.
#
# Git Workspace is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# Git Workspace is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with Git Workspace. If not, see <https://www.gnu.org/licenses/>.

"""Test Utilities."""
import contextlib
import logging
import os
import re
import shutil
import subprocess

# pylint: disable=unused-import
from subprocess import run  # noqa

from click.testing import CliRunner

from gitws._cli import main


@contextlib.contextmanager
def chdir(path):
    """Change Working Directory to `path`."""
    curdir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(curdir)


def get_sha(path):
    """Get SHA for `path`."""
    assert (path / ".git").exists()
    result = run(("git", "rev-parse", "HEAD"), capture_output=True, check=True, cwd=path)
    return result.stdout.decode("utf-8").strip()


def format_output(result, tmp_path=None):
    """Format Command Output."""
    lines = result.output.split("\n")
    if tmp_path:
        lines = [replace_tmp_path(line, tmp_path) for line in lines]
    return lines


def format_logs(caplog, tmp_path=None):
    """Format Logs."""
    lines = [f"{record.levelname:7s} {record.name} {record.message}" for record in caplog.records]
    if tmp_path:  # pragma: no cover
        lines = [replace_tmp_path(line, tmp_path) for line in lines]
    return lines


def replace_tmp_path(text, tmp_path):
    """Replace `tmp_path` in `text`."""
    tmp_path_esc = re.escape(str(tmp_path))
    sep_esc = re.escape(os.path.sep)
    regex = re.compile(rf"{tmp_path_esc}([A-Za-z0-9_{sep_esc}]*)")

    def repl(mat):
        sub = mat.group(1) or ""
        sub = sub.replace(os.path.sep, "/")
        return f"TMP{sub}"

    return regex.sub(repl, text)


def cli(command, exit_code=0, tmp_path=None):
    """Invoke CLI."""
    result = CliRunner().invoke(main, command)
    output = format_output(result, tmp_path=tmp_path)
    assert result.exit_code == exit_code, (result.exit_code, output)
    return output


def check(workspace, name, content=None, exists=True):
    """Check."""
    file_path = workspace / name / "data.txt"
    content = content or name
    if exists:
        assert file_path.exists()
        assert file_path.read_text() == f"{content}"
    else:
        assert not file_path.exists()


# Just set in the shell `export LEARN=1`

LEARN = bool(int(os.environ.get("LEARN") or 0))


def assert_gen(genpath, refpath, capsys=None, caplog=None, tmp_path=None):  # pragma: no cover
    """Compare Generated Files Versus Reference."""
    genpath.mkdir(parents=True, exist_ok=True)
    refpath.mkdir(parents=True, exist_ok=True)
    if capsys:
        captured = capsys.readouterr()
        out = captured.out
        err = captured.err
        if tmp_path:
            out = replace_tmp_path(out, tmp_path)
            err = replace_tmp_path(err, tmp_path)
        (genpath / "stdout.txt").write_text(out)
        (genpath / "stderr.txt").write_text(err)
    if caplog:
        with open(genpath / "logging.txt", "wt", encoding="utf-8") as file:
            for item in format_logs(caplog, tmp_path=tmp_path):
                file.write(f"{item}\n")
    if LEARN:
        logging.getLogger(__name__).warning("LEARNING %s", refpath)
        shutil.rmtree(refpath, ignore_errors=True)
        shutil.copytree(genpath, refpath)
    cmd = ["diff", "-r", "--exclude", "__pycache__", str(refpath), str(genpath)]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as error:
        assert False, error.stdout.decode("utf-8")


def assert_any(gen, refs):
    """Check if one of the refs fits."""
    for ref in refs:
        if gen == ref:
            assert True
            break
    else:
        # complain enriched
        assert gen == refs[0], gen
