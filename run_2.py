# This is showcase of the ultimate goal of the library

import pandas as pd

import serverless_ray


def f1(open, close):
    return close-open


def f2(high, low):
    return high-low


def f3(f1, f2):
    return f1*f2


@serverless_ray.remote(num_cpus=10, num_gpus=1, memory_mb=512*1024)
def heavy_computation(factor_name):

    func = globals()[factor_name]
    data_to_load = get_arg_names(func)
    df = {}

    for data_name in data_to_load:
        df[data_name] = pd.read_s3(f"s3://data/{data_name}.csv")

    ret = func(**df)

    ret.to_s3(f"s3://data/{factor_name}.csv")

    return factor_name


if __name__ == "__main__":

    serverless_ray.config()

    args_list = ['f1', 'f2', 'f3']

    # Run the function, all function run in parallel
    with serverless_ray.start():
        heavy_computation.map(args_list)
