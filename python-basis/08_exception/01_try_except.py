# ============================================================
# 异常处理 try / except / else / finally
# ============================================================
# Go 的错误处理哲学：函数返回 error，显式判断
#   result, err := doSomething()
#   if err != nil { return err }
#
# Python 的错误处理哲学：出错就抛出（raise）异常，用 try/except 捕获。
# 不捕获异常会导致程序崩溃并打印调用栈。
#
# Agent 调用网络、模型、文件时可能出现各种错误，必须处理异常。
# ============================================================

# ---------- 1. 最基本的 try/except ----------

try:
    num = int("abc")                # 这里会抛出 ValueError
    print("不会执行到这")
except ValueError:
    print("捕获到值错误：无法转换")

# ---------- 2. 捕获多种异常 ----------

# 方式1：多个 except 分别处理
def parse_value(text):
    try:
        return int(text)
    except ValueError:
        print("不是整数")
    except TypeError:
        print("类型错误（比如传了 None）")

parse_value("abc")
parse_value(None)

# 方式2：一个 except 捕获多种异常（元组）
try:
    value = d["missing"]
except (ValueError, KeyError, TypeError) as e:
    print("捕获多种异常之一:", type(e).__name__, e)

# as e 把异常对象绑定到变量 e，可以查看错误信息

# ---------- 3. 异常对象的信息 ----------

try:
    [1, 2, 3][10]
except IndexError as e:
    print("错误类型:", type(e).__name__)
    print("错误信息:", str(e))
    print("错误参数:", e.args)

# ---------- 4. else：没有异常时执行 ----------

def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("不能除以0")
    else:
        # 只有 try 成功才执行，放这里让 try 块尽量短（只包裹可能出错的代码）
        print(f"结果是 {result}")
        return result

safe_divide(10, 2)
safe_divide(10, 0)

# ---------- 5. finally：无论是否异常都执行 ----------

def read_demo():
    try:
        print("尝试操作")
        return "正常返回"
    except Exception:
        print("异常")
    finally:
        # 即使 try 里有 return，finally 也会执行！
        print("清理资源（关闭文件/连接）")

print(read_demo())

# finally 常用于释放资源（文件、数据库连接、锁）

# ---------- 6. 完整结构执行顺序 ----------

def full_demo(x):
    print("---")
    try:
        result = 10 / x
    except ZeroDivisionError:
        print("except: 除以0")
    else:
        print("else: 结果", result)
    finally:
        print("finally: 结束")

full_demo(2)                         # try成功 -> else -> finally
full_demo(0)                         # 异常 -> except -> finally

# ---------- 7. 捕获顺序：从具体到宽泛 ----------
# 异常匹配从上到下，先写具体异常，最后才写兜底的 Exception

try:
    int(None)
except ValueError:
    print("值错误")
except TypeError:
    print("类型错误")
except Exception as e:               # 兜底捕获（要放最后）
    print("其他异常:", e)

# 坑：不要裸 except:（不写异常类型），它会连键盘中断等都捕获
# 也不要一上来就 except Exception 吞掉所有错误，应该针对性捕获

# ---------- 8. 抛出异常 raise ----------

def set_age(age):
    if not isinstance(age, int):
        raise TypeError("年龄必须是整数")
    if age < 0:
        raise ValueError("年龄不能为负")
    return age

try:
    set_age(-1)
except ValueError as e:
    print("捕获:", e)

# raise 单独使用：在 except 中重新抛出（异常链/记录后继续传播）
def rethrow_demo():
    try:
        int("abc")
    except ValueError:
        print("记录日志后重新抛出")
        raise                          # 重新抛出当前异常

# rethrow_demo()

# ---------- 9. 异常链 raise ... from ----------

def fetch_config():
    try:
        with open("missing.json") as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError("配置文件读取失败") from e
# from 保留原始异常因果关系（调试能看到 During handling...）

# ---------- 10. 常见内置异常类型 ----------
#
# 异常名             触发场景
# ValueError         值不合法（int("abc")）
# TypeError          类型不对（1 + "a"）
# KeyError           dict 的 key 不存在
# IndexError         list/tuple 索引越界
# AttributeError     属性/方法不存在
# NameError          变量未定义
# FileNotFoundError  文件不存在
# ZeroDivisionError  除以0
# NotImplementedError 抽象方法/未实现
# RuntimeError       一般运行时错误
# ImportError        导入失败（ModuleNotFoundError 是子类）
# OSError            系统/IO错误
# StopIteration      迭代器结束
# AssertionError     assert 断言失败
#
# 不需要背，遇到报错看异常类型即可

# ---------- 11. assert 断言 ----------
def divide(a, b):
    assert b != 0, "除数不能为0"      # 条件为False抛 AssertionError
    return a / b

print(divide(10, 2))
# 注意：python -O 模式下 assert 会被移除，不要用 assert 做业务校验，
# 业务校验应该用 if + raise

# ---------- 12. 实战小例子 ----------

# 例子1：健壮的 API 参数解析
def parse_int_param(value, name, min_v=None, max_v=None, default=None):
    if value is None:
        return default
    try:
        result = int(value)
    except (ValueError, TypeError):
        raise ValueError(f"参数 {name} 必须是整数，收到: {value}")
    if min_v is not None and result < min_v:
        raise ValueError(f"参数 {name} 不能小于 {min_v}")
    if max_v is not None and result > max_v:
        raise ValueError(f"参数 {name} 不能大于 {max_v}")
    return result

print(parse_int_param("25", "age", 0, 150))

# 例子2：重试装饰器雏形（Agent 调用模型常用）
import time

def with_retry(max_retries=3, exceptions=(Exception,)):
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    print(f"第{attempt}次失败: {e}")
                    if attempt < max_retries:
                        time.sleep(0.1 * attempt)
            raise last_error
        return wrapper
    return decorator

call_count = 0
@with_retry(max_retries=3)
def unstable_api():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError("网络波动")
    return "成功"

print(unstable_api())
