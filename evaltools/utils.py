from timeit import default_timer as timer
import pypapi
from pypapi import events, papi_high as high
import warnings


def papi_event_exists(event):
    """
    Helper function to check if a papi event exists.
    :param event: papi event to be checked.
    :return: (bool) True, if event exists.
    """
    try:
        high.start_counters([event])
        return True
    except pypapi.exceptions.PapiNoEventError:
        return False


def runtime(show=True):
    """
    Decorator function which measures the runtime of the decorated function and prints it to
    stdout.
    If the decorated function contains a dictionary passed via the keyword parameter "log_time",
    then the result is saved in there.
    :param show: (bool) True if the runtime is supposed to be printed to stdout.
    :return: Decorated function.
    """
    def eval_runtime(func):
        def timed(*args, **kwargs):
            kkwargs = kwargs.copy()
            try:
                kkwargs.pop("log_time")
            except:
                pass

            start = timer()
            result = func(*args, **kkwargs)
            elapsed = timer() - start
            if show:
                print("{}\tRUNTIME: {:.2f} ms".format(func.__name__, elapsed*1000))
            if "log_time" in kwargs:
                kwargs["log_time"][func.__name__] = elapsed * 1000
            return result
        return timed
    return eval_runtime


def flops(show=True):
    """
    Decorator function which measures the FLOPs used by the decorated function and prints it to
    stdout.
    If the kernel does not support this functionality, a warning is printed and the
    function is simply executed.
    If the decorated function contains a dictionary passed via the keyword parameter "log_flops",
    then the result is saved in there.
    :param show: (bool) True if the number of FLOPs are supposed to be printed to stdout.
    :return: Decorated function.
    """
    def eval_flops(func):
        def floped(*args, **kwargs):
            kkwargs = kwargs.copy()
            try:
                kkwargs.pop("log_flops")
            except:
                pass
            if papi_event_exists(events.PAPI_DP_OPS):
                high.start_counters([events.PAPI_DP_OPS])
                result = func(*args, **kkwargs)
                flops = high.start_counters()
                if "log_flops" in kwargs:
                    kwargs["log_flops"][func.__name__] = flops
                if show:
                    print("{}\tFLOPS: {}".format(func.__name__, flops))
                return result
            else:
                warnings.warn("Event (events.PAPI_DP_OPS) does not exist. Your kernel might not "
                              "support this function. Function {} is executed without FLOP "
                              "counting.".format(func.__name__))
                return func(*args, **kkwargs)
        return floped
    return eval_flops
