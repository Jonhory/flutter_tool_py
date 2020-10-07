# flutter_tool_py

针对Flutter工程的一些py脚本

### `translate`文件夹 -- 针对`i18n`,`Intl`等配套使用
* 使用前请安装`python3`以及相关库

```
import hashlib
import random
import os
import requests
import sys
from urllib import parse
import json
from string import punctuation
```

* 翻译能力来自[百度翻译](https://api.fanyi.baidu.com/)
* `translate.py`脚本文件内`appid` 和 `secretKey` 获取自[百度翻译开放平台管理控制器](https://api.fanyi.baidu.com/api/trans/product/desktop?req=developer)
* 默认针对开发中常遇到的中文翻译为英文。


举个🌰(具体可查看相关文件内容):

待翻译内容为：

```
你好，世界！
这是一个翻译的小工具
```
运行结果：

```
<<*可选配置: /Config/translate_config*>> 
有效定义字段:
  1. path: 待翻译文件路径
  2. savePath_en: 英文保存路径（文件夹或文件，如果是文件就重写）
  3. savePath_cn: 中文保存路径（文件夹或文件，如果是文件就重写）
  4. savePath_en_base: 英文保存路径（文件夹或文件，如果是文件就重写）
Configuration information: {'savePath_en': '/lib/localization/strings_en_US.arb', 'savePath_cn': '/lib/localization/strings_zh.arb', 'savePath_en_base': '/lib/localization/strings_en.arb'}
Start translation...
Ready:【 你好，世界！ 】 to:  en
Translation completed  你好，世界！  >>>  Hello, world!
Ready:【 这是一个翻译的小工具 】 to:  en
Translation completed  这是一个翻译的小工具  >>>  This is a translation tool
Rewrite successful: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_zh.arb
Rewrite successful: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_en_US.arb
Translate finished >>> total:  2
Rewrite successful: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_en.arb


❌Please check if it is json data format: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_zh.arb
❌Please check if it is json data format: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_en_US.arb
❌Please check if it is json data format: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_en.arb
```

当文件内容不是`json`格式时，会提示`❌Please check if it is json data format:`,此时需要用户自行处理该文件，使其成为`json`格式数据。

例如首次运行后，`lib/localization/strings_zh.arb`内容为：

```
  "mHelloWorld": "你好，世界！",
  "mThisIsATranslation": "这是一个翻译的小工具"

```

此时需要用户处理为:

```
{
  "mHelloWorld": "你好，世界！",
  "mThisIsATranslation": "这是一个翻译的小工具"
}
```

下次有内容需要补充就不会有格式错误的提示了。

例如第二次待翻译内容为：

```
你好，世界！
这是一个翻译的小工具
你我皆凡人　生在人世间
终日奔波苦　一刻不得闲
```

运行结果：

```
<<*可选配置: /Config/translate_config*>> 
有效定义字段:
  1. path: 待翻译文件路径
  2. savePath_en: 英文保存路径（文件夹或文件，如果是文件就重写）
  3. savePath_cn: 中文保存路径（文件夹或文件，如果是文件就重写）
  4. savePath_en_base: 英文保存路径（文件夹或文件，如果是文件就重写）
Configuration information: {'savePath_en': '/lib/localization/strings_en_US.arb', 'savePath_cn': '/lib/localization/strings_zh.arb', 'savePath_en_base': '/lib/localization/strings_en.arb'}
Start translation...
Ready:【 你好，世界！ 】 to:  en
Translation completed  你好，世界！  >>>  Hello, world!
Ready:【 这是一个翻译的小工具 】 to:  en
Translation completed  这是一个翻译的小工具  >>>  This is a translation tool
Ready:【 你我皆凡人　生在人世间 】 to:  en
Translation completed  你我皆凡人　生在人世间  >>>  You and I are all mortals born in the world
Ready:【 终日奔波苦　一刻不得闲 】 to:  en
Translation completed  终日奔波苦　一刻不得闲  >>>  All day long, hard, no leisure
Rewrite successful: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_zh.arb
Rewrite successful: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_en_US.arb
Translate finished >>> total:  4
Rewrite successful: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_en.arb


Check the data path: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_zh.arb
Total valid data: 4
Raw data: 6
report:【 2 】Duplicate fields, please check the file path: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_zh.arb
repeat⚠️: ['mHelloWorld', 'mThisIsATranslation']
Check the data path: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_en_US.arb
Total valid data: 4
Raw data: 6
report:【 2 】Duplicate fields, please check the file path: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_en_US.arb
repeat⚠️: ['mHelloWorld', 'mThisIsATranslation']
Check the data path: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_en.arb
Total valid data: 4
Raw data: 6
report:【 2 】Duplicate fields, please check the file path: /Users/yaliang/Desktop/PythonProjects/lib/localization/strings_en.arb
repeat⚠️: ['mHelloWorld', 'mThisIsATranslation']
```

此时可以看到有重复的`key`警告信息，这是因为待翻译内容的翻译结果生成的`key`在结果中重复了。此时需要用户自行处理（例如是否需要两个同样的值，如果需要则手动修改重复的`key`，如果不需要，则手动删除多余的数据）。

检查数据完成之后即可复制相关内容到`flutter`项目内，或者配置文件和脚本直接放在`flutter`项目内，配置文件路径写为正确路径，配合相关插件能力即可立刻使用。

#### 使用指南

1.将`wait_translate`文件、`Config`文件夹、`translate.py`放在同一路径下。

2.将需要翻译的中文写入`wait_translate`文件内。

3.直接命令行运行

```
python3 /Users/yaliang/Desktop/PythonProjects/translate.py
```

或者生成程序，以后双击使用即可。

python脚本生成应用`pyinstaller -F translate.py`,生成完成后放在同级目录下，双击程序运行。

* 可自行修改源码发挥空间
	* 待翻译语言可以修改为任何语言
	* 待翻译结果可以修改为任何语言
