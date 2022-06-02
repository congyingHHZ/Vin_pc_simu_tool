# -*- coding:utf-8 -*-
# Author:hml 20190506
# 命令形式数据中提取vin码



obd_can = [
    '10', '14', '62', 'F1', '90', '*', '*', '*'
    , '21', '*', '*', '*', '*', '*', '*', '*'
    , '22', '*', '*', '*', '*', '*', '*', '*']

obd_kw = [
    '87', 'F1', '11', '49', '02', '01', '00', '00', '00', '*', '00'
    , '87', 'F1', '11', '49', '02', '02', '*', '*', '*', '*', '00'
    , '87', 'F1', '11', '49', '02', '03', '*', '*', '*', '*', '00'
    , '87', 'F1', '11', '49', '02', '04', '*', '*', '*', '*', '00'
    , '87', 'F1', '11', '49', '02', '05', '*', '*', '*', '*', '00'
]

can_rowlen = 8
kw_rowlen = 11


def cmd_to_vin_hexs(in_commad):
    out = []

    l = in_commad.split('\n')
    in_commads = []
    for i in l:
        
        in_commads.extend(i.strip().split(' '))

    print(in_commads)

    if in_commads[0] == '10' or in_commads[0] == '87':
        if in_commads[0] == '10':
            cmd_type = 'can'
        elif in_commads[0] == '87':
            cmd_type = 'kw'

        try:
            if cmd_type == 'can':
                out = [in_commads[x] for x, y in enumerate(obd_can) if y == '*']
            elif cmd_type == 'kw':
                out = [in_commads[x] for x, y in enumerate(obd_kw) if y == '*']
        except Exception as e:
            msg = '命令解析为:' + cmd_type + ' ,但是无法提取VIN码的字节，请核对命令'
        else:
            msg = '从命令中提取vin码：right'
    else:
        msg = '无法解析命令格式'

    return out, msg


if __name__ == '__main__':
    in_commad = """10 14 5A 91 4C 5A 57 41	   
7E8     	21 44 41 47 42 34 47 42	  
7E8     	22 37 32 37 32 30 37 30
"""
    print(cmd_to_vin_hexs(in_commad))
