
def logging(logstr):
    with open('urllog.txt', 'a+') as f:
        f.write(logstr)