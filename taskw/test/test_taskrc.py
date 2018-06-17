from taskw.fields import NumericField, ChoiceField
from taskw.taskrc import TaskRc


def test_taskrc_parsing(default_taskrc_path):
    assert TaskRc(default_taskrc_path) == {
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


def test_taskrc_overrides(default_taskrc_path):
    overrides = {
        'uda': {
            'd': {
                'type': 'string',
                'label': 'Delta',
            }
        },
        'alpha': {
            'two': '3',
        }
    }
    taskrc = TaskRc(default_taskrc_path, overrides=overrides)
    assert taskrc == {
        'data': {
            'location': '~/.task'
        },
        'alpha': {
            'one': 'yes',
            'two': '3',
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
            },
            'd': {
                'type': 'string',
                'label': 'Delta',
            }
        }
    }


def test_get_udas(default_taskrc_path):
    expected_udas = {
        'a': NumericField(label='Alpha'),
        'b': ChoiceField(
            label='Beta',
            choices=['Strontium-90', 'Hydrogen-3'],
        ),
    }
    actual_udas = TaskRc(default_taskrc_path).get_udas()
    assert actual_udas == expected_udas
