# -*- coding: utf-8 -*-
# /usr/bin/env python
# coding=utf8

import hashlib
import random
import os
import requests
import sys
from urllib import parse
import json
from string import punctuation

# 翻译能力来自百度翻译
# https://api.fanyi.baidu.com/

# appid 和 secretKey 获取自[百度翻译开放平台管理控制器]
# https://api.fanyi.baidu.com/api/trans/product/desktop?req=developer
appid = ''
secretKey = ''
baseUrl = '/api/trans/vip/translate'

add_punc = ':，。、【】“”；（）《》‘’{}？！⑦()、%^>℃.”“^-——=&#@￥'
all_punc = punctuation + add_punc


def save_file(content, save_path, suffix):
    p = os.path.split(save_path)
    file = p[1].split('.')[0]

    # 如果是路径为文件夹，写入文件
    if os.path.isdir(save_path):
        new_file = p[0] + "/" + file + suffix
        with open(new_file, "w", encoding="utf-8") as f:
            f.write(content)
            print('Generated successfully: path = ', new_file)
    # 如果是路径为文件，重写文件
    elif os.path.isfile(save_path):
        with open(save_path, 'r', encoding='utf-8') as f:
            # 按行读取内容
            old = f.readlines()
            f.close()
            if len(old) > 1:
                for i in range(len(old), -1, -1):
                    if '}' in old[i - 1]:
                        # 插入最后一行
                        old.insert(i - 1, content)
                        # 调整格式
                        old[i - 2] = old[i - 2].replace('\n', '') + ',\n'
                        break
            else:
                old.append(content)

            # 写入内容
            with open(save_path, 'w', encoding='utf-8') as f2:
                f2.writelines(old)
                f2.close()
                print('Rewrite successful:', save_path)


def translate(q, lang='zh', to_lang='en'):
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode('utf-8'))
    sign = m1.hexdigest()
    my_url = baseUrl + '?appid=' + appid + '&q=' + parse.quote(q) + '&from=' + lang + '&to=' + to_lang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        h = requests.get('https://api.fanyi.baidu.com' + my_url)
        h.encoding = 'GBK'
        result = h.text
        result = eval(result)
        result = result['trans_result'][0]['dst']
        print('Translation completed ', q, ' >>> ', result)
        return result
    except Exception as e:
        print('Request Error: ', e)
    return ''


def translate_with(data, save_path_cn, save_path_en, to='en'):
    print('Start translation...')
    # Target result data
    to_content = ''
    # Chinese language target result data
    cn_content = ''
    # replace repeat text
    all_text = []

    count = 0

    for i in range(len(data)):
        text = data[i]
        text = text.replace('\n', '')
        old_key = ''
        # flutter  String getCommodity() => "AA";
        if 'String get' in text and ' => ' in text:
            #  [String getCommodity(),"AA";]
            key_values = text.split(' => ')
            old_key = key_values[0]
            text = key_values[1][1:][:-2]
        elif text.replace(' ', '') == '':
            continue

        if len(text) == 0 or text == '\n':
            continue

        # replace repeat
        if text in all_text:
            continue
        all_text.append(text)

        count += 1

        print('Ready:【', text, '】 to: ', to)
        result = translate(text, to_lang=to)

        key = ''
        results = result.split(' ')
        for j in range(len(results)):
            if j > 3:
                break
            # Remove the special symbol as the method name
            r = results[j]
            temp = []
            for k in r:
                if k not in all_punc:
                    temp.append(k)
            r = ''.join(temp)
            if old_key == '':
                key += r.capitalize()

        if old_key == '':
            cn_content += '  "m' + key + '": "' + text + '"'
            if i == len(data) - 1:
                cn_content += '\n'
            else:
                cn_content += ',\n'

            to_content += '  "m' + key + '": "' + result + '"'
            if i == len(data) - 1:
                to_content += '\n'
            else:
                to_content += ',\n'
        else:
            to_content += '    ' + old_key + ' => "' + result + '",\n'
    if count > 0:
        if cn_content != '':
            save_file(cn_content, save_path_cn, suffix='CN.md')
        save_file(to_content, save_path_en, suffix=to + '.md')

    print('Translate finished >>> total: ', count)
    return to_content


