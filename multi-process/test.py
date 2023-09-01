#!/user/bin/env python

import os
import multiprocessing

def child_process():
    print(f"Hi! I'm a child procss {os.getpid()}")

# A very very simple process.
if __name__ == "__main__":
    print(f"Hi! I'm procss {os.getpid()}")

    # Here we create a new instance of the Process class and assign our
    # `chils_process` function to be excuted.
    process = multiprocessing.Process(target=child_process)
    
    # We then start the process
    process.start()

    # And finally, we join the process. This will make our script to hang and
    # wait until the child process is done.
    process.join()

