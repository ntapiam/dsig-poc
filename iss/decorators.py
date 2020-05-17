import functools as fnt


def time_this(fn):
    @fnt.wraps(fn)
    def timed_fn(*args, **kwargs):
        import time

        start = time.time()
        x = fn(*args, **kwargs)
        stop = time.time()
        print(f"Time spent in {fn.__name__!r}: {stop-start} s")
        return x

    return timed_fn
