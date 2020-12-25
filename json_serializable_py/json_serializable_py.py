# -*- coding: utf-8 -*-

import json
import os

# 保存已处理的字典类型 ，用于过滤相同数据的重复处理 [{key: class_name, value: dict}]
written_dict_list = []
# 生成的类名是否采用简洁模式，如果是的话，需要注意检查结果，可能会漏生成在不同类具备同名的类
is_class_name_brief = True


# 读取源文件
def readfile(file_path, name='SourceBean'):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()
            js = json.dumps(content)
            resource = json.loads(js)

            data = json.loads(resource)

            # 通用头部
            to_result = ''

            if type(data) is dict:
                to_result = analysis_dict(data, to_result, name)
            elif type(data) is list:
                if (len(data)) > 0:
                    to_result = analysis_dict(data[0], to_result, name)

            print('🎉解析完成，正在准备保存...')
            return to_result
    except json.decoder.JSONDecodeError as e:
        print('错误！请检查数据源格式，非json!!!')
        print(e)
        return ''


# 解析字典类型
def analysis_dict(dic, result, class_name):
    if check_repeat_dic(dic)[0]:
        return result

    written_dict_list.append({'key': class_name, 'value': dic})

    result += '\nclass ' + class_name + ' {\n'

    result_list = analysis_one_dict(dic, result, class_name)
    result = result_list[0]
    other_list = result_list[1]
    result += '\n}\n'
    result = add_class_method(dic, result, class_name)

    for item in other_list:
        if type(item) is dict:
            for key, value in item.items():
                if type(value) is dict:
                    if is_class_name_brief:
                        result = analysis_dict(value, result, key.capitalize())
                    else:
                        result = analysis_dict(value, result, class_name + key.capitalize())

                elif type(value) is list:
                    if len(value) > 0:
                        if type(value[0]) is dict:
                            print('开始解析 ' + key)
                            if is_class_name_brief:
                                result = analysis_dict(value[0], result, key.capitalize())
                            else:
                                result = analysis_dict(value[0], result, class_name + key.capitalize())
                        else:
                            print('警告，此数据结构异常')

    return result


# 解析一个字典数据
def analysis_one_dict(dic, result, class_name):
    # 装 value = dict 或 list 的数据
    other_list = []

    if len(dic.items()) == 0:
        class_init = '  ' + class_name + '();\n'
        result += '\n' + class_init
        result = add_class_method_in(result, class_name)
        return [result, other_list]

    class_init = '  ' + class_name + '({\n'

    # 遍历字典 类型判断
    for k, v in dic.items():
        if type(v) == str:
            result += '  '
            result += 'String ' + k + ';\n'
        elif type(v) == int:
            result += '  '
            result += 'int ' + k + ';\n'
        elif type(v) == float:
            result += '  '
            result += 'double ' + k + ';\n'
        elif type(v) == bool:
            result += '  '
            result += 'bool ' + k + ';\n'
        elif v is None:
            result += '  '
            result += 'String ' + k + ';\n'
        elif type(v) is dict:
            result += '  '
            check = check_repeat_dic(v)
            if check[0]:
                if is_class_name_brief:
                    result += check[1] + ' ' + k + ';\n'
                else:
                    result += class_name + check[1] + ' ' + k + ';\n'
            else:
                if is_class_name_brief:
                    result += k.capitalize() + ' ' + k + ';\n'
                else:
                    result += class_name + k.capitalize() + ' ' + k + ';\n'

            other_list.append({k: v})
        elif type(v) is list:
            result += '  '

            # 数组长度大于0
            if len(v) > 0:
                # 判断数组内部数据类型
                # List<Map>
                if type(v[0]) is dict:
                    check = check_repeat_dic(v[0])
                    if check[0]:
                        if is_class_name_brief:
                            result += 'List<' + check[1] + '> ' + k + ';\n'
                        else:
                            result += 'List<' + class_name + check[1] + '> ' + k + ';\n'
                    else:
                        if is_class_name_brief:
                            result += 'List<' + k.capitalize() + '> ' + k + ';\n'
                        else:
                            result += 'List<' + class_name + k.capitalize() + '> ' + k + ';\n'

                    other_list.append({k: v})

                # List<str>
                elif type(v[0]) is str:
                    result += 'List<String> ' + k + ';\n'
                # List<int>
                elif type(v[0]) is int:
                    result += 'List<int> ' + k + ';\n'
                elif type(v[0]) == float:
                    result += 'List<double> ' + k + ';\n'
                elif type(v[0]) == bool:
                    result += 'List<bool> ' + k + ';\n'
                else:
                    result += 'List ' + k + ';\n'
            else:
                result += 'List ' + k + ';\n'

        else:
            print(k, '========', v)
            print(type(v))

        class_init += '    this.' + k + ',\n'

    class_init += '  });\n'
    result += '\n' + class_init

    result = add_class_method_in(result, class_name)

    return [result, other_list]


# 增加类方法
def add_class_method_in(result, class_name):
    result += '\n'
    result += '  factory ' + class_name + '.fromJson(Map<String, dynamic> json) =>\n'
    result += '    _$' + class_name + 'FromJson(json);\n'
    result += '\n'
    result += '  Map<String, dynamic> toJson() => _$' + class_name + 'ToJson(this);\n'
    return result


