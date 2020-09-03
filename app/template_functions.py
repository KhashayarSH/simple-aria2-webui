from datetime import timedelta

# converts bytes to K,M,G,TB
def size_adapter(size):
    if size == '':
        return ''
    size = float(size)
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(format(size, '.2f'))+ power_labels[n]+'B'

# converts sec to d/h/m format
def time_adapter(sec):
    if sec == '':
        return ''
    sec = int(sec)
    import datetime
    res = timedelta(seconds =sec)
    return res

# gets a list with 3 elements returns estimated time left in seconds
def sec_left(list):
    if int(list[2]) == 0:
        return ''
    sec=(int(list[0])-int(list[1]))/int(list[2])
    return sec

# gets a list with 2 elements and returns percentage of list[1]/list[0]
def percent(list):
    if(int(list[0])):
        return format(float(list[1])/int(list[0])*100, '.2f')
    else:
        return ''
