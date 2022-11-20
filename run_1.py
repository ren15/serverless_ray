# This is PoC of how the library are intended to be used 

import serverless_ray

@serverless_ray.remote
def heavy_computation(n):
    import time
    time.sleep(5)
    return n*2


if __name__ == "__main__":

    ## Connect to the serverless platform
    serverless_ray.config()

    ## Args to be passed to the function
    args_list = [1, 2, 3]

    ## Run the function, only wait for 5 seconds, instead of 15
    with serverless_ray.start():
        ret = heavy_computation.map(args_list)
    
    assert(ret == [2, 4, 6])
