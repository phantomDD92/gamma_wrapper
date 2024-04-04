import json
import sys
import os
import datetime as dt
import logging
import csv

from pathlib import Path
import time


# ENCODER/DECODER to format json datetime items
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (dt.date, dt.datetime)):
            return obj.isoformat()


class CustomDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.try_datetime, *args, **kwargs)

    @staticmethod
    def try_datetime(d):
        ret = {}
        for key, value in d.items():
            try:
                ret[key] = dt.datetime.fromisoformat(value)
            except (ValueError, TypeError):
                ret[key] = value
        return ret


# LOAD / SAVE JSON
def load_json(filename: str, folder_path: str):
    path_to_file = "{}/{}.json".format(folder_path, filename)  # full filename
    if os.path.exists(path_to_file):
        with open(path_to_file, "r") as f:
            try:
                return json.load(f, cls=CustomDecoder)
            except Exception as e:
                logging.getLogger(__name__).exception(
                    "Unexpected error while loading {} file    .error: {}".format(
                        path_to_file, sys.exc_info()[0]
                    )
                )
    return None


def save_json(filename: str, data, folder_path: str) -> bool:
    """Save json to file path

    Args:
       filename (str): file name
       data (_type_): json data
       folder_path (str): folder path name

    Returns:
       bool: Returns true when successfull
    """
    timestamp = time.time()
    path_to_file = "{}/{}.json".format(folder_path, filename)  # full filename
    path_to_tempfile = "{}/{}_{}.tmp".format(
        folder_path, filename, timestamp
    )  # full filename
    # check if folder exists
    if not os.path.exists(folder_path):
        # Create a new directory
        os.makedirs(name=folder_path, exist_ok=True)

    # save it to temporary file
    with open(path_to_tempfile, "w") as f:
        try:
            json.dump(data, f, cls=CustomEncoder)
        except Exception as e:
            logging.getLogger(__name__).exception(
                "Unexpected error while saving {} file    .error: {}".format(
                    path_to_tempfile, sys.exc_info()[0]
                )
            )
            return False

        # remove old file
        try:
            os.remove(path_to_file)
        except FileNotFoundError:
            # file does not exist or something...
            pass
        except Exception:
            logging.getLogger(__name__).exception(
                "Unexpected error while deleting {} file    .error: {}".format(
                    path_to_file, sys.exc_info()[0]
                )
            )

        # rename tmp file
        try:
            os.rename(path_to_tempfile, path_to_file)
        except Exception as e:
            logging.getLogger(__name__).exception(
                "Unexpected error while renaming {} file    .error: {}".format(
                    path_to_tempfile, sys.exc_info()[0]
                )
            )
            return False

        return True

    return False


# SAVE CSV
def SaveCSV(filename, columns, rows):
    """Save multiple rows to CSV

    Arguments:
       rows {[type]} -- corresponding to fieldname headers defined like:
                       [{
                       'time': self.time,
                       'id': self.oid,
                       'side': self.side,
                       'price': self.price,
                       'size': self.size
                       }, ...]
    """
    my_file = Path(filename)
    if not my_file.is_file():
        with open(filename, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()

    with open(filename, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        for i in rows:
            writer.writerow(i)


def SaveCSV_row(filename, columns, row):
    """Save 1 row to CSV

    Arguments:
       row (dict)
    """

    my_file = Path(filename)
    # check if folder exists
    if not os.path.exists(my_file.parent):
        # Create a new directory
        os.makedirs(name=my_file.parent, exist_ok=True)

    if not my_file.is_file():
        with open(filename, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()

    with open(filename, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        writer.writerow(row)


def LoadCSV(filename):
    """Load CSV to dict

    Arguments:
       filename (str): filename

    Returns:
       list: list of dict
    """
    my_file = Path(filename)
    if not my_file.is_file():
        return []

    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        return rows


# YIELD FILES IN SPECIFIED PATH
def get_files(path: str, subfolders: bool = False):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file
        elif subfolders and os.path.isdir(os.path.join(path, file)):
            yield from get_files(path=os.path.join(path, file), subfolders=subfolders)


# SAVE TEXT
def save_text(
    filename: str,
    text: str,
    folder_path: str | None = None,
) -> bool:
    """Save text to file

    Arguments:
        folder_path (str): folder path name, without filename
       filename (str): filename
       text (str): text to save
    """

    try:
        # use current folder if no folder path is provided
        if not folder_path:
            folder_path = os.path.dirname(os.path.abspath(__file__))
        elif not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # save to folder
        _full_filename = os.path.join(folder_path, filename)

        with open(_full_filename, "w") as _file:
            _file.write(text)

        logging.getLogger(__name__).debug(f" Saved file: {_full_filename}")
        return True
    except Exception as e:
        logging.getLogger(__name__).exception(
            "Unexpected error while saving {} file    .error: {}".format(
                filename, sys.exc_info()[0]
            )
        )

    return False
