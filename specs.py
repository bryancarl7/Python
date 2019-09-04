import platform
import datetime
import os
import subprocess
import operator
import csv
import time
from psutil import virtual_memory, boot_time, disk_partitions, disk_usage

# pre-load some memory/cpu variables
memory = virtual_memory()
boot = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
return_var = subprocess.check_output(['/usr/sbin/sysctl', "-n", "machdep.cpu.brand_string"]).strip()

# Setup disk_partitions
disks = disk_partitions()
disk_count = len(disks)
free = disk_usage(disks[0].mountpoint).total

# bytes pretty-printing
UNITS_MAPPING = [
    (1<<50, ' PB'),
    (1<<40, ' TB'),
    (1<<30, ' GB'),
    (1<<20, ' MB'),
    (1<<10, ' KB'),
    (1, (' byte', ' bytes')),
]

# Source:
# https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def pretty_size(bytes, units=UNITS_MAPPING):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = int(bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix

# From my github, function to list files from smallest to largest
def csv_print_dictionary(filename, dictionary):
    '''
    (string, dict) -> None
    prints dictinary contents out to a txt file
    '''
    sort = sorted(dictionary.items(), key=operator.itemgetter(1))
    with open(filename, mode='w') as file:
        filewriter = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for instance in sort:
            filewriter.writerow([str(instance[0]), pretty_size(instance[1])])
    return


# nice lil print statements
print("\n\n------------------------------ Device Info -------------------------------\n|\n|")
print("| Name of PC: \t\t\t" + str(platform.node()) + "\n|")
print("| Machine Platform: \t\t" + str(platform.machine()) + "\n|")
print("| Operating System: \t\t" + str(platform.system()) + "\n|")
print("| Platform Processor: \t\t" + str(return_var).replace("b", "")[1:-1] + "\n|") # a little finnicky to remove quotes
print("| Physical Memory: \t\t" + pretty_size(memory.total) + "\n|")
print("| Number of Partitions: \t" + str(disk_count) + "\n|")
print("| Total Free Space on drives: \t" + str(pretty_size(free)) + "\n|")
print("|\tUsed: \n|")
for instance in disks:  # Loop through the disks to get their usage
    print("|\t" +str(pretty_size(disk_usage(instance.mountpoint).used))+ ":\t" + instance.mountpoint+ "\n|")
print("| Python Implementation: \t" + str(platform.python_implementation()) + " with version: "+ str(platform.python_version()) + "\n|")
print("| Last Shutdown: \t\t" + boot + "\n|")
print("|\n---------------------------------------------------------------------------\n\n")

time.sleep(2)
response = input("Would you like to scan this computer for the largest files? (Y/N) ")

# Go down this branch if the user wants a report of largest files
if response.lower() == 'y':
    csv_file = input("\nPlease provide a new filename to print objects to (end with .csv): ")
    print("\nThis may take up to 5 minutes to complete.")
    time.sleep(2)
    print("\nScanning all files on hard drive...")
    # Getting the current work directory (cwd)
    directories = []

    # r=root, d=directories, f = files
    if os.name == "nt":
        print("Not tested for windows so this may not work!")
        for resource, directory, files in os.walk("C:\\"):
            for file in files:
                directories.append(os.path.join(resource, file))
    else:
        for resource, directory, files in os.walk("/"):
            for file in files:
                directories.append(os.path.join(resource, file))

    size_dict = {}
    for file in directories:
        if os.path.isfile(file):
            size = os.stat(file)
            if size.st_size > 10000000:
                size_dict[file] = size.st_size

    # Print out the report to a csv
    print("\nRecorded all file sizes, printing output to " + csv_file)
    csv_print_dictionary(csv_file, size_dict)

    # Throw some print statements in for information
    print("\nComplete!")
    time.sleep(2)
    print("\nCheckout " + csv_file + " for the full report, anything below 100000 bytes is not listed")
