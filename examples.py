from evaltools.utils import runtime, flops


def loop(n):
    a = 0
    for i in range(n):
        a += 1


@runtime(show=True)
def test0(n):
    loop(n)


@runtime(True)
def test1(n):
    loop(n)


@runtime(False)
def test2(n):
    loop(n)


@flops(True)
def test3(n):
    loop(n)


# @flops(False)
def test4(n):
    loop(n)


if __name__ == "__main__":
    test0(1000)

    for n in [100, 1000, 100000, 1000000]:
        for test in [test1, test2, test3, test4]:
            test(n)

    log_time = {}
    test1(n, log_time=log_time)
    print(log_time)

    log_flops = {}
    test3(n, log_flops=log_flops)
    print(log_flops)