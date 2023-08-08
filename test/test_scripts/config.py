" Constants used in running tests "

# imports
import pathlib


class TestRoutineConstants:
    """
    constants used in running tests
    """

    # Paths to locations inside the code base
    TEST_DIR_PATH = (pathlib.Path(__file__).parent.parent).resolve()
    TEST_DATA_DIR_PATH = TEST_DIR_PATH / "data"
    # Names of and paths to directories and files used in testing
    TEST_DATA_FILE_ROOT_DIR_NAME = "test_file_root_dir"
    TEST_DATA_FILE_SUB_DIR_NAME = "test_file_sub_dir"
    TEST_DATA_FILE_NAME = "1a0ceb89-b5f0-45dc-9c12-63d3020e2217.dat"
    TEST_DATA_FILE_ROOT_DIR_PATH = TEST_DATA_DIR_PATH / TEST_DATA_FILE_ROOT_DIR_NAME
    TEST_DATA_FILE_PATH = (
        TEST_DATA_DIR_PATH
        / TEST_DATA_FILE_ROOT_DIR_NAME
        / TEST_DATA_FILE_SUB_DIR_NAME
        / TEST_DATA_FILE_NAME
    )

TEST_CONST = TestRoutineConstants()
