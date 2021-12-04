def intToBinArray(number, size=0):
    bitArray = []
    size -= 1

    while size >= 0:
        if 2 ** size > number:
            bitArray.append(0)
        else:
            bitArray.append(1)
            number -= 2 ** size
        size -= 1
    return bitArray