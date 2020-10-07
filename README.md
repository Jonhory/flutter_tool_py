# flutter_tool_py

针对Flutter工程的一些py脚本

## `translate`文件夹 -- 针对`i18n`,`Intl`等配套使用
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


* 举个🌰(具体可查看相关文件内容):

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
python3 ***/Desktop/PythonProjects/translate.py
```

或者生成程序，以后双击使用即可。

python脚本生成应用`pyinstaller -F translate.py`,生成完成后放在同级目录下，双击程序运行。

* 可自行修改源码发挥空间
	* 待翻译语言可以修改为任何语言
	* 待翻译结果可以修改为任何语言


## `handleImages`文件夹--处理图片

* 在开发中如果使用`png`图片时，会遇到在`iOS`下使用`@2x`、`@3x`图片资源的问题，从蓝湖上下载出来的图片名称往往都是各种乱七八糟的名称以及处于同级文件夹下。在`flutter`项目中，我们想要使用这种图片，就需要手动修改名称，然后移动到对应的`2.0x`、`3.0x`文件夹下，该脚本为解决此问题而生。ps.使用`svg`、`webp`格式更好～

* ⚠️不要直接运行在已处理好的文件夹下，因为会重命名所有该路径下的图片文件。

* 举个🌰(具体可查看相关文件内容)
	* `test/source`文件夹
	
	```
	点赞.png
	点赞@2x.png
	点赞@3x.png
	高清.png
	高清@2x.png
	高清@3x.png
	回放.png
	回放@2x.png
	回放@3x.png
	```

	* 运行之后效果如`images`文件夹

	```
	2.0x
	2.0x/test_0.png
	2.0x/test_1.png
	2.0x/test_2.png
	3.0x
	3.0x/test_0.png
	3.0x/test_1.png
	3.0x/test_2.png
	test_0.png
	test_1.png
	test_2.png
	```
	
* 使用方法1⃣️
	* 将`handleImages/handleImages/dist/handleImages`程序复制到对应的图片文件夹内，双击运行

```
Last login: Wed Oct  7 16:21:20 on ttys000
***/flutter_tool_py/handleImages/test/images/handleImages ; exit;
☁  ~  ***/flutter_tool_py/handleImages/test/images/handleImages ; exit;
Please enter the picture name prefix required:test
Current folder path: ***/flutter_tool_py/handleImages/test/images
===>>> change_name finish , count == 3

[进程已完成]
```


* 使用方法2⃣️
	* 命令行运行脚本
```
 python3 handleImages.py [图片文件夹路径] [图片前缀]
```

* 可自行修改源码发挥空间
	* 结合翻译脚本相关方法，可以将图片名称从中文转为对应的英文