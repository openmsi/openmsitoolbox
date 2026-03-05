"Tests for argument parsing utilities."
import os
import pathlib
import pytest
import logging
from openmsitoolbox.argument_parsing.parser_callbacks import (
    existing_file,
    existing_dir,
    create_dir,
    int_power_of_two,
    positive_int,
    logger_string_to_level,
)
from openmsitoolbox import OpenMSIArgumentParser
from config import TEST_CONST


def test_argument_parser(output_dir):
    parser = OpenMSIArgumentParser()
    parser.add_arguments(
        "filepath",
        "output_dir",
        "optional_output_dir",
        n_threads=5,
        update_seconds=60,
    )

    args = [
        os.fspath(TEST_CONST.TEST_DATA_FILE_PATH),
        os.fspath(output_dir / "TEST_OUTPUT"),
        "--output_dir",
        os.fspath(TEST_CONST.TEST_DATA_FILE_ROOT_DIR_PATH),
        "--n_threads",
        "100",
    ]

    parsed = parser.parse_args(args=args)
    assert parsed.n_threads == 100
    assert (output_dir / "TEST_OUTPUT").is_dir()

    with pytest.raises(ValueError):
        parser = OpenMSIArgumentParser()
        parser.add_arguments("never_name_a_command_line_arg_this")


def test_existing_file(tmp_path):
    this_file = pathlib.Path(__file__).resolve()
    assert existing_file(this_file) == this_file
    assert existing_file(str(this_file)) == this_file

    bad_path = tmp_path / "fake_file.fake"
    with pytest.raises(FileNotFoundError):
        existing_file(bad_path)
    with pytest.raises(FileNotFoundError):
        existing_file(str(bad_path))
    with pytest.raises(TypeError):
        existing_file(None)


def test_existing_dir(output_dir):
    """Test the existing_dir argument parser callback"""
    assert output_dir.is_dir()
    assert existing_dir(output_dir) == output_dir
    output_dir_str = str(output_dir)
    assert existing_dir(output_dir_str) == output_dir

    non_existent_dir = (output_dir / "never_make_a_directory_called_this").resolve()
    assert not non_existent_dir.is_dir()
    with pytest.raises(FileNotFoundError):
        existing_dir(non_existent_dir)
    with pytest.raises(FileNotFoundError):
        existing_dir(str(non_existent_dir))
    with pytest.raises(TypeError):
        existing_dir(None)


def test_create_dir(output_dir):
    """Test the create_dir argument parser callback"""
    assert output_dir.is_dir()
    assert create_dir(output_dir) == output_dir
    assert create_dir(str(output_dir)) == output_dir

    create_dir_path = (output_dir / "test_create_directory").resolve()
    assert not create_dir_path.is_dir()

    try:
        assert create_dir(create_dir_path) == create_dir_path
        assert create_dir_path.is_dir()
        create_dir_path.rmdir()
        assert not create_dir_path.is_dir()

        assert create_dir(str(create_dir_path)) == create_dir_path
        assert create_dir_path.is_dir()
    finally:
        if create_dir_path.is_dir():
            create_dir_path.rmdir()

    with pytest.raises(TypeError):
        existing_file(None)


def test_int_power_of_two():
    """Test the int_power_of_two argument parser callback"""
    assert int_power_of_two(524288) == 524288
    assert int_power_of_two(16384) == 16384
    assert int_power_of_two(4) == 4
    assert int_power_of_two("8") == 8
    assert int_power_of_two(16.0) == 16

    with pytest.raises(ValueError):
        int_power_of_two("hello : )")
    with pytest.raises(ValueError):
        int_power_of_two("-2")
    with pytest.raises(ValueError):
        int_power_of_two(-4)
    with pytest.raises(TypeError):
        int_power_of_two(None)


def test_positive_int():
    """Test the positive_int argument parser callback"""
    assert positive_int(3) == 3
    assert positive_int("5") == 5
    assert positive_int(22.0) == 22

    with pytest.raises(ValueError):
        positive_int("hello : )")
    with pytest.raises(ValueError):
        positive_int("-3")
    with pytest.raises(ValueError):
        positive_int(-5)
    with pytest.raises(TypeError):
        positive_int(None)


def test_logger_string_to_level():
    """Test the logger_string_to_level argument parser callback"""
    assert logger_string_to_level("notset") == logging.NOTSET
    assert logger_string_to_level("debug") == logging.DEBUG
    assert logger_string_to_level("info") == logging.INFO
    assert logger_string_to_level("warning") == logging.WARNING
    assert logger_string_to_level("error") == logging.ERROR
    assert logger_string_to_level("critical") == logging.CRITICAL
    assert logger_string_to_level("11") == 11

    with pytest.raises(ValueError):
        logger_string_to_level("-5")