# 实现类方法
def add_class_method(dic, result, class_name):
    result += '\n'
    result += class_name + ' ' + '_$' + class_name + 'FromJson(Map<String, dynamic> json) {\n'
    result += '  return ' + class_name + '(\n'

    for k, v in dic.items():
        v_type = 'String'
        type_v = type(v)
        if type_v is list:
            # 数组长度大于0
            if len(v) > 0:
                if type(v[0]) is dict:
                    if is_class_name_brief:
                        v_type = k.capitalize()
                    else:
                        v_type = class_name + k.capitalize()
                    result += '    ' + k + ": (json['" + k + "'] as List)\n"
                    result += '        ' + '?.map((e) => e == null\n'
                    result += '            ' + '? null\n'
                    result += '            ' + ': ' + v_type + '.fromJson(e as Map<String, dynamic>))\n'
                    result += '        ' + '?.toList(),\n'
                elif type(v[0]) is str:
                    result += '    ' + k + ": (json['" + k + "'] as List)\n"
                    result += '        ' + '?.map((e) => e as String)?.toList(),\n'
                elif type(v[0]) is int:
                    result += '    ' + k + ": (json['" + k + "'] as List)\n"
                    result += '        ' + '?.map((e) => e as int)?.toList(),\n'
                elif type(v[0]) is float:
                    result += '    ' + k + ": (json['" + k + "'] as List)\n"
                    result += '        ' + '?.map((e) => e as double)?.toList(),\n'
                elif type(v[0]) is bool:
                    result += '    ' + k + ": (json['" + k + "'] as List)\n"
                    result += '        ' + '?.map((e) => e as bool)?.toList(),\n'

            else:
                result += '    ' + k + ": (json['" + k + "'] as List)\n"
                result += '        ' + '?.map((e) => e as String)?.toList(),\n'
            continue

        if type_v is dict:
            if is_class_name_brief:
                v_type = k.capitalize()
            else:
                v_type = class_name + k.capitalize()
            result += '    ' + k + ": json['" + k + "'] == null\n"
            result += '        ' + '? null\n'
            result += '        ' + ': ' + v_type + '.fromJson(\n'
            result += '            ' + "json['" + k + "'] as Map<String, dynamic>),\n"
            continue

        if type_v is int:
            v_type = 'int'
        elif type_v is float:
            v_type = 'double'
        elif type_v is bool:
            v_type = 'bool'
        result += "    " + k + ": json['" + k + "']" + ' as ' + v_type + ',\n'

    result += '  );\n}\n'

    result += '\n'
    result += 'Map<String, dynamic> _$' + class_name + 'ToJson(\n'
    result += '        ' + class_name + ' instance) =>\n'
    result += '    <String, dynamic>{\n'

    for k, _ in dic.items():
        result += "      '" + k + "': instance." + k + ',\n'

    result += '    };\n'
    result += '\n'

    return result


# 查重
def check_repeat_dic(dic):
    for _dic in written_dict_list:
        # 差集
        differ = set(_dic['value'].keys()) - set(dic.keys())
        if len(differ) == 0 and len(_dic['value'].keys()) > 0:
            print('重复的类：%s' % _dic['key'])
            return [True, _dic['key']]
    return [False, '']


# 保存文件
def save_file(content, path_save, suffix):
    if content == '':
        return
    p = os.path.split(path_save)
    file = p[1].split('.')[0]
    new_file = p[0] + "/" + file + suffix
    if not os.path.exists(p[0] + "/"):
        try:
            os.makedirs(p[0])
        except FileExistsError:
            path_save = input('⚠️文件名重复，请重新输入保存的文件路径：')
            save_file(content, path_save, suffix)
            return

    with open(new_file, "w", encoding="utf-8") as f:
        f.write(content)
        print('🎉保存成功：', new_file)


def input_source_path():
    source_path = input('请输入json数据源文件路径：')
    if source_path == '':
        input_source_path()
    else:
        if not os.path.isfile(source_path):
            print('❌源文件路径错误:', source_path)
            input_source_path()
        else:
            return source_path


if __name__ == "__main__":

    is_test = True
    if is_test:
        bean_name = input('请输入最外层的类名（默认请直接按回车）：')
        if bean_name == '':
            bean_name = 'Result'
        print('bean_name = ', bean_name)

        file_result = readfile(os.path.dirname(__file__) + '/json_example', bean_name)
        if is_class_name_brief:
            result_name = 'result_brief.txt'
        else:
            result_name = 'result.txt'
        save_file(file_result, os.path.dirname(__file__) + '/', result_name)
    else:
        bean_name = input('请输入最外层的类的文件名（默认请直接按回车）：')
        path = input_source_path()
        save_path = input('请输入保存文件路径（默认与源文件同级请直接按回车）：')
        if save_path == '':
            save_path = os.path.dirname(path)
        if save_path[-1] != '/':
            save_path += '/'

        # 获取运行时目录
        # current_dir1 = os.path.dirname(sys.executable)
        # current_dir1 = os.path.dirname(__file__)

        if bean_name == '':
            file_result = readfile(path)
            save_file(file_result, save_path, 'jsonBean.dart')
        else:
            file_result = readfile(path, bean_name)
            save_file(file_result, save_path, bean_name)
