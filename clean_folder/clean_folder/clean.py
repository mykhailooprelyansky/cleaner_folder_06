import re
import shutil
import sys
from pathlib import Path

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r",
               "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")


TRANS = {}


for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


EXTENSIONS_DICT = {
    'images': ('.jpeg', '.png', '.jpg', '.svg', '.dng'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'documents': ('.doc', '.docx', '.txt', '.pdf', '.xls', '.xlsx', '.pptx', '.djvu', '.rtf'),
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'archives': ('.zip', '.gz', '.tar'),
}


LIST_FOLDERS = ("images", "video", "documents", "audio", "archives", "unknown")


def normalize(name):
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return new_name


main_folder = Path(sys.argv[1])


def scan(folder):
    for item in folder.iterdir():
        if item.is_file():
            scan_files(item)

        if item.is_dir():
            if item.name not in LIST_FOLDERS:
                scan(item)
                if not any(item.iterdir()):
                    item.rmdir()
    for item in folder.iterdir():
        if item.is_file():
            scan_unknown_files(item)


def scan_files(file):
    file_suffix = file.suffix.lower()
    file_name = file.stem
    for clef, values in EXTENSIONS_DICT.items():
        if file_suffix in values:
            file_normalize = normalize(file_name)
            new_file_name = file_normalize + file_suffix
            end_folder = main_folder.joinpath(clef)
            end_folder.mkdir(exist_ok=True)
            file.replace(end_folder / new_file_name)
            if clef == 'archives':
                unpack_archive_folder = end_folder / file_normalize
                unpack_archive_folder.mkdir(exist_ok=True)
                try:
                    shutil.unpack_archive(new_file_name, unpack_archive_folder)
                except shutil.ReadError:
                    unpack_archive_folder.rmdir()
                    return
                except FileNotFoundError:
                    unpack_archive_folder.rmdir()
                    return


def scan_unknown_files(file):
    file_suffix = file.suffix.lower()
    file_name = file.stem
    for clef, values in EXTENSIONS_DICT.items():
        if file_suffix not in values:
            unknown_extension = "unknown"
            unknown_file_normalize = normalize(file_name)
            new_unknown_file_name = unknown_file_normalize + file_suffix
            unknown_folder = main_folder / unknown_extension
            unknown_folder.mkdir(exist_ok=True)
            try:
                file.replace(unknown_folder / new_unknown_file_name)
            except FileNotFoundError:
                pass


def main():
    path = sys.argv[1]
    print(f"Start in {path}")
    scan(Path(path))