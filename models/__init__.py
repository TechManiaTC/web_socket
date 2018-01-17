import json

from utils import log


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


class Model(object):
    """
    Model 是所有 model 的基类
    @classmethod 是一个套路用法
    例如
    user = User()
    user.db_path() 返回 User.txt
    """

    def __init__(self, form):
        # self.id = None
        self.id = form.get('id', None)


    @classmethod
    def db_path(cls):
        """
        cls 是类名, 谁调用的类名就是谁的
        classmethod 有一个参数是 class(这里我们用 cls 这个名字)
        所以我们可以得到 class 的名字
        """
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # m 是 dict, 用 cls.new(m) 可以初始化一个 cls 的实例
        # 不明白就 log 大法看看这些都是啥
        log('before cls.new', models)
        ms = [cls.new(m) for m in models]
        return ms

    @classmethod
    def new(cls, form):
        # User.txt(form)
        # User.txt.__init__(form)
        m = cls(form)
        # log('user new', m)
        return m

    @staticmethod
    def valid_kwargs(model, kwargs):
        # 抽取公共部分
        exist = False
        for k, v in kwargs.items():
            if hasattr(model, k) and v == getattr(model, k):
                exist = True
            else:
                exist = False
        return exist

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='test1')
        """
        log('kwargs, ', kwargs)
        for m in cls.all():
            valid = cls.valid_kwargs(m, kwargs)
            if valid:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='test1')
        """
        log('kwargs, ', kwargs)
        models = []
        for m in cls.all():
            valid = cls.valid_kwargs(m, kwargs)
            if valid:
                models.append(m)
        return models

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        log('debug save')
        models = self.all()
        log('models', models)

        if self.id is None:
            log('self id is none')
            if len(models) == 0:
                self.id = 1
            else:
                self.id = models[-1].id + 1
            models.append(self)
        else:
            log('self id is not none')
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)
