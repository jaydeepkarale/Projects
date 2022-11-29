import pytest
import tempfile
from main import (
    start_script,
    # read_files_from_source_directory,
    check_if_directory_exists,
    move_files,
    check_if_file_already_exists
)


@pytest.fixture()
def create_tmp_directory(tmpdir):
    p = tmpdir.mkdir("sub")
    return p


def test_check_if_dest_directory_exists(create_tmp_directory):
    assert check_if_directory_exists(create_tmp_directory) is True


def test_check_return_false_if_directory_does_not_exists():
    assert check_if_directory_exists('../etc') is False


def test_check_return_true_if_file_already_exists():
    with tempfile.NamedTemporaryFile() as f:
        f.write(b'Hello World')
        assert check_if_file_already_exists(f.name) is True


def test_check_return_false_if_file_does_not_exists():
    assert check_if_file_already_exists('./anyname.py') is False


def test_move_file_from_src_dest():
    assert move_files(
        source_directory='sample_src/',
        destination_directory='sample_dest/',
        extension='txt'
    ) is True


def test_move_file_from_dest_src():
    assert move_files(
        source_directory='sample_dest/',
        destination_directory='sample_src/',
        extension='txt'
    ) is True
