from taskw.warrior import TaskWarrior


def test_task_data_is_empty(taskwarrior):
    """
    Just a sanity check to make sure that after the setup, the list of
    tasks is empty, otherwise we are probably using the current user's
    TASKDATA and we should not continue.
    """
    assert taskwarrior.load_tasks() == {'completed': [], 'pending': []}


def test_add_task_foobar(taskwarrior):
    """
    Add a task with description 'foobar' and checks that the task is
    indeed created.
    """
    taskwarrior.task_add("foobar")
    tasks = taskwarrior.load_tasks()
    assert len(tasks['pending']) == 1
    assert tasks['pending'][0]['description'] == 'foobar'


def test_add_task_null_char(taskwarrior):
    """
    Try adding a task where the description contains a NULL character
    (0x00). This should not fail but instead simply add a task with the
    same description minus the NULL character.
    """
    taskwarrior.task_add("foo\x00bar")
    tasks = taskwarrior.load_tasks()
    assert len(tasks['pending']) == 1
    assert tasks['pending'][0]['description'] == 'foobar'


def test_load_config(default_taskrc_path):
    config = TaskWarrior.load_config(default_taskrc_path)
    assert config == {
        'data': {
            'location': '~/.task'
        },
        'alpha': {
            'one': 'yes',
            'two': '2',
        },
        'beta': {
            'one': 'FALSE',
        },
        'gamma': {
            'one': 'TRUE',
        },
        'uda': {
            'a': {
                'type': 'numeric',
                'label': 'Alpha',
            },
            'b': {
                'type': 'string',
                'label': 'Beta',
                'values': 'Strontium-90,Hydrogen-3',
            }
        }
    }
