"""
Project Tasks that can be invoked using using the program "invoke" or "inv"
"""

import os
import glob
from invoke import task

# disable the check for unused-arguments to ignore unused ctx parameter in tasks
# pylint: disable=unused-argument

IS_WINDOWS = os.name == 'nt'
if IS_WINDOWS:
    # setting 'shell' is a work around for issue #345 of invoke
    RUN_ARGS = {'pty': False, 'shell': r'C:\Windows\System32\cmd.exe'}
else:
    RUN_ARGS = {'pty': True}


def get_files(is_list=False):
    """Get the files to run analysis on

    :param is_list: If True return a list else return a space separated string
    (Default value = False)

    """
    files = [
        'vup',
        'setup.py',
        'tasks.py',
    ]
    files.extend(glob.glob(os.path.join('tests', '*.py')))
    if is_list:
        return files
    files_string = ' '.join(files)
    return files_string


@task
def setup(ctx):
    """Install python requirements

    :param ctx: invoke context

    """
    ctx.run('python3 -m pip install -r requirements.txt', **RUN_ARGS)


@task
def clean(ctx):
    """Clean repository using git

    :param ctx: invoke context

    """
    ctx.run('git clean --interactive', **RUN_ARGS)


@task
def lint(ctx):
    """Run pylint on this module

    :param ctx: invoke context

    """
    cmds = ['pylint --output-format=parseable', 'flake8']
    base_cmd = 'python3 -m {cmd} {files}'

    for cmd in cmds:
        ctx.run(base_cmd.format(cmd=cmd, files=get_files()), **RUN_ARGS)


@task
def reformat(ctx):
    """Run formatting on this module

    :param ctx: invoke context

    """
    cmd = 'yapf --recursive --in-place'
    base_cmd = 'python3 -m {cmd} {files}'

    ctx.run(base_cmd.format(cmd=cmd, files=get_files()), **RUN_ARGS)


@task
def docstring(ctx):
    """Run formatting on this module

    :param ctx: invoke context

    """
    base_cmd = 'pyment -w {a_file}'

    for a_file in get_files(is_list=True):
        ctx.run(base_cmd.format(a_file=a_file, **RUN_ARGS))


@task
def metrics(ctx):
    """Run radon code metrics on this module

    :param ctx: invoke context

    """
    cmd = 'radon {metric} --min B {files}'
    metrics_to_run = ['cc', 'mi']
    for metric in metrics_to_run:
        ctx.run(cmd.format(metric=metric, files=get_files()), **RUN_ARGS)


@task
def test(ctx):
    """Test Task

    :param ctx: invoke context

    """
    # Use py.test instead of the recommended pytest so it works on Python 3.3
    cmd = 'py.test --cov-report term-missing --cov=vup --color=no'
    ctx.run(cmd, **RUN_ARGS)


# pylint: disable=redefined-builtin
@task(test, reformat, lint, metrics, default=True)
def all(ctx):
    """All tasks minus

    :param ctx: invoke context

    """


@task(clean)
def build(ctx):
    """Task to build an executable using pyinstaller

    :param ctx: invoke context

    """
    cmd = 'pyinstaller -n vup --onefile ' + os.path.join('vup', '__main__.py')
    ctx.run(cmd, **RUN_ARGS)
