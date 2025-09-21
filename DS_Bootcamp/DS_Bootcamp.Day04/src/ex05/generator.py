import sys
import resource

def read_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line
    
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: <name_of_file>")
        sys.exit(1)

    try:
        lines = read_file(sys.argv[1])

        for line in lines:
            pass

        peak_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024**2
        user_time = resource.getrusage(resource.RUSAGE_SELF).ru_utime
        system_time = resource.getrusage(resource.RUSAGE_SELF).ru_stime
        
        print(f"Peak Memory Usage = {peak_mem} GB")
        print(f"User Mode Time + System Mode Time = {user_time + system_time}s")
    
    except FileNotFoundError as e:
        print(e)
