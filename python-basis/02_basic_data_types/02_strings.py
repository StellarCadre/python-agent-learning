# ============================================================
# 字符串 str 全面讲解
# ============================================================
# Go 的字符串：string，用双引号，UTF-8 编码，不可变
# Python 的字符串：str，单双引号都行，Unicode 编码，不可变
#
# Python 字符串功能比 Go 丰富很多，Agent 开发中处理 prompt、
# 解析模型输出都离不开字符串，务必熟练。
# ============================================================

# ---------- 1. 字符串的多种声明方式 ----------

s1 = "双引号字符串"
s2 = '单引号字符串'                  # 和双引号完全等价
s3 = """三引号字符串
可以跨多行
保留换行和缩进"""
s4 = '''单引号三引号
也可以跨多行'''

# 单双引号嵌套时不用转义
s5 = "It's a pen"                   # 双引号包单引号
s6 = '他说"你好"'                    # 单引号包双引号

# 转义字符（和 Go 类似）
s7 = "第一行\n第二行"                # \n 换行
s8 = "制表符\t分隔"                  # \t 制表符
s9 = "引号\"引号"                    # \" 转义双引号
s10 = "路径\\文件夹\\文件"           # \\ 反斜杠
s11 = "回车\r覆盖"                   # \r 回车
print("转义操作结果\n",s7, s8, s9, s10, s11)

# 原始字符串：r 开头，转义字符不生效（常用于正则、文件路径）
path = r"C:\Users\Desktop\new.txt"  # \n 不会被解释成换行
print(path)
# Go 中反引号字符串 `...` 就是原始字符串，Python 用 r"..."

# ---------- 2. f-string 格式化（最常用，必须掌握）----------

name = "Tom"
age = 18
height = 1.75

# 基本用法：在字符串前加 f，用 {} 包裹变量或表达式
print(f"我叫{name}，今年{age}岁")
print(f"明年我{age + 1}岁")          # {} 里可以放表达式
print(f"身高{height}米")
print(f"身高{height:.2f}米")         # 保留2位小数 1.75
print(f"名字是{name:>10}|结束")      # 右对齐，宽度10
print(f"名字是{name:<10}|结束")      # 左对齐
print(f"名字是{name:^10}|结束")      # 居中
print(f"百分比{0.85:.1%}")           # 百分比格式 85.0%

# Python 3.8+ 支持 = 自动打印变量名和值（调试很方便）
print(f"{name=}")                   # name='Tom'
print(f"{age=}")                    # age=18

# 其他格式化方式（了解，老代码可能遇到）
print("我叫%s，今年%d岁" % (name, age))           # % 格式化（类似 C 语言，老写法）
print("我叫{}，今年{}岁".format(name, age))        # str.format()（较老写法）
print("我叫{0}，{0}今年{1}岁".format(name, age))  # format 带索引

# ---------- 3. 字符串拼接与重复 ----------

# 拼接
greeting = "你好" + "，" + "世界"     # + 拼接（Go 也用 +）
print(greeting)

# join 拼接（推荐，尤其拼接列表中的多个字符串）
words = ["Python", "Agent", "开发"]
result = " ".join(words)             # 用空格连接
print(result)                        # Python Agent 开发
print("-".join(words))               # Python-Agent-开发
# 坑：join 只能拼接字符串列表，如果有数字要先转 str
nums = [1, 2, 3]
print(",".join(str(n) for n in nums))

# 字符串重复
print("=" * 30)                      # 重复30次，打印分隔线很方便
print("哈" * 3)                      # 哈哈哈

# ---------- 4. 字符串常用方法（全面）----------

s = "  Hello, Python World  "

# --- 大小写相关 ---
print(s.upper())                     # 全部转大写
print(s.lower())                     # 全部转小写
print("hello world".title())         # 每个单词首字母大写 Hello World
print("hello world".capitalize())    # 首字母大写 Hello world
print(s.swapcase())                  # 大小写互换

# --- 去除空白 ---
print(s.strip())                     # 去除两端空白（最常用，类似 Go 的 strings.TrimSpace）
print(s.lstrip())                    # 只去左边
print(s.rstrip())                    # 只去右边
print("===hello===".strip("="))     # 去除指定字符

# --- 查找与判断 ---
print("hello world".find("world"))   # 查找子串位置，返回索引10，找不到返回 -1
print("hello world".find("xyz"))     # -1
print("hello world".index("world"))  # 类似 find，但找不到会抛异常 ValueError
print("hello world".count("l"))      # 统计子串出现次数 3
print("hello world".startswith("he"))  # 是否以...开头 True
print("hello world".endswith("ld"))    # 是否以...结尾 True
print("hello".isalpha())             # 是否全是字母 True
print("123".isdigit())               # 是否全是数字 True
print("hello123".isalnum())          # 是否全是字母或数字 True
print("   ".isspace())               # 是否全是空白 True
print("HELLO".isupper())             # 是否全大写
print("hello".islower())             # 是否全小写

