from timeit import default_timer as timer
import pypapi
from pypapi import events, papi_high as high
import warnings


def runtime(show=True):
    """
    Decorator function which measures the runtime of the decorated function (in milliseconds) and
    prints it to stdout.
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
                print("{}\tRUNTIME [ms]:\t{:.4f}".format(func.__name__, elapsed*1000))
            if "log_time" in kwargs:
                kwargs["log_time"][func.__name__] = elapsed * 1000
            return result
        return timed
    return eval_runtime


def flops(show=True):
    """
    Decorator function which measures the FLOPs used by the decorated function and prints it to
    stdout. The function relies on the availability of the PAPI_DP_OPS event. If the kernel does
    not support this event, a warning is printed and the function is simply executed.
    If the decorated function contains a dictionary passed via the keyword parameter "log_flops",
    then the result is saved in there.
    :param show: (bool) True if the number of FLOPs are supposed to be printed to stdout.
    :return: Decorated function.
    """
    def eval_flops(func):
        def floped(*args, **kwargs):
            kkwargs = kwargs.copy()
            # check if the log_flops keyword is provided
            try:
                kkwargs.pop("log_flops")
            except:
                pass

            # if the event is available, do flop calculation & execute func
            try:
                high.start_counters([events.PAPI_DP_OPS])
                result = func(*args, **kkwargs)
                flops = high.stop_counters()[0]
                if "log_flops" in kwargs:
                    kwargs["log_flops"][func.__name__] = flops
                if show:
                    print("{}\tFLOPS:\t\t{}".format(func.__name__, flops))
                return result
            except pypapi.exceptions.PapiNoEventError as e:
                warnings.warn("{} \nYour kernel might not "
                              "support this function. Function {} is executed without FLOP "
                              "counting.".format(e, func.__name__))
                return func(*args, **kkwargs)
        return floped
    return eval_flops
