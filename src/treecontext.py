class TreeContext():

    def __init__(self, manager=None, ctx={}):
        self.parent = manager
        self.ctx = ctx

    def __call__(self, key: str):
        if not key in self.ctx:
            self.ctx[key] = {}

        return self.__class__(self, self.ctx[key])

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def get(self, attr, val0):

        if isinstance(attr, tuple):
            vals = val0 if isinstance(val0, tuple) else (val0,)
            return tuple(
                self.get(a, vals[i % len(vals)]) for i, a in enumerate(attr)
            )

        closest = self.closest(attr)
        if closest is not None:
            return closest.ctx[attr]

        self.ctx[attr] = val0

        return val0

    def closest(self, attr):

        if attr in self.ctx:
            return self

        if self.parent is not None:
            return self.parent.closest(attr)

        return None

    def set(self, attr, val):

        if isinstance(attr, tuple):
            vals = val if isinstance(val, tuple) else (val,)
            return tuple(
                self.set(a, vals[i % len(vals)])
                for i, a in enumerate(attr)
            )

        closest = self.closest(attr)
        closest = self if closest is None else closest
        closest.ctx[attr] = val

        return val
