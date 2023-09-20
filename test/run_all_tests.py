" Run all of the unittests plus some linting and formatting checks "

# imports
import unittest
import subprocess
import pathlib
import re
from argparse import ArgumentParser
from openmsitoolbox.logging import OpenMSILogger

# constants
TEST_DIR_PATH = pathlib.Path(__file__).resolve().parent
TOP_DIR_PATH = TEST_DIR_PATH.parent
TEST_SCRIPT_DIR_PATH = TEST_DIR_PATH / "test_scripts"
CWD = pathlib.Path().resolve()
LOGGER = OpenMSILogger("run_all_tests")


def get_args(args):
    """
    Return the parsed command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument(
        "--no_pyflakes",
        action="store_true",
        help="Add this flag to skip running the pyflakes check",
    )
    parser.add_argument(
        "--no_formatting",
        action="store_true",
        help="Add this flag to skip running the formatting checks",
    )
    parser.add_argument(
        "--no_pylint",
        action="store_true",
        help="Add this flag to skip running the pylint checks",
    )
    script_test_opts = parser.add_mutually_exclusive_group()
    script_test_opts.add_argument(
        "--no_script_tests",
        action="store_true",
        help=f"Add this flag to skip running the tests in {TEST_SCRIPT_DIR_PATH.name}",
    )
    script_test_opts.add_argument(
        "--test_regex",
        type=re.compile,
        default=None,
        help="Only tests whose function names match this regex will be run",
    )
    parser.add_argument(
        "--failfast",
        action="store_true",
        help="Add this flag to exit after the first failed test",
    )
    return parser.parse_args(args=args)


def test_pyflakes(args):
    """
    If requested, run pyflakes and check the output for errors
    """
    if args.no_pyflakes:
        LOGGER.info("SKIPPING PYFLAKES TEST")
    else:
        LOGGER.info("testing code consistency with pyflakes...")
        cmd = (
            f"cd {TOP_DIR_PATH}; pyflakes .; cd {TEST_DIR_PATH}; pyflakes.; "
            f"cd {CWD}; exit 0"
        )
        with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True,
        ) as proc:
            stdout, _ = proc.communicate()
            if stdout != "":
                LOGGER.error(
                    f"ERROR: pyflakes check failed with output:\n{stdout}",
                    exc_type=RuntimeError,
                )
        LOGGER.info("Passed pyflakes check : )")


def test_formatting(args):
    """
    If requested, run a formatting check with Black and check the output
    """
    if args.no_formatting:
        LOGGER.info("SKIPPING FORMATTING TEST")
    else:
        LOGGER.info("testing code formatting with Black...")
        cmd = (
            f"cd {TOP_DIR_PATH}; black openmsitoolbox --check; black test --check; "
            f"cd {CWD}; exit 0"
        )
        with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True,
        ) as proc:
            stdout, _ = proc.communicate()
            if stdout != "":
                LOGGER.error(
                    f"ERROR: formatting check failed with output:\n{stdout}",
                    exc_type=RuntimeError,
                )
            LOGGER.info("Passed formatting check : )")


def test_pylint(args):
    """
    If requested, run pylint and check the output for errors
    """
    if args.no_pylint:
        LOGGER.info("SKIPPING PYLINT TEST")
    else:
        LOGGER.info("testing code consistency with pylint...")
        cmd = (
            f"cd {TOP_DIR_PATH}; pylint openmsitoolbox; pylint --recursive=y test; "
            f"cd {CWD}; exit 0"
        )
        with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            universal_newlines=True,
        ) as proc:
            stdout, _ = proc.communicate()
            if stdout != "":
                LOGGER.error(
                    f"ERROR: pylint checks failed with output:\n{stdout}",
                    exc_type=RuntimeError,
                )
        LOGGER.info("Passed pylint checks : )")


def skip_unmatched_tests(args, suites):
    """
    If a regex was given to specify which tests to run, set any that don't match it to skip
    """
    if args.test_regex is not None:
        for suite in suites:
            for test_group in suite._tests:  # pylint: disable=protected-access
                for test in test_group:
                    # pylint: disable=protected-access
                    if not args.test_regex.match(test._testMethodName):
                        # pylint: disable=protected-access
                        test_name = test._testMethodName
                        msg = (
                            f"tests that don't match the regex '{args.test_regex}' "
                            "are being skipped"
                        )
                        setattr(
                            test,
                            test_name,
                            unittest.skip(msg)(getattr(test, test_name)),
                        )


def run_script_tests(args):
    """
    Run all requested tests defined in the "test_scripts" directory
    """
    if args.no_script_tests:
        LOGGER.info("SKIPPING SCRIPT TESTS")
    else:
        LOGGER.info(f"Running tests in {TEST_SCRIPT_DIR_PATH}...")
        # load all of the tests into suites
        loader = unittest.TestLoader()
        suites = loader.discover(TEST_SCRIPT_DIR_PATH)
        if len(loader.errors) > 0:
            errmsg = "ERROR: encountered the following errors in loading tests:\n\t"
            errmsg += "\n\t".join([str(error) for error in loader.errors])
            LOGGER.error(errmsg, exc_type=RuntimeError)
        # otherwise, if only some tests will be run. Set any that don't match the regex to skip
        skip_unmatched_tests(args, suites)
        # actually run all of the requested tests
        runner_kwargs = {"verbosity": 3}
        if args.failfast:
            runner_kwargs["failfast"] = True
        runner = unittest.TextTestRunner(**runner_kwargs)
        result = runner.run(suites)
        # check for any errors or failures
        if len(result.errors) > 0 or len(result.failures) > 0:
            raise RuntimeError(
                "ERROR: some test(s) failed! See output above for details."
            )
        LOGGER.info("All script tests complete : )")


def main(args=None):
    """
    Main function to run the script
    """
    args = get_args(args)
    test_pyflakes(args)
    test_formatting(args)
    test_pylint(args)
    run_script_tests(args)
    # If we've made it here all the (requested) tests passed!
    msg = "All "
    if (
        args.no_pyflakes
        or args.no_pylint
        or args.no_formatting
        or args.no_script_tests
        or args.test_regex
    ):
        msg += "requested "
    msg += "tests passed!"
    LOGGER.info(msg)


if __name__ == "__main__":
    main()
