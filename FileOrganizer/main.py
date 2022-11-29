import argparse
from pathlib import Path
import shutil
import logging
from datetime import datetime
import sys

LOG_FILE_NAME = f'downloadfoldercleaner_{datetime.utcnow().strftime(format("%Y%m%d%H%M%S"))}.log'
logger = logging.getLogger("downloadercleaner")
logging.basicConfig(
    filename=LOG_FILE_NAME, # comment this line to redirect output to console
    #stream=sys.stdout, # uncomment this line to redirect output to console
    format="%(asctime)s--%(levelname)s--%(message)s",
    level=logging.DEBUG
)


def check_if_directory_exists(path: str):
    logger.info(f"Checking if directory={path} exists ")
    ret_val = False
    ret_val = Path(path).is_dir()
    if ret_val:
        logger.info(f"{path} exists returning {ret_val}")
        ret_val = True
    else:
        logger.info(f"{path} does not exist returning {ret_val}")
    return ret_val


def check_if_file_already_exists(file: str):
    return Path(file).is_file()


def read_files_from_source_directory(
        source_directory: str,
        extension: str
):
    logger.info(f"Processing files of extension={extension}")
    files = Path(source_directory)
    all_files = files.glob(f'**/*.{extension}')
    return all_files


def move_files(
        source_directory: str,
        destination_directory: str,
        extension: str
):
    move_complete = False
    try:
        file_counter = 0
        all_files = read_files_from_source_directory(
            source_directory=source_directory,
            extension=extension
        )
        for file in all_files:
            filename = file.stem + file.suffix
            logger.info(f"Moving file={filename} to directory={destination_directory}")
            destination = destination_directory
            if check_if_file_already_exists(destination):
                logger.info(f"file={filename} already exists in directory={destination_directory}..skipping")
                continue
            shutil.move(file, destination)
            file_counter = file_counter + 1
        logger.info(f"Total files moved for extension={extension} is {file_counter}")
        move_complete = True
    except Exception as ex:
        logger.error(f"{str(ex)}")
    finally:
        return move_complete


def start_script(**kwargs):
    source_directory = kwargs.get('source_directory')
    destination_directory = kwargs.get('destination_directory')
    extension = kwargs.get('file_extension')

    if not check_if_directory_exists(source_directory):
        logger.error(f"Source directory {source_directory} does not exist")
        return False

    if not check_if_directory_exists(destination_directory):
        logger.error(f"Destination directory {destination_directory} does not exist")
        return False

    completed_string = "without errors"
    logger.info(f"Staring script at {datetime.now().strftime('%d-%m-%Y %H-%M-%S')} "
                f"to move files from [src={source_directory}] to [dest={destination_directory}] "
                f"for {extension} files")
    if not move_files(
        source_directory=source_directory,
        destination_directory=destination_directory,
        extension=extension
    ):
        completed_string = "with errors"
    logger.info(f"Completed script {completed_string} at {datetime.now().strftime('%d-%m-%Y %H-%M-%S')}")


if __name__ == "__main__":
    arguments = argparse.ArgumentParser()
    arguments.add_argument(
        '--source_directory',
        help='Directory from which files should be picked'
             'example: C:/Users/Downloads/',
        type=str,
        required=True
    )
    arguments.add_argument(
        '--destination_directory',
        help='Directory to which files should be moved'
             'example: C:/Users/Uploads/',
        type=str,
        required=True
    )
    arguments.add_argument(
        '--file_extension',
        help='Type of files should be moved png, jpeg, jpg, pdf etc',
        type=str,
        required=True
    )
    args = arguments.parse_args()
    start_script(**vars(args))