# 检查json数据是否包含重复key
def check_key_repeat(check_path):
    with open(check_path, 'r', encoding='utf-8') as file:
        content_s = file.readlines()
        file.close()

    with open(check_path, 'r', encoding='utf-8') as f:
        content = f.read()
        f.close()
        try:
            dic = json.loads(content)
        except json.decoder.JSONDecodeError as e:
            print('❌Please check if it is json data format:', check_path)
            return

        print('Check the data path:', check_path)
        print('Total valid data:', len(dic.items()))
        print('Raw data:', len(content_s) - 2)
        replace_len = len(content_s) - 2 - len(dic.items())

        if replace_len > 0:
            print('report:【', replace_len, '】Duplicate fields, please check the file path:', check_path)
            content_keys = []
            content_replace_keys = []
            for t in content_s:
                if '": "' in t:
                    key = t.split('": "')[0][3:]
                    if key in content_keys:
                        if key not in content_replace_keys:
                            content_replace_keys.append(key)
                    else:
                        content_keys.append(key)
            print('repeat⚠️:', content_replace_keys)


#  eg. AA\nBB
#  return eg. String getSalesVolume() => "AA";\nString getCommodity() => "BB";
def get_word_from_file(p, save_path_cn, save_path_en):
    with open(p, 'r', encoding='utf-8') as f:
        content = f.readlines()
        f.close()
        return translate_with(content, save_path_cn, save_path_en)


# noinspection PyBroadException
def read_config(config_path):
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()

            js = json.dumps(content)
            resource = json.loads(js)
            data = json.loads(resource)
            print('Configuration information:', data)
            p = ''
            if 'path' in data.keys():
                p = data['path']
            s = ''
            if 'savePath_cn' in data.keys():
                s = data['savePath_cn']
            en = ''
            if 'savePath_en' in data.keys():
                en = data['savePath_en']
            en_bug = ''
            if 'savePath_en_base' in data.keys():
                en_bug = data['savePath_en_base']
            return [p, s, en, en_bug]
    except Exception:
        print('No configuration information')
        return ['', '', '']

if __name__ == '__main__':
    if 2 == sys.argv:
        get_word_from_file(sys.argv[1])
    else:
        # python脚本生成应用 pyinstaller -F translate.py
        # 获取运行时目录
        # current_dir1 = os.path.dirname(sys.executable)
        current_dir1 = os.path.dirname(__file__)

        print('<<*可选配置: /Config/translate_config*>> ')
        print('有效定义字段:')
        print('  1. path: 待翻译文件路径')
        print('  2. savePath_en: 英文保存路径（文件夹或文件，如果是文件就重写）')
        print('  3. savePath_cn: 中文保存路径（文件夹或文件，如果是文件就重写）')
        print('  4. savePath_en_base: 英文保存路径（文件夹或文件，如果是文件就重写）')
        config = current_dir1 + '/Config/translate_config'
        config = read_config(config)

        if config[0] == '':
            # 默认获取待翻译文件路径
            wait_translate_path = current_dir1 + '/wait_translate'
        else:
            wait_translate_path = config[0]

        if config[1] == '':
            # 默认获取中文保存路径
            savePath_cn = current_dir1 + '/'
        else:
            savePath_cn = current_dir1.replace('/python', '') + config[1]

        if config[2] == '':
            # 默认获取英文保存路径
            savePath_en = current_dir1 + '/'
        else:
            savePath_en = current_dir1.replace('/python', '') + config[2]

        if config[3] == '':
            # 默认获取英文保存路径
            savePath_en_base = current_dir1 + '/'
        else:
            savePath_en_base = current_dir1.replace('/python', '') + config[3]

        to_result = get_word_from_file(wait_translate_path, savePath_cn, savePath_en)
        if to_result != '':
            save_file(to_result, savePath_en_base, suffix='bug.md')

        print('\n')
        check_key_repeat(savePath_cn)
        check_key_repeat(savePath_en)
        check_key_repeat(savePath_en_base)

