# encoding:utf-8
import binascii
import re

import win32clipboard as w


def vin2hex(vin):
    print('输入字符长度为: ', len(vin))
    vin_hexs = []

    try:
        for i in vin:
            vin_hexs.append(hex(ord(i))[2:].upper())
    except:
        print('请检查输入的VIN码')
        return False
    else:
        return ' '.join(vin_hexs)


def hex2vin(hex_str):
    vins = []
    hex_s = hex_str.split(' ')
    try:
        for i in hex_s:
            vins.append(binascii.a2b_hex(i).decode().upper())
    except binascii.Error as E:
        msg = f"十六进制[{i}]转换为ASCII码出错"
        return msg, False

    return ''.join(vins), True


def check_vin(in_vin):
    out_vin = in_vin
    msg = None
    check_index = 9
    year_index = 10

    weight_values = {
        1: 8,
        2: 7,
        3: 6,
        4: 5,
        5: 4,
        6: 3,
        7: 2,
        8: 10,
        10: 9,
        11: 8,
        12: 7,
        13: 6,
        14: 5,
        15: 4,
        16: 3,
        17: 2}
    change_vals = {
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        'A': 1,
        'B': 2,
        'C': 3,
        'D': 4,
        'E': 5,
        'F': 6,
        'G': 7,
        'H': 8,
        'J': 1,
        'K': 2,
        'L': 3,
        'M': 4,
        'N': 5,
        'P': 7,
        'R': 9,
        'S': 2,
        'T': 3,
        'U': 4,
        'V': 5,
        'W': 6,
        'X': 7,
        'Y': 8,
        'Z': 9}
    formals = []

    if len(in_vin) == 17:
        print('输入为：%s' % in_vin[:check_index - 1] + ' ' + in_vin[check_index - 1] + ' ' + in_vin[check_index:])
        for ind, i in enumerate(in_vin):
            change_val, weight_val = None, None
            if ind + 1 != 9:
                weight_val = weight_values[ind + 1]
                try:
                    change_val = change_vals[i]
                except KeyError:
                    print('\n输入VIN码第%s位含有非法字符"%s",请检查输入的VIN码\n' % (str(ind + 1), i))
                    msg = ('\n输入VIN码第%s位含有非法字符"%s",请检查输入的VIN码\n' % (str(ind + 1), i))
                    return False, msg
                formals.append(weight_val * change_val)
        else:
            out = sum(formals)
            out = out % 11
            if out == 10:
                out = 'X'

        if in_vin[check_index - 1] != str(out):
            print('原检验位:%s,经计算校验位应为%s' % (in_vin[check_index - 1], out))
            msg = '原检验位:%s,经计算校验位应为%s' % (in_vin[check_index - 1], out)
            out_vin = in_vin[:check_index - 1] + str(out) + in_vin[check_index:]
        else:
            print('第%s位校验位符合规律：%s' % (check_index, out))
            msg = '第%s位校验位符合规律：%s' % (check_index, out)

        year = in_vin[year_index - 1]
        if re.fullmatch(r'\d', year):
            msg += f'；年款可能为200{year}。'
        else:
            year_int = ord(year)
            year_ranges = [(65, 72),(74, 78),(80, 80),(82, 84),(86, 89)]
            for part, year_range in enumerate(year_ranges):
                if year_range[0]<= year_int <= year_range[1]:
                    year = "20" + str(year_int - 65 + 10 - part)
                    break
            else:
                year = "未知"
            # if 65 <= year_int < 73:
            #     year = "20" + str(year_int - 65 + 10)
            # # 跳过 I
            # elif 74 <= year_int <= 78:
            #     year = "20" + str(year_int - 65 + 10 + 1)
            # # 去掉 O
            # elif year_int == 80:
            #     year = "20" + str(year_int - 65 + 10 + 2)
            # # 跳过Q
            # elif 82 <= year_int <= 84:
            #     year = "20" + str(year_int - 65 + 10 + 3)
            # # 跳过U
            # elif 86 <= year_int <= 89:
            #     year = "20" + str(year_int - 65 + 10 + 4)
            # else:
            #     year = "未知"

            msg += f'；年款可能为 {year}。'
    else:
        # print('输入位数不等于17')

        msg = '输入位数大于17' if len(in_vin) > 17 else '输入位数小于17'
        return False, msg

    return out_vin, msg


def setText(aString):  # 写入剪切板
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardText(aString)
    w.CloseClipboard()


def vin2hex_check_vin(vin):
    new_vin = check_vin(vin)
    out = vin2hex(new_vin)
    return out


def hex2vin_check_vin(hex_vin):
    out, status = hex2vin(hex_vin)
    new_vin, msg = check_vin(out)
    return new_vin, msg


if __name__ == '__main__':
    vin = 'LFPH3ACC5JF365780'
    hex_vin = '4C 53 56 46 48 34 30 47 38 47 4C 53 56 46 48 34 30'

    #
    # out = vin2hex_check_vin(vin)
    print(check_vin(vin))
    # out = hex2vin_check_vin(hex_vin)

    # print(out)
    # setText(out)
    # input('..')
