# ============================================================
# mypackage/models.py 数据模型模块
# ============================================================

class User:
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def __repr__(self):
        return f"User({self.uid}, {self.name})"
