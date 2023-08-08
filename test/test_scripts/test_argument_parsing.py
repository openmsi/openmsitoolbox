" Testing the argument_parsing functions and classes "

# imports
import pathlib
import os
import logging
from openmsitoolbox.testing import TestWithOutputLocation
from openmsitoolbox.argument_parsing.parser_callbacks import (
    existing_file,
    existing_dir,
    create_dir,
    int_power_of_two,
    positive_int,
    logger_string_to_level,
)
from openmsitoolbox import OpenMSIArgumentParser
from config import TEST_CONST  # pylint: disable=import-error,wrong-import-order

class TestArgumentParsing(TestWithOutputLocation):
    """
    Class for testing functions in utilities/argument_parsing.py
    """

    def test_argument_parser(self):
        """
        Test OpenMSIArgumentParser by just adding a bunch of arguments
        """
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
            os.fspath(self.output_dir / "TEST_OUTPUT"),
            "--output_dir",
            os.fspath(TEST_CONST.TEST_DATA_FILE_ROOT_DIR_PATH),
            "--n_threads",
            "100",
        ]
        args = parser.parse_args(args=args)
        self.assertEqual(args.n_threads, 100)
        self.assertTrue((self.output_dir / "TEST_OUTPUT").is_dir())
        with self.assertRaises(ValueError):
            parser = OpenMSIArgumentParser()
            parser.add_arguments("never_name_a_command_line_arg_this")
        self.success = True  # pylint: disable=attribute-defined-outside-init

    def test_existing_file(self):
        """
        Test the existing_file argument parser callback
        """
        this_file_path = pathlib.Path(__file__).resolve()
        self.assertTrue(this_file_path.is_file())
        self.assertEqual(existing_file(this_file_path), this_file_path)
        this_file_path_str = str(this_file_path)
        self.assertEqual(existing_file(this_file_path_str), this_file_path)
        does_not_exist_file_path = (
            self.output_dir
            / "never_make_a_directory_called_this"
            / "nor_a_file_called_this.fake_file_ext"
        )
        does_not_exist_file_path = does_not_exist_file_path.resolve()
        self.assertFalse(does_not_exist_file_path.is_file())
        with self.assertRaises(FileNotFoundError):
            _ = existing_file(does_not_exist_file_path)
        does_not_exist_file_path_str = str(does_not_exist_file_path)
        with self.assertRaises(FileNotFoundError):
            _ = existing_file(does_not_exist_file_path_str)
        with self.assertRaises(TypeError):
            _ = existing_file(None)
        self.success = True  # pylint: disable=attribute-defined-outside-init

    def test_existing_dir(self):
        """
        Test the existing_dir argument parser callback
        """
        self.assertTrue(self.output_dir.is_dir())
        self.assertEqual(existing_dir(self.output_dir), self.output_dir)
        output_dir_path_str = str(self.output_dir)
        self.assertEqual(existing_dir(output_dir_path_str), self.output_dir)
        does_not_exist_dir_path = (
            self.output_dir / "never_make_a_directory_called_this"
        ).resolve()
        self.assertFalse(does_not_exist_dir_path.is_dir())
        with self.assertRaises(FileNotFoundError):
            _ = existing_dir(does_not_exist_dir_path)
        does_not_exist_dir_path_str = str(does_not_exist_dir_path)
        with self.assertRaises(FileNotFoundError):
            _ = existing_dir(does_not_exist_dir_path_str)
        with self.assertRaises(TypeError):
            _ = existing_dir(None)
        self.success = True  # pylint: disable=attribute-defined-outside-init

    def test_create_dir(self):
        """
        Test the create_dir argument parser callback
        """
        self.assertTrue(self.output_dir.is_dir())
        self.assertEqual(create_dir(self.output_dir), self.output_dir)
        this_file_dir_path_str = str(self.output_dir)
        self.assertEqual(create_dir(this_file_dir_path_str), self.output_dir)
        self.assertTrue(self.output_dir.is_dir())
        create_dir_path = (self.output_dir / "test_create_directory").resolve()
        self.assertFalse(create_dir_path.is_dir())
        try:
            self.assertEqual(create_dir(create_dir_path), create_dir_path)
            self.assertTrue(create_dir_path.is_dir())
            create_dir_path.rmdir()
            self.assertFalse(create_dir_path.is_dir())
            create_dir_path_str = str(create_dir_path)
            self.assertEqual(create_dir(create_dir_path_str), create_dir_path)
            self.assertTrue(create_dir_path.is_dir())
        except Exception as exc:
            raise exc
        finally:
            if create_dir_path.is_dir():
                create_dir_path.rmdir()
        with self.assertRaises(TypeError):
            _ = existing_file(None)
        self.success = True  # pylint: disable=attribute-defined-outside-init

    def test_int_power_of_two(self):
        """
        Test the int_power_of_two argument parser callback
        """
        self.assertEqual(int_power_of_two(524288),524288)
        self.assertEqual(int_power_of_two(16384), 16384)
        self.assertEqual(int_power_of_two(4), 4)
        self.assertEqual(int_power_of_two("8"), 8)
        self.assertEqual(int_power_of_two(16.0), 16)
        with self.assertRaises(ValueError):
            _ = int_power_of_two("hello : )")
        with self.assertRaises(ValueError):
            _ = int_power_of_two("-2")
        with self.assertRaises(ValueError):
            _ = int_power_of_two(-4)
        with self.assertRaises(TypeError):
            _ = int_power_of_two(None)
        self.success = True  # pylint: disable=attribute-defined-outside-init

    def test_positive_int(self):
        """
        Test the positive_int argument parser callback
        """
        self.assertEqual(positive_int(3), 3)
        self.assertEqual(positive_int("5"), 5)
        self.assertEqual(positive_int(22.0), 22)
        with self.assertRaises(ValueError):
            _ = positive_int("hello : )")
        with self.assertRaises(ValueError):
            _ = positive_int("-3")
        with self.assertRaises(ValueError):
            _ = positive_int(-5)
        with self.assertRaises(TypeError):
            _ = positive_int(None)
        self.success = True  # pylint: disable=attribute-defined-outside-init

    def test_logger_string_to_level(self):
        """
        Test the logger_string_to_level argument parser callback
        """
        self.assertEqual(logger_string_to_level("notset"), logging.NOTSET)
        self.assertEqual(logger_string_to_level("debug"), logging.DEBUG)
        self.assertEqual(logger_string_to_level("info"), logging.INFO)
        self.assertEqual(logger_string_to_level("warning"), logging.WARNING)
        self.assertEqual(logger_string_to_level("error"), logging.ERROR)
        self.assertEqual(logger_string_to_level("critical"), logging.CRITICAL)
        self.assertEqual(logger_string_to_level("11"), 11)
        with self.assertRaises(ValueError):
            _ = logger_string_to_level("-5")
        self.success = True  # pylint: disable=attribute-defined-outside-init
