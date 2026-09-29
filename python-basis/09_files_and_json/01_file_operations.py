# ============================================================
# 文件读写操作
# ============================================================
# Go 读写文件：os.Open, os.Create, ioutil.ReadFile, defer f.Close()
# Python 读写文件：open()，配合 with 自动关闭（推荐）。
#
# open(文件路径, 模式, encoding)
# 模式：
#   "r"  只读（默认，文件不存在报错）
#   "w"  写入（覆盖，文件不存在则创建）
#   "a"  追加（末尾添加，不存在则创建）
#   "r+" 读写
#   "rb"/"wb" 二进制模式（图片、音频等）
# ============================================================

import os

# ---------- 1. 写入文件 ----------

# with 语句：结束时自动关闭文件（即使异常也关闭），等价 Go 的 defer f.Close()
with open("demo.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")
    f.writelines(["第三行\n", "第四行\n"])   # 批量写入（不会自动加换行）

# 坑：
# 1. 必须指定 encoding="utf-8"，否则 Windows 默认 gbk，中文可能乱码
# 2. write 不会自动换行，需要自己写 \n
# 3. "w" 模式会清空原文件，小心覆盖

# ---------- 2. 读取文件 ----------

# 方式1：read() 读取全部内容为一个字符串
with open("demo.txt", "r", encoding="utf-8") as f:
    content = f.read()
print("全部内容:\n" + content)

# 方式2：readline() 逐行读取
with open("demo.txt", "r", encoding="utf-8") as f:
    first = f.readline()
    print("第一行:", first.strip())

# 方式3：readlines() 读取所有行到 list
with open("demo.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
print("行列表:", [l.strip() for l in lines])

# 方式4（推荐）：直接遍历文件对象，逐行读取，省内存
with open("demo.txt", "r", encoding="utf-8") as f:
    for line in f:
        print("行:", line.strip())

# 大文件一定要用逐行遍历，read() 会把整个文件读进内存

# ---------- 3. 追加内容 ----------

with open("demo.txt", "a", encoding="utf-8") as f:
    f.write("追加的一行\n")

# ---------- 4. 二进制文件读写 ----------
# 图片、视频、音频等用 rb/wb，不能指定 encoding（没有编码概念）

# with open("image.png", "rb") as f:
#     data = f.read()                  # bytes
# with open("copy.png", "wb") as f:
#     f.write(data)

# ---------- 5. 文件不存在的处理 ----------

try:
    with open("not_exist.txt", "r", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("文件不存在")

# ---------- 6. 文件/目录常用操作 ----------

# 判断存在
print(os.path.exists("demo.txt"))
print(os.path.isfile("demo.txt"))
print(os.path.isdir("."))

# 创建目录
os.makedirs("output/sub", exist_ok=True)   # exist_ok 已存在不报错

# 重命名/删除
# os.rename("demo.txt", "demo2.txt")
# os.remove("demo2.txt")
# os.rmdir("空目录")

# ---------- 7. pathlib 更现代的方式（推荐）----------

from pathlib import Path

# 写
Path("p_demo.txt").write_text("pathlib写入\n第二行", encoding="utf-8")

# 读
text = Path("p_demo.txt").read_text(encoding="utf-8")
print(text)

# 路径拼接（跨平台，用 / 运算符）
data_file = Path("data") / "input" / "a.txt"
print(data_file)

# 遍历目录下某类文件
for py_file in Path(".").glob("*.txt"):
    print("找到:", py_file)

# ---------- 8. 实战小例子 ----------

# 例子1：统计文件信息
def analyze_file(path):
    p = Path(path)
    if not p.exists():
        return None
    text = p.read_text(encoding="utf-8")
    return {
        "name": p.name,
        "size": p.stat().st_size,
        "lines": len(text.splitlines()),
        "chars": len(text),
        "words": len(text.split()),
    }

print(analyze_file("demo.txt"))

# 例子2：批量处理目录下文件
def batch_process(folder, suffix=".txt"):
    folder = Path(folder)
    results = {}
    for file in folder.glob(f"*{suffix}"):
        content = file.read_text(encoding="utf-8")
        results[file.name] = len(content)
    return results

print(batch_process("."))

# 清理临时文件
for tmp in ["demo.txt", "p_demo.txt"]:
    if Path(tmp).exists():
        Path(tmp).unlink()
Path("output").rmdir()
Path("output/sub").rmdir()
