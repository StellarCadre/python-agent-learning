## 1. 创建环境

```
# 创建名为 agent 的环境，指定 Python 3.11（Agent 生态兼容性好）
conda create -n agent python=3.11 -y
```

> 环境会自动创建在 `C:\Software\Anaconda3\envs\agent` 下。 如果想装 Python 3.12，把 `python=3.11` 改成 `python=3.12` 即可。

## 2. 激活环境

```
conda activate agent
```

激活后命令行前缀会变成 `(agent)`，确认一下：

```
python --version
pip --version
```

## 3. （可选）升级 pip 并装基础工具

```
python -m pip install --upgrade pip
pip install ipython jupyter
```

## 常用环境管理命令（备查）

```
conda env list                    # 查看所有环境
conda deactivate                  # 退出当前环境
conda remove -n agent --all       # 删除整个环境
conda list                        # 查看当前环境已装包
```

创建好并激活后告诉我，我们再继续阶段 1 的学习。