def sumBool(arr):
    wetLaps = 0
    for i in arr:
        if i:
            wetLaps += 1
    if wetLaps >= (len(arr) / 3):
        return 1
    else:
        return 0


def ConvertTimeDelta(time: str) -> float:
    time = str(time)
    if time == 'N/A' or time == 'nan' or time == 'DNS':
        return 1000

    val = 0
    t = time.split(':')
    val += int(t[0]) * 60
    val += float(t[1])
    return val


if __name__ == '__main__':
    print(ConvertTimeDelta("0 days 00:01:18.218000"))
