import os
import shutil
import sys

def is_video_file(path):
    filename = os.path.basename(path)
    video_extensions = ['.mp4', '.avi', '.flv', '.wmv', '.mov', '.MOV', '.MP4', '.AVI', '.FLV', '.WMV']
    return any(filename.endswith(ext) for ext in video_extensions)

def is_hidden_file(path):
    filename = os.path.basename(path)
    hidden_beginners = ['._', '.DS_Store']
    return any(filename.startswith(beginner) for beginner in hidden_beginners)

def copy_files(source_path, destination_path):
    if not os.path.exists(source_path):
        print("Source path does not exist!")
        return
    if not os.path.exists(destination_path):
        print("Destination path does not exist!")
        return

    print("Source path: {}".format(source_path))
    print("Destination path: {}".format(destination_path))

    # get the number and size of files to be copied
    num_files = 0
    size_files = .0 # KB
    for root, _, files in os.walk(source_path):
        for file in files:
            if not is_video_file(file) and not is_hidden_file(file):
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_path, source_file[len(source_path) + 1:])
                if not os.path.exists(destination_file) or os.path.getmtime(source_file) > os.path.getmtime(destination_file):
                    try:
                        size_files += os.path.getsize(source_file) / 1024
                        num_files += 1
                    except FileNotFoundError:
                        print("FileNotFoundError: {}".format(source_file))
                
    # estimate the time to copy files
    time_estimate = size_files / 1024 / 30
    print("There are {} files to be copied, total size is {:.2f}MB, estimated time is {:.2f} seconds.".format(num_files, size_files / 1024, time_estimate))

    # ask for confirmation
    while True:
        answer = input("Do you want to continue? (y/n)\n\tType y also if you want to copy empty folders (which will not be calculated).\n")
        if answer == "y":
            break
        elif answer == "n":
            return
        else:
            print("Please input y or n!")

    # copy files
    num_files_copied = 0
    size_files_copied = .0
    for root, dirs, files in os.walk(source_path):
        for dir in dirs:
            destination_dir = os.path.join(destination_path, root[len(source_path) + 1:], dir)
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir, exist_ok=True)
        for file in files:
            if not is_video_file(file) and not is_hidden_file(file):
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_path, source_file[len(source_path) + 1:])
                destination_dir = os.path.dirname(destination_file)
                if not os.path.exists(destination_file):
                    print("Copying {} to {}...".format(source_file, destination_file))
                    os.makedirs(destination_dir, exist_ok=True)
                    try:
                        shutil.copy(source_file, destination_file)
                        num_files_copied += 1
                        size_files_copied += os.path.getsize(source_file) / 1024
                    except FileNotFoundError:
                        print("FileNotFoundError: {}".format(source_file))
                elif os.path.getmtime(source_file) > os.path.getmtime(destination_file):
                    print("Copying {} to {}...".format(source_file, destination_file))
                    try:
                        os.remove(destination_file)
                    except FileNotFoundError:
                        print("FileNotFoundError: {}".format(destination_file))
                    try:
                        shutil.copy(source_file, destination_file)
                        num_files_copied += 1
                        size_files_copied += os.path.getsize(source_file) / 1024
                    except FileNotFoundError:
                        print("FileNotFoundError: {}".format(source_file))

    print("Copy finished! {} files copied, total size is {:.2f}MB.".format(num_files_copied, size_files_copied / 1024))


    # get the number of files to be deleted
    num_files = 0
    for root, _, files in os.walk(destination_path):
        for file in files:
            if not is_video_file(file) and not is_hidden_file(file):
                destination_file = os.path.join(root, file)
                source_file = os.path.join(source_path, destination_file[len(destination_path) + 1:])
                if not os.path.exists(source_file):
                    num_files += 1

    print("There are {} files to be deleted.".format(num_files))

    # ask for confirmation
    while True:
        answer = input("Do you want to continue? (y/n)")
        if answer == "y":
            break
        elif answer == "n":
            return
        else:
            print("Please input y or n!")

    # remove duplicate files
    num_files_deleted = 0
    for root, _, files in os.walk(destination_path):
        for file in files:
            if not is_video_file(file) and not is_hidden_file(file):
                destination_file = os.path.join(root, file)
                source_file = os.path.join(source_path, destination_file[len(destination_path) + 1:])
                if not os.path.exists(source_file):
                    print("Deleting {}...".format(destination_file))
                    try:
                        os.remove(destination_file)
                        num_files_deleted += 1
                    except FileNotFoundError:
                        print("FileNotFoundError: {}".format(destination_file))

    print("Delete finished! {} files deleted.".format(num_files_deleted))

    # get the number of dirs to be removed
    num_dirs = 0
    for root, dirs, _ in os.walk(destination_path):
        for dir in dirs:
            destination_dir = os.path.join(root, dir)
            source_dir = os.path.join(source_path, destination_dir[len(destination_path) + 1:])
            if not os.path.exists(source_dir):
                num_dirs += 1

    print("There are {} dirs to be removed.".format(num_dirs))

    # ask for confirmation
    while True:
        answer = input("Do you want to continue? (y/n)")
        if answer == "y":
            break
        elif answer == "n":
            return
        else:
            print("Please input y or n!")

    # remove duplicate dirs
    num_dirs_deleted = 0
    for root, dirs, _ in os.walk(destination_path):
        for dir in dirs:
            destination_dir = os.path.join(root, dir)
            source_dir = os.path.join(source_path, destination_dir[len(destination_path) + 1:])
            if not os.path.exists(source_dir):
                # exam if the dir contains no files. If so, remove it. Use os.walk() to exam recursively.
                num_files = 0
                for _, _, files in os.walk(destination_dir):
                    for file in files:
                        if not is_hidden_file(file):
                            num_files += 1
                if num_files == 0:
                    print("Removing {}...".format(destination_dir))
                    shutil.rmtree(destination_dir)
                    num_dirs_deleted += 1

    print("Remove finished! {} dirs removed recursively.".format(num_dirs_deleted))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python copy_files.py source_path destination_path")
    else:
        copy_files(sys.argv[1], sys.argv[2])
