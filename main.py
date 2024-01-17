from datetime import datetime
from os import path, mkdir, listdir
from shutil import move
from sys import exit
# import tkinter as tk
from tkinter.filedialog import askdirectory

from PIL.Image import open as open_image
from PIL.ExifTags import TAGS as Exif_tags


# 获取拍摄时间的年月
def get_date_taken(filename):
    is_image = False
    try:
        # 尝试打开文件
        with open_image(filename) as img:
            is_image = True
    except OSError:
        is_image = False
    if not is_image:
        return None
    image_exif = open_image(filename)._getexif()
    if image_exif:
        exif = {Exif_tags[k]: v for k, v in image_exif.items() if k in Exif_tags and type(v) is not bytes}
        # 截取年月
        date_obj = datetime.strptime(exif['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
        return date_obj
    else:
        return None


def move_files_to_date_folders(source_folder, target_folder):
    # 检查源文件夹和目标文件夹是否存在
    if not path.exists(source_folder):
        print("源文件夹不存在")
        return
    if not path.exists(target_folder):
        mkdir(target_folder)

    file_num = 0
    # 遍历源文件夹中的文件
    for file in listdir(source_folder):
        file_path = path.join(source_folder, file)
        # 检查文件是否为普通文件（不是文件夹）
        if path.isfile(file_path):
            # 尝试获取照片的拍摄时间
            date_taken = get_date_taken(file_path)
            if date_taken is None:
                # 获取文件的修改时间
                modified_time = path.getmtime(file_path)
            else:
                modified_time = date_taken.timestamp()
            # 使用修改时间作为文件夹名称创建目标文件夹
            target_folder_name = path.join(target_folder,
                                           datetime.fromtimestamp(modified_time).strftime('%Y%m'))

            if not path.exists(target_folder_name):
                mkdir(target_folder_name)
            # 移动文件到目标文件夹
            move(file_path, target_folder_name)
            print(path.basename(file) + " -> " + target_folder_name)
            file_num = file_num + 1

    print('已完成！共移动文件数：' + str(file_num))


# 定义选择文件夹的函数
def select_folder():
    folder_path = askdirectory()
    return folder_path


def select_folder_confirm():
    select_result1 = input("请选择文件夹:\n1.选择目录\n2.关闭\n")
    if select_result1 == '2':
        exit()
    confirm_folder_path = select_folder()
    print("已选择的文件夹路径：" + confirm_folder_path)
    input_result = input("1.确认\n2.重选\n")
    if input_result == '2':
        select_folder_confirm()
    return confirm_folder_path


def move_file(first):
    if first:
        print("🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪")
        print(
            "说明：将所选文件夹中的文件按照修改时间（如果是照片，则将尝试获取拍摄时间）进行分组，分别移动到以文件修改时间的年月命名的文件夹中。")
    select_folder_path = select_folder_confirm()

    source_folder = select_folder_path
    target_folder = select_folder_path
    move_files_to_date_folders(source_folder, target_folder)
    move_file(False)


if __name__ == '__main__':
    move_file(True)