# --- 替换与分割 ---
print("hello world".replace("world", "python"))  # 替换,将world替换为python
print("a-b-c-d".replace("-", "_", 2))            # 只替换前2个

parts = "a,b,c,d".split(",")         # 按分隔符分割成列表
print(parts)                         # ['a', 'b', 'c', 'd']
print("a,b,c".split(",", maxsplit=1))  # 只分割1次 ['a', 'b,c']

lines = "第一行\n第二行\n第三行".splitlines()  # 按行分割
print(lines)

# partition：分成 (前, 分隔符, 后) 三部分
print("hello:world".partition(":"))  # ('hello', ':', 'world')

# --- 填充对齐 ---
print("42".zfill(5))                 # 零填充到5位 00042
print("hello".center(11, "-"))       # 居中填充 ---hello---
print("hello".ljust(10, "."))        # 左填充 hello.....
print("hello".rjust(10, "."))        # 右填充 .....hello

# ---------- 5. 字符串索引与切片 ----------
# 字符串是序列，支持和 list 一样的索引和切片（字符串不可变，不能通过索引修改）

text = "Python"
print(text[0])                       # 第一个字符 P
print(text[-1])                      # 最后一个字符 n
print(text[0:3])                     # 切片 Pyt（左闭右开，索引0,1,2）
print(text[:4])                      # Pyth（从头开始）
print(text[2:])                      # thon（到末尾）
print(text[-3:])                     # hon（最后3个字符）
print(text[::2])                     # Pto（步长2，隔一个取一个）
print(text[::-1])                    # nohtyP（反转字符串，常用技巧）

# text[0] = "J"   # 报错！字符串不可变（和 Go 字符串一样不可变）
# 想要修改只能创建新字符串
new_text = "J" + text[1:]
print(new_text)                      # Jython

# ---------- 6. len 与成员判断 ----------

print(len(text))                     # 长度 6（Go 用 len()）
print("yth" in text)                 # True，判断子串是否包含
print("xyz" not in text)             # True

# ---------- 7. 字符串编码 ----------
# Python 3 字符串是 Unicode，需要和字节串 bytes 互转（网络/文件场景）

# str -> bytes（编码）
byte_data = "你好".encode("utf-8")
print(byte_data)                     # b'\xe4\xbd\xa0\xe5\xa5\xbd'

# bytes -> str（解码）
str_data = byte_data.decode("utf-8")
print(str_data)                      # 你好

# 坑：解码时编码不一致会乱码或报错
# byte_data.decode("gbk")   # 用 gbk 解 utf-8 会乱码或 UnicodeDecodeError


