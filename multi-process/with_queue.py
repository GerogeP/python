#!/user/bin/env python

import os
import multiprocessing

def child_process(queue, n1,n2):
    print(f"Hi! I'm a child procss {os.getpid()}. I do calculations.")
    sum = n1+ n2

    # Putting data into the queue
    queue.put(sum)

# A very very simple process.
if __name__ == "__main__":
    print(f"Hi! I'm procss {os.getpid()}")

    # Defining a new Queue()
    queue = multiprocessing.Queue()

    # Here we create a new instance of the Process class and assign our
    # `chils_process` function to be excuted. Note the difference now that we
    # are using the `args` parameter now, this means that we can pass down
    # parameters to the function being executed as a child process.
    process = multiprocessing.Process(target=child_process, args=(queue, 1,2))
    
    # We then start the process
    process.start()

    # And finally, we join the process. This will make our script to hang and
    # wait until the child process is done.
    process.join()

    # Accessing the result from the queue.
    print(f"Got the result from child process as {queue.get()}")
    
