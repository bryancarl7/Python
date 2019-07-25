import os
import sys
import operator
import csv
# Written by Bryan Carl
# 25 July, 2018


def main(argv):
    if len(argv) != 3:
        print("Usage: python3 path.py <directory_to_list_from> <csv_file_to_print_to>")
    # Getting the current work directory (cwd)
    thisdir = argv[1]
    directories = []

    # r=root, d=directories, f = files
    for resource, directory, files in os.walk(thisdir):
        for file in files:
            directories.append(os.path.join(resource, file))

    size_dict = {}
    for file in directories:
        if os.path.isfile(file):
            size = os.stat(file)
            size_dict[file] = size.st_size

    csv_print_dictionary(argv[2], size_dict)
    return


def csv_print_dictionary(filename, dictionary):
    '''
    (string, dict) -> None
    prints dictinary contents out to a txt file
    '''
    sort = sorted(dictionary.items(), key=operator.itemgetter(1))
    with open(filename, mode='w') as file:
        filewriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for instance in sort:
            filewriter.writerow([str(instance[0]), get_size_truncated(instance[1])])
    return


def get_size_truncated(size):
    '''
    (int)->string
    takes the size of a file and converts it to plain english
    '''
    string = str(size)
    if len(string) < 3:
        return "<1 KB"
    elif len(string) == 4:
        return string[0] + "." + string[0:] + " KB"
    elif len(string) == 5:
        return string[0:1] + "." + string[1:] + " KB"
    elif len(string) == 6:
        return string[0:2] + "." + string[2:] + " KB"
    elif len(string) == 7:
        return string[0] + "." + string[0:] + " MB"
    elif len(string) == 8:
        return string[0:1] + "." + string[1:] + " MB"
    elif len(string) == 9:
        return string[0:2] + "." + string[2:] + " MB"
    elif len(string) > 10:
        return string[:-9] + "." + string[-9:]+ " GB"



if __name__ == "__main__":
    main(sys.argv[:])
