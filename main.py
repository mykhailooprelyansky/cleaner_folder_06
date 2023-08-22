import shutil
import sys
from pathlib import Path
import normalize

EXTENSIONS_DICT = {
    'images': ('.jpeg', '.png', '.jpg', '.svg', '.dng'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'documents': ('.doc', '.docx', '.txt', '.pdf', '.xls', '.xlsx', '.pptx', '.djvu', '.rtf'),
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'archives': ('.zip', '.gz', '.tar'),
}


LIST_FOLDERS = ("images", "video", "documents", "audio", "archives", "unknown")


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
    for key, values in EXTENSIONS_DICT.items():
        if file_suffix in values:
            file_normalize = normalize.normalize(file_name)
            new_file_name = file_normalize + file_suffix
            end_folder = main_folder.joinpath(key)
            end_folder.mkdir(exist_ok=True)
            file.replace(end_folder / new_file_name)
            if key == 'archives':
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
    for key, values in EXTENSIONS_DICT.items():
        if file_suffix not in values:
            unknown_extension = "unknown"
            unknown_file_normalize = normalize.normalize(file_name)
            new_unknown_file_name = unknown_file_normalize + file_suffix
            unknown_folder = main_folder / unknown_extension
            unknown_folder.mkdir(exist_ok=True)
            try:
                file.replace(unknown_folder / new_unknown_file_name)
            except FileNotFoundError:
                pass




if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    scan(Path(path))
