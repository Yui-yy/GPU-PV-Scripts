from shutil import copy
import os
from tkinter import filedialog




os.system("devcon.exe driverfiles * > driverfiles.txt")



# get all gpu name
def get_gpu_name_list():
    gpu_names = os.popen('wmic path Win32_VideoController get name').read()
    #split text with \n
    gpu_names = gpu_names.split('\n')
    #Remove spaces from the right of a string
    gpu_names = [x.rstrip() for x in gpu_names]
    #clear empty element
    gpu_names = [x for x in gpu_names if x != '']
    #Remove elements if they are equal to "name", ignoring case
    gpu_names = [x for x in gpu_names if x.lower() != 'name']
    return gpu_names



#print gpu names with index
def print_gpu_name_list(gpu_names):
    for i in range(len(gpu_names)):
        print(str(i+1) + ': ' + gpu_names[i])


#Use user input to select gpu and check if valid and ask user to confirm
def select_gpu_name(gpu_names):
    while True:
        try:
            gpu_name = input('Select GPU: ')
            gpu_name = gpu_names[int(gpu_name)-1]
            print('Selected GPU: ' + gpu_name)
            break
        except:
            print('Invalid input. Try again.')
    return gpu_name


gpu_names = get_gpu_name_list()
print_gpu_name_list(gpu_names)
gpuname = select_gpu_name(gpu_names)
#Select the drive file save path or save the script folder
def select_path():
    while True:
        try:
            path = input('Do you want to select the drive file save path? If not then save to script directory (y/n): ')
            if path == 'y':
                path = filedialog.askdirectory()+"/"
                break
            elif path == 'n':
                path = os.getcwd()+"/"
                break
            else:
                print('Invalid input. Try again.')
        except:
            print('Invalid input. Try again.')
    return path

drive_file_save_path = select_path()
#show user the path to save driver file
print('The driver files will be saved in: ' + drive_file_save_path)


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


filename = os.path.join(os.path.dirname(__file__), "driverfiles.txt").replace("\\", "/")

f = open(filename)
info = f.readlines()
flg = False
filepath = []
for line in info:
    if line.lower().replace(" ", "").__contains__(gpuname.lower().replace(" ", "")):
        flg = True
        continue
    if flg:
        if line.replace(" ", "").lower().find("c:\\") == 0:
            filepath.append(line[line.find("C:\\") :])
        if line.lower().__contains__("name"):
            break
    else:
        flg = False


for fname in filepath:
    fname = fname.replace("\n", "")
    basename: str = os.path.basename(fname)
    dirname: str = os.path.dirname(fname)
    dirname = dirname.replace("C:\\", drive_file_save_path)
    if dirname.__contains__("DriverStore"):
        dirname = dirname.replace("DriverStore", "HostDriverStore")
    mkdir(dirname)
    copy(fname, dirname)
