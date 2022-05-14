from concurrent.futures import process
from shutil import copy
import os, sys
from tkinter import filedialog
import zipfile
import re


class ProgressBar(object):
    DEFAULT = "Progress: %(bar)s %(percent)3d%%"
    FULL = "%(bar)s %(current)d/%(total)d (%(percent)3d%%) %(remaining)d to go"

    def __init__(self, total, width=40, fmt=DEFAULT, symbol="=", output=sys.stderr):
        assert len(symbol) == 1

        self.total = total
        self.width = width
        self.symbol = symbol
        self.output = output
        self.fmt = re.sub(r"(?P<name>%\(.+?\))d", r"\g<name>%dd" % len(str(total)), fmt)

        self.current = 0

    def __call__(self):
        percent = self.current / float(self.total)
        size = int(self.width * percent)
        remaining = self.total - self.current
        bar = "[" + self.symbol * size + " " * (self.width - size) + "]"

        args = {
            "total": self.total,
            "bar": bar,
            "current": self.current,
            "percent": percent * 100,
            "remaining": remaining,
        }
        print("\r" + self.fmt % args, file=self.output, end="")

    def done(self):
        self.current = self.total
        self()
        print("", file=self.output)


# get all gpu info
def get_gpu_infos():
    # get gpu info
    def get_gpu_info(info_text):
        gpu_info = {}
        for i in range(len(info_text)):
            # if line has ":" add to gpu_info
            if ":" in info_text[i]:
                # Start a new loop from the current index +1
                for j in range(i + 1, len(info_text)):
                    # if line has ":" save j to index, if not break index = j
                    if ":" in info_text[j]:
                        index = j
                        break
                    else:
                        index = j + 1
                # if key equal to "Name" then value convert to str
                if info_text[i].split(":")[0].strip() == "Name":
                    # check value has element
                    if len(info_text[i + 1 : index]) > 0:
                        value = str(info_text[i + 1 : index][0])
                else:
                    value = info_text[i + 1 : index]
                # add key and value to gpu_info
                gpu_info[info_text[i].split(":")[0].strip()] = value
                # gpu_info[info_text[i].replace(":", "")] = info_text[i + 1 : index]
        return gpu_info

    gpu_infos = []
    devcon_output = os.popen("devcon.exe hwids =display").read()
    # replace ":" with ": \n"
    devcon_output = devcon_output.replace(":", ": \n")
    # split text with \n
    devcon_output = devcon_output.split("\n")
    # remove left and right spaces and empty elements
    devcon_output = [x.strip() for x in devcon_output if x != ""]
    # remove last element
    devcon_output = devcon_output[:-1]
    # split device info with name
    for i in range(len(devcon_output)):
        # if line equals "name:"
        if devcon_output[i].lower() == "name:":
            # start a new loop from the current index +1
            for j in range(i + 1, len(devcon_output)):
                # if line equals "name:" save j to index, if not break index = j
                if devcon_output[j].lower() == "name:":
                    index = j
                    break
                else:
                    index = j + 1
            # add gpu info to gpu_infos
            gpu_infos.append(get_gpu_info(devcon_output[i:index]))
    return gpu_infos


# Use user input to select gpu and check if valid and ask user to confirm then return first element in Hardware IDs
def get_gpu_hardware_id(gpu_infos):
    # print gpu names with index
    def print_gpu_name_list(gpu_infos):
        for i in range(len(gpu_infos)):
            print(str(i + 1) + ". " + gpu_infos[i]["Name"])
    def select_gpu(gpu_infos):
        while True:
            try:
                print_gpu_name_list(gpu_infos)
                gpu_index = int(input("Select the GPU index: "))
                if gpu_index > len(gpu_infos) or gpu_index < 1:
                    print("Invalid input. Try again.")
                else:
                    print("You have selected: " + gpu_infos[gpu_index - 1]["Name"])
                    break
            except:
                print("Invalid input. Try again.")
        # if Hardware IDs is not empty then return the first element
        if gpu_infos[gpu_index - 1]["Hardware IDs"] != "":
            return gpu_infos[gpu_index - 1]["Hardware IDs"][0]
        else:
            return None

    return select_gpu(gpu_infos)


# Select the drive file save path or save to the script folder
def select_path():
    while True:
        try:
            path = input(
                "Do you want to select the drive file save path? If not then save to script directory (y/n): "
            )
            if path == "y":
                path = filedialog.askdirectory() + "/"
                break
            elif path == "n":
                path = os.getcwd() + "/"
                break
            else:
                print("Invalid input. Try again.")
        except:
            print("Invalid input. Try again.")
    return path


# find driverfilewith the gpu_hardware_id
def find_driver_file_path(gpu_hardware_id):
    driver_file_path = os.popen(
        'devcon.exe driverfiles "{0}"'.format(gpu_hardware_id)
    ).read()
    # split with \n and remove empty elements and left and right spaces
    driver_file_path = [x.strip() for x in driver_file_path.split("\n") if x != ""]
    # remove all elements that are not paths
    driver_file_path = [x for x in driver_file_path if os.path.exists(x)]
    return driver_file_path




gpu_infos = get_gpu_infos()
gpu_hardware_id = get_gpu_hardware_id(gpu_infos)
drive_file_save_path = select_path() + "DriverFiles/"
driver_file_path = find_driver_file_path(gpu_hardware_id)
# show user the path to save driver file
print("The driver files will be saved in: " + drive_file_save_path)


progress = ProgressBar(len(driver_file_path), fmt=ProgressBar.FULL)
for fname in driver_file_path:
    # get base name
    base_name = os.path.basename(fname)
    # get file folder
    file_folder = os.path.dirname(fname)
    # replace file folder disk letter to drive file save path
    file_folder = file_folder.replace("C:\\", drive_file_save_path)
    # if path has "DriverStore" then replace it with "HostDriverStore"
    if "DriverStore" in file_folder:
        file_folder = file_folder.replace("DriverStore", "HostDriverStore")
    # create folder if not exist
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)
    # copy file to drive file save path
    copy(fname, file_folder)
    progress.current += 1
    progress()
progress.done()


print("The driver files have been saved in: " + drive_file_save_path)

# open the folder
os.startfile(drive_file_save_path)
print("Done!")
