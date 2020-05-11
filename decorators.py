class _Decorator:
    def __init__(self):
        self._func = None

    def _call(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __call__(self, func):
        self._func = func
        return self._call


class _DecoratorDecorator(_Decorator):
    def __init__(self, base: _Decorator = None):
        self._base = base
        super().__init__()

    def _call(self, *args, **kwargs):
        if self._base is None:
            return super()._call(*args, **kwargs)

        return self._base._call(*args, **kwargs)

    def __call__(self, func):
        self._func = func

        if self._base is not None:
            self._base.__call__(func)

        return self._call


class debug(_DecoratorDecorator):
    def _call(self, *args, **kwargs):
        print(f'DEBUG: name={self._func.__name__}')
        print(f'DEBUG: {args=}')
        print(f'DEBUG: {kwargs=}')

        result = super()._call(*args, **kwargs)

        print(f'DEBUG: {result=}')

        return result


class Tracker(_DecoratorDecorator):
    def __init__(self, base=None):
        super().__init__(base=base)
        self._calls = {}

    def _call(self, *args, **kwargs):
        result = super()._call(*args, **kwargs)
        call = {
            'args': args,
            'kwargs': kwargs,
            'return': result
        }
        if self._func.__name__ not in self._calls:
            self._calls[self._func.__name__] = [call]
        else:
            self._calls[self._func.__name__].append(call)

        return result

    def __getitem__(self, name):
        return self._calls[name]

    def __str__(self) -> str:
        return str(self._calls)

    def __iter__(self):
        return iter(self._calls)

track = Tracker()


class memoize(_DecoratorDecorator):
    def __init__(self, base: _Decorator = None):
        super().__init__(base)
        self.cache = {}

    def _call(self, *args, **kwargs):
        key = (tuple(args), tuple(sorted(kwargs.items())))
        if key in self.cache:
            return self.cache[key]

        result = super()._call(*args, **kwargs)
        self.cache[key] = result

        return result


@memoize(track)
def foo(x, y):
    return x + y

for _ in range(500000):
    foo(3, 5)

print(len(track['foo']))
