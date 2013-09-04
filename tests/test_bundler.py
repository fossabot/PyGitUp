# System imports
import os
import subprocess
from os.path import join

# 3rd party libs
from nose.plugins.skip import SkipTest
from git import *

# PyGitup imports
from tests import basepath, write_file, init_master

test_name = 'bundler'

repo_path = join(basepath, test_name + os.sep)


def setup():
    master_path, master = init_master(test_name)

    # Prepare master repo
    master.git.checkout(b=test_name)

    # Add Gemfile
    gemfile = join(master_path, 'Gemfile')
    write_file(gemfile, "source 'https://rubygems.org'\ngem 'colored'")
    master.index.add([gemfile])
    master.index.commit(test_name)

    # Clone to test repo
    path = join(basepath, test_name)

    master.clone(path, b=test_name)
    repo = Repo(path, odbt=GitCmdObjectDB)
    repo.git.config('git-up.bundler.check', 'true')

    assert repo.working_dir == path


def test_ahead_of_upstream():
    """ Run 'git up' with result: rebasing """
    def is_installed(prog):
        return subprocess.call([prog, '-v'], shell=True, stdout=None) == 0

    if not (is_installed('ruby') and is_installed('gem')):
        # Ruby not installed, skip test
        raise SkipTest('Ruby not installed, skipped Bundler integration test')

    os.chdir(repo_path)

    from PyGitUp.gitup import GitUp
    gitup = GitUp()
    gitup.run(testing=True)

