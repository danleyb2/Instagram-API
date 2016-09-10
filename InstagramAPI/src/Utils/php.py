def file_get_contents(file):
    with open(file,'rb') as fFile:
        return fFile.read()


def file_put_contents(file,contents):
    with open(file,'w') as fFile:
        fFile.write(contents) ##todo return result
        fFile.flush()


def mt_rand(low=0,high=0x7fffffff):
    import random
    return random.randint(low,high)
