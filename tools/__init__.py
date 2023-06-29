def hump_to_underline(text):
    """
    驼峰转下划线
    :param text:
    :return:
    """
    res = []
    for index, char in enumerate(text):
        if char.isupper() and index != 0:
            res.append("_")
        res.append(char)
    return ''.join(res).lower()


def underline_to_hump(text):
    """
    下划线转大驼峰
    :param text:
    :return:
    """
    arr = text.lower().split('_')
    res = []
    for i in arr:
        res.append(i[0].upper() + i[1:])
    return ''.join(res)


def underline_to_camel(text):
    """
    下划线转小驼峰
    :param text:
    :return:
    """
    s = underline_to_hump(text)
    return s[0].lower() + s[1:]

def underline_to_short(text):
    """
    下划线取short
    :param text:
    :return:
    """
    arr = text.lower().split('_')
    return ''.join(arr[1:])