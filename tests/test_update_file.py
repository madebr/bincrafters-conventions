#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters_conventions.bincrafters_conventions import Command

import tempfile
from shutil import copyfile


def _prepare_old_file(file_name: str, suffix: str, old=None, expected=None):
    if old is None:
        old = file_name + "_old"

    if expected is None:
        expected = file_name + "_expected"

    _, path_old = tempfile.mkstemp(prefix=old, suffix=suffix)
    copyfile("files/{}{}".format(old, suffix), path_old)

    _, expected_path = tempfile.mkstemp(prefix=expected, suffix=suffix)
    copyfile("files/{}{}".format(expected, suffix), expected_path)

    return path_old, expected_path


def _compare_file(path_old: str, expected_path: str):
    """ This is needed to ignore different line endings styles
        e.g. filecmp.cmp would throw an error with differnt line ending
    """
    l1 = l2 = True
    with open(path_old, 'r') as f1, open(expected_path, 'r') as f2:
        while l1 and l2:
            l1 = f1.readline()
            l2 = f2.readline()
            if l1 != l2:
                return False
    return True


def test_updated_conanfile():
    """ Try to update an already up-to-date file, nothing should change
    """

    path_old, path_expected = _prepare_old_file("conan_1", ".py", old="conan_1_expected")

    args = ['--conanfile', path_old]
    command = Command()
    command.run(args)

    assert _compare_file(path_old, path_expected)


def test_conanfile_default_options():
    """ Try to update an conanfile which has old styled default options
    """

    path_old, path_expected = _prepare_old_file("conan_1", ".py")

    args = ['--conanfile', path_old]
    command = Command()
    command.run(args)

    assert _compare_file(path_old, path_expected)


def test_conanfile_default_options_mutiline():
    """ Try to update an conanfile which has old styled multiline default options
    """

    path_old, path_expected = _prepare_old_file("conan_multiline_options", ".py", expected="conan_1_expected")

    args = ['--conanfile', path_old]
    command = Command()
    command.run(args)

    assert _compare_file(path_old, path_expected)


def test_appveyor_update_up_to_date():
    """ Try to update an up-to-date AppVeyor file
    """

    path_old, path_expected = _prepare_old_file("appveyor_1", ".yml", old="appveyor_1_expected")

    args = ['--appveyorfile', path_old]
    command = Command()
    command.run(args)

    assert _compare_file(path_old, path_expected)


def test_appveyor_update():
    """ Try to update an AppVeyor file
    """

    path_old, path_expected = _prepare_old_file("appveyor_1", ".yml")

    args = ['--appveyorfile', path_old]
    command = Command()
    command.run(args)

    assert _compare_file(path_old, path_expected)


def test_appveyor_update_new_compiler_jobs():
    """ Try to update an AppVeyor file, new compiler jobs should be added
    """

    path_old, path_expected = _prepare_old_file("appveyor_2", ".yml")

    args = ['--appveyorfile', path_old]
    command = Command()
    command.run(args)

    assert _compare_file(path_old, path_expected)


def test_update_travis_file():
    """ Create a standard travis file and update it.
    """

    path_old, path_expected = _prepare_old_file("travis_1", ".yml")

    args = ['--travisfile', path_old]
    command = Command()
    command.run(args)

    assert _compare_file(path_old, path_expected)


def test_update_travis_file_macos_images():
    """ Travis file with old macOS images
    """

    path_old, path_expected = _prepare_old_file("travis_1", ".yml", old="travis_1_old_macos_images")

    args = ['--travisfile', path_old]
    command = Command()
    command.run(args)

    assert _compare_file(path_old, path_expected)


def test_update_travis_file_with_global():
    """ Create a standard travis file and update it.
    """

    path_old, path_expected = _prepare_old_file("travis_with_globals", ".yml")

    args = ['--travisfile', path_old]
    command = Command()
    command.run(args)

    assert _compare_file(path_old, path_expected)


def test_travis_update_url():
    """ Create a README.md file and update it.
    """

    path_old, path_expected = _prepare_old_file("readme_1", ".md")

    args = ['--readme', path_old]
    command = Command()
    command.run(args)

    assert _compare_file(path_old, path_expected)
