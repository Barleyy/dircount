import pytest
from commands import *
from test_cases import CaseDefinition, current_dir, test_dir
import zipfile
import shutil as sh

logger = logging.getLogger("test runner")
logging.basicConfig(level=logging.WARN)

ZIP_FILE = "ex_prog.zip"
paths = CaseDefinition.get_all_paths()
expectations = CaseDefinition.get_all_expectations()


def setup_module(module):
    logger.info("Extracting test cases")
    with zipfile.ZipFile(f"{current_dir}/{ZIP_FILE}", 'r') as zip_ref:
        zip_ref.extractall(current_dir)


def teardown_module(module):
    logger.info(f"Deleting extracted tests directory {test_dir}")
    sh.rmtree(test_dir)


class Test:
    @pytest.mark.parametrize(["path", "variable_expectations"], [(p, e) for p, e in zip(paths, expectations)])
    def test_integration_test(self, path, variable_expectations):
        logger.info("Executing integration test at: ", path)
        function_main = Function(path, "TEST_MAIN", 0, None)
        Function.function_stack.append(function_main)
        function_main.perform_function_code()
        variable_stack = function_main.variable_stack
        Test.verify_expectations(variable_expectations, variable_stack)
        Function.function_stack.pop()

    @staticmethod
    def verify_expectations(variable_expectations, stack):
        logger.info(expectations)
        assert len(stack.var_stack) == len(variable_expectations)
        for expectation in variable_expectations:
            assert stack.check_if_var_exists_by_name(expectation.name)
            var = stack.get_var_by_name(expectation.name)
            assert var.type == expectation.type
            assert var.value == expectation.value
