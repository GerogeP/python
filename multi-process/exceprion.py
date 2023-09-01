#!/user/bin/env python

import os
import multiprocessing

def child_process():
    print(f"Hi! I'm a child procss {os.getpid()}.")
    raise Exception("Oh no! :(")

# A very very simple process.
if __name__ == "__main__":
    print(f"Hi! I'm procss {os.getpid()}")

    # Here we create a new instance of the Process class and assign our
    # `chils_process` function to be excuted. Note the difference now that we
    # are using the `args` parameter now, this means that we can pass down
    # parameters to the function being excuted as a child process.
    process = multiprocessing.Process(target=child_process)
    
    try:
        # We then start the process
        process.start()

        # And finally, we join the process. This will make our script to hang and
        # wait until the child process is done.
        process.join()

        print("after chiled execution! right!")
    except Exception:
        print("Uhhhh... It failed?")

