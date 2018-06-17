import tempfile
import os
import shutil

import pytest

from taskw.warrior import TaskWarrior


@pytest.fixture
def default_taskrc_path():
    """ Path to default taskrc resource """
    path_to_default_taskrc = os.path.join(
        os.path.dirname(__file__),
        'data/default.taskrc'
    )
    yield path_to_default_taskrc


@pytest.fixture
def empty_taskrc_path():
    """ Path to empty taskrc resource """
    path_to_empty_taskrc = os.path.join(
        os.path.dirname(__file__),
        'data/empty.taskrc'
    )
    yield path_to_empty_taskrc


@pytest.fixture
def taskwarrior(empty_taskrc_path):
    """ TaskWarrior instance that uses empty.taskrc"""
    taskdata = tempfile.mkdtemp()
    tw = TaskWarrior(
        config_filename=empty_taskrc_path,
        config_overrides={'data.location': taskdata}
    )
    yield tw
    shutil.rmtree(taskdata)
