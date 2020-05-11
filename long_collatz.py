from decorators import *


@memoize
def length(n):
    if n == 1:
        return 1
    if n % 2 == 0:
        return 1 + length(n // 2)
    return 1 + length(3 * n + 1)


print(max(range(1, 1000000), key=length))