# ============================================================
# 【扩展】字符串编码与解码原理详解
# ============================================================
# 一、根本矛盾：计算机只认识字节，不认识文字
# ------------------------------------------------------------
# 计算机的世界里只有二进制，最小存储/传输单位是"字节"（8位，0~255）。
# 但人要处理的是 "你"、"好"、"A"、"😀" 这些文字。
# 文字没法直接存进电脑，必须有一套规则把文字翻译成数字。
# 这个翻译分两层：
#
#    文字          第一层            第二层
#   "你"   ──→   码点 U+4F60   ──→   字节 E4 BD A0
#         字符集(Unicode)         编码(UTF-8)
#         解决"编号是多少"         解决"编号怎么存成字节"
#
# ============================================================
# 二、第一层：字符 → 码点（Unicode 干的事）
# ------------------------------------------------------------
# Unicode 是一张超大的"世界字符总表"，给地球上每一个字符发一个
# 唯一编号，叫"码点（Code Point）"，写成 U+XXXX：
#
#   字符    Unicode 码点
#   你      U+4F60
#   好      U+597D
#   A       U+0041
#
# 注意：Unicode 只负责"编号"，它没规定这个编号怎么用字节存。
# ============================================================
# 三、第二层：码点 → 字节（UTF-8 干的事）
# ------------------------------------------------------------
# 码点是个数字，但怎么把它落成字节？这需要"编码方式（Encoding）"。
# UTF-8 是最常用的编码规则，特点是变长（1~4字节）：
#
#   字符    码点       UTF-8 字节      字节数
#   你      U+4F60     E4 BD A0        3
#   好      U+597D     E5 A5 BD        3
#   A       U+0041     41              1
#
# 规律：英文字符（ASCII 范围）只占 1 字节，中文占 3 字节，emoji 占 4 字节。
# ============================================================
# 四、关键区分：字符集 ≠ 编码（最容易混淆）
# ------------------------------------------------------------
#   字符集（Unicode）：规定"字符 ↔ 编号"，是一本字典
#   编码（UTF-8/UTF-16/GBK）：规定"编号 ↔ 字节"，是打包方式
#
# 同一个字符，用不同编码得到的字节完全不同（实测数据）：
#
#   字符    UTF-8        GBK
#   你      E4 BD A0     C4 E3
#   好      E5 A5 BD     BA C3
#
# GBK 是中文专用老编码，中文只占 2 字节（比 UTF-8 省 1 字节），
# 但不支持全世界文字。这就是为什么同一个 "你"，UTF-8 和 GBK 对不上。
# ============================================================
# 五、为什么网络/文件场景必须转 bytes（核心问题）
# ------------------------------------------------------------
# 两种环境能承载的数据形态不同：
#
#   场景              数据形态                  用什么类型
#   内存中(程序处理)   Unicode 文本，方便索引/     str
#                     算长度/切片/拼接
#   磁盘/网络          只能存/传"字节流"          bytes
#
# 磁盘上的文件、网线里传输的数据，本质都是一串字节，没有"文字"概念。
# 所以：
#
#   写入文件 / 发送请求：   str  ──encode()──→  bytes   （编码）
#   读取文件 / 接收响应：   bytes ──decode()──→  str    （解码）
#
# Go 里同理：string 底层是字节，[]byte(s) 转换、json.Marshal 都在做这层事。
# 只是 Python 把"内存用 Unicode、外部用 bytes"的区分做得更显式。
# ============================================================
# 六、Python 的两种类型
# ------------------------------------------------------------
#   text = "你好"                    # str：Unicode 文本（人看的）
#   data = b"\xe4\xbd\xa0"          # bytes：字节串（机器传的），b 开头
#
#   str 的元素是"字符/码点"
#   bytes 的元素是 0~255 的整数（b"\xe4" 就是数字 228）
# ============================================================
# 七、乱码是怎么来的
# ------------------------------------------------------------
# 编码和解码必须用同一套规则，就像寄件和开箱要用同一种语言：
#
#   byte_data = "你好".encode("utf-8")   # 用 UTF-8 编码
#   byte_data.decode("gbk")              # 却用 GBK 解码 → 乱码或报错
#
#   - UTF-8 的字节 E4 BD A0 被 GBK 按它自己的规则解读，拼成别的字 → 乱码
#   - 如果字节序列在目标编码里根本不合法 → 直接报 UnicodeDecodeError
#
# 这也解释了文件章节为什么反复强调：打开文件要写对 encoding="utf-8"，
# 因为写和读的编码不一致就会乱码。
# ============================================================
# 八、可运行验证示例
# ============================================================

# 8.1 查看字符的码点和各种编码的字节
for ch in "你好A":
    cp = ord(ch)                                 # ord() 取码点
    utf8_bytes = ch.encode("utf-8")
    gbk_bytes = ch.encode("gbk")
    print(f"字符 {ch} | 码点 U+{cp:04X} | "
          f"UTF-8 {utf8_bytes.hex(' ').upper()} | "
          f"GBK {gbk_bytes.hex(' ').upper()}")

# 8.2 编码 → 解码完整流程
original = "你好，世界"
encoded = original.encode("utf-8")               # str -> bytes
print("编码后 bytes:", encoded)
decoded = encoded.decode("utf-8")                # bytes -> str
print("解码后 str:", decoded)
print("是否还原:", original == decoded)

# 8.3 故意用错编码看乱码（注意：这里用 errors 避免崩溃，演示效果）
utf8_bytes = "你好".encode("utf-8")
# 用 gbk 解 utf-8 的字节：可能乱码，也可能报错
try:
    wrong = utf8_bytes.decode("gbk")
    print("用GBK解UTF-8的结果（乱码）:", wrong)
except UnicodeDecodeError as e:
    print("用GBK解UTF-8报错:", e)

# 8.4 注意：只有 bytes 才能 decode，str 不能 decode！
# str 要 encode 成 bytes，bytes 才能 decode 回 str。
demo_str = "模拟网络发来的数据"
demo_bytes = demo_str.encode("utf-8")            # 先编码（模拟网络传输的是字节）
demo_restored = demo_bytes.decode("utf-8")       # 再解码
print("还原:", demo_restored)

# ============================================================
# 一句话总结：
# Unicode 给每个字符一个编号（码点），UTF-8 决定编号怎么变成字节。
# 内存里程序用 Unicode 的 str 处理文字，磁盘和网络只认字节，
# 所以要 encode/decode 互转；编码解码规则不一致，就是乱码。
# ============================================================


