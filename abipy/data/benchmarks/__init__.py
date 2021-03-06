from __future__ import division, print_function


def bench_main(main):
    """
    This decorator is used to decorate main functions producing `AbinitFlows`.
    It adds the initialization of the logger and an argument parser that allows one to select 
    the loglevel, the workdir of the flow as well as the YAML file with the parameters of the `TaskManager`.
    The main function shall have the signature:

        main(options)

    where options in the container with the command line options generated by `ArgumentParser`.

    Args:
        main:
            main function.
    """
    from functools import wraps

    @wraps(main)
    def wrapper(*args, **kwargs):
        import argparse
        parser = argparse.ArgumentParser()

        parser.add_argument('--loglevel', default="ERROR", type=str,
                            help="set the loglevel. Possible values: CRITICAL, ERROR (default), WARNING, INFO, DEBUG")

        parser.add_argument("-w", '--workdir', default="", type=str, help="Working directory of the flow.")

        parser.add_argument("-m", '--manager', default="", type=str,
                            help="YAML file with the parameters of the task manager")

        parser.add_argument("--mpi-range", type=str, default="(1,3,1)", help="Range of MPI processors to test."
                            "'--mpi-range='(1,4,2)' performs benchmarks for mpi_procs in [1, 3]")

        parser.add_argument('--paw', default=False, action="store_true", help="Run PAW calculation if present")
        parser.add_argument('--paral_kgb', default=1, type=int, help="paral_kgb input variable")

        parser.add_argument("--sched", default=False, action="store_true", help="Scheduler or rapidfire mode")

        options = parser.parse_args()

        # loglevel is bound to the string value obtained from the command line argument. 
        # Convert to upper case to allow the user to specify --loglevel=DEBUG or --loglevel=debug
        import logging
        numeric_level = getattr(logging, options.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % options.loglevel)
        logging.basicConfig(level=numeric_level)

        # parse arguments
        if options.mpi_range is not None:
            import ast
            t = ast.literal_eval(options.mpi_range)
            assert len(t) == 3
            options.mpi_range = range(t[0], t[1], t[2])
            #print(lst(options.mpi_range))

        return main(options)

    return wrapper
