import os
import re
import sys
import shutil

pattern = '([\w\W]*?)(@[0-9]+x)?(\.png|\.jpg|\.jpeg)'
dic = {}
count = 0

def change_name(path, add_prefix):
    global count
    global dic
    global pattern
    if os.path.isdir(path):
        for filename in os.listdir(path):
            if os.path.isfile(path + '/' + filename):
                matched = re.search(pattern, filename)
                if matched is not None:
                    prefix = matched.group(1)
                    suffix = matched.group(2)
                    enffix = matched.group(3)

                    if suffix is None:
                        suffix = ''
                    if prefix not in dic.keys():
                        dic[prefix] = add_prefix + "_" + str(count)
                        count += 1

                    new_name = dic[prefix] + enffix

                    if suffix == '@2x':
                        if not os.path.isdir(path + '/2.0x'):
                            os.mkdir(path + '/2.0x')
                        shutil.move(path + '/' + filename, path + '/2.0x/' + new_name)
                    elif suffix == '@3x':
                        if not os.path.isdir(path + '/3.0x'):
                            os.mkdir(path + '/3.0x')
                        shutil.move(path + '/' + filename, path + '/3.0x/' + new_name)
                    else:
                        os.rename(path + '/' + filename, path + '/' + new_name)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        source_path = sys.argv[1]
        nPrefix = sys.argv[2]
    else:
        nPrefix = input('Please enter the picture name prefix required:')
        # python脚本生成应用 pyinstaller -F translate.py
        # 获取运行时目录
        source_path = os.path.dirname(sys.executable)
        # source_path = os.path.dirname(os.getcwd()) + '/test/images'
        print('Current folder path:', source_path)

    change_name(source_path, nPrefix)
    print('===>>> change_name finish , count == ' + str(count))
