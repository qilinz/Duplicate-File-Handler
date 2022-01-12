import argparse
import hashlib
import os


# -------------------------CHECK INPUT-------------------------- #
def get_inputs():
    """
    Get inputs of user regarding format to search and sorting options
    :return: file_format, sort
    """
    file_format = input("Enter file format:\n")
    print("""Size sorting options:
1. Descending
2. Ascending""")
    while True:
        try:
            sort = int(input("Enter a sorting option:\n"))
            if sort in [1, 2]:
                break
            else:
                print("Wrong option")
        except ValueError:
            print("Wrong option")

    return file_format, sort


def check_duplicates():
    """
    If user wants to check duplicates
    :return: True for checking; False for not checking
    """
    while True:
        check = input("Check for duplicates?\n")
        if check == "yes":
            return True
        elif check == "no":
            return False
        else:
            print("Wrong option")


def delete_duplicates():
    """
    If users wants to delete duplicates files
    :return: True for deleting; False for not deleting
    """
    while True:
        check = input("Delete files?\n")
        if check == "yes":
            return True
        elif check == "no":
            return False
        else:
            print("Wrong option")


def check_index(max_count):
    """
    Collect user input and transform the input to a list of index. (start from 0 instead of 1)
    :param max_count: max count of files that can be deleted
    :return: a list of index to delete.
    """
    max_index = max_count - 1
    while True:
        try:
            list_index = [int(i) - 1 for i in input("Enter file numbers to delete:").split()]

        except ValueError:
            print("Wrong format")

        else:
            # check if empty input
            if not list_index:
                print("Wrong format")
            else:
                # check if index within the range
                if max(list_index) <= max_index and min(list_index) >= 0:
                    return list_index
                else:
                    print("Wrong format")


# -------------------------GENERATE DICT/ LIST-------------------------- #
def dict_by_size(folder_root, file_format):
    """
    Create a dict with file size as keys
    :param folder_root: folder to search
    :param file_format: file format to search. "" for all formats
    :return: dict = {
                size1: [file1, file2, ...],
                ...
             }
    """
    size_dict = {}
    for root, dirs, files in os.walk(folder_root, topdown=True):
        for name in files:
            # if match format
            # if input = "", count all the files
            if file_format == "" or name.split(".")[-1] == file_format:

                # get file path and size
                file_path = os.path.join(root, name)
                file_size = os.path.getsize(file_path)

                # add to dict
                if file_size not in size_dict:
                    size_dict[file_size] = [file_path]
                else:
                    size_dict[file_size].append(file_path)
    return size_dict


def dict_by_hash():
    """
    Create a nested dict with file size as keys for outer dict, hash_values as keys for inner dict
    :return: hash_dict = {
                size1: {
                    hash1: [file1, file2, ...],
                    hash2: [file1, file2, ...],
                    ...
                }
             }
    """
    hash_dict = {}

    # loop through the matched files
    for file_size, file_paths in matched_dict.items():
        for file_path in file_paths:
            # get the hash
            h = get_hash(file_path)

            # add to new dict with hash
            if file_size not in hash_dict:
                hash_dict[file_size] = {
                    h: [file_path]
                }
            else:
                if h not in hash_dict[file_size]:
                    hash_dict[file_size][h] = [file_path]
                else:
                    hash_dict[file_size][h].append(file_path)
    return hash_dict


# -------------------------OTHER FUNCTIONS-------------------------- #
def get_hash(full_path):
    m = hashlib.md5()
    with open(full_path, "rb") as file:
        data = file.read()
        m.update(data)
        return m.hexdigest()


def delete_files(list_file, list_index):
    """
    delete given files and return how much spaces are freed
    :param list_file: list of tuples of (file_path, file_size)
    :param list_index: list of index of files
    :return: space. how much spaces are freed
    """
    space = 0
    for index in list_index:
        file_path, file_size = list_file[index]

        # delete the file
        os.remove(file_path)
        # add freed spaces
        space += file_size

    return space


# -------------------------   MAIN  -------------------------- #
# Create arg parser
parser = argparse.ArgumentParser(description="This program lists all the files in the given root folder.")
parser.add_argument("root_folder", help="You need to type the dire you would like to search.", default=None, nargs='?')

args = parser.parse_args()
root_folder = args.root_folder

# Interact with user inputs
if root_folder:
    search_format, sort_option = get_inputs()
    file_dict = dict_by_size(root_folder, search_format)

    # sort the dict
    if sort_option == 2:
        sorted_dict = dict(sorted(file_dict.items()))
    else:
        sorted_dict = dict(sorted(file_dict.items(), reverse=True))

    # create a new dict to include files with matched size
    matched_dict = {}

    # print if files have same size
    for key, value in sorted_dict.items():
        if len(value) > 1:
            # add the matched ones to new dict
            matched_dict[key] = value
            print(f"\n{key} bytes")
            for item in value:
                print(item)

    # if check hash
    if check_duplicates():
        hashed_dict = dict_by_hash()

        # index counter
        count = 0

        # create an empty list for files might be deleted
        file_list = []

        # print the results
        for size, value in hashed_dict.items():
            print(f"\n{size} bytes")
            for h, paths in hashed_dict[size].items():
                if len(paths) > 1:
                    print("Hash:", h)
                    for path in paths:
                        count += 1
                        print(f"{count}. {path}")

                        # add the file to list
                        file_list.append((path, size))

        if delete_duplicates():
            index_list = check_index(count)
            freed_space = delete_files(file_list, index_list)
            print(f"Total freed up space: {freed_space} bytes")

else:
    print("Directory is not specified")