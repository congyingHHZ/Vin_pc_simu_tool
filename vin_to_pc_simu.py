import vin_tool
import copy

obd_can = ['14','49','02','00']
obd_kw = [
'87','F1','11','49','02','01','00','00','00','*','D1'
,'87','F1','11','49','02','02','*','*','*','*','D2'
,'87','F1','11','49','02','03','*','*','*','*','D3'
,'87','F1','11','49','02','04','*','*','*','*','D4'
,'87','F1','11','49','02','05','*','*','*','*','D5'
]
can_rowlen = 8
kw_rowlen = 11


# def check_vin(in_vin):
    
#     out_vin = in_vin
#     msg = None
#     check_index = 9


#     weight_values = {
#         1: 8,
#         2: 7,
#         3: 6,
#         4: 5,
#         5: 4,
#         6: 3,
#         7: 2,
#         8: 10,
#         10: 9,
#         11: 8,
#         12: 7,
#         13: 6,
#         14: 5,
#         15: 4,
#         16: 3,
#         17: 2}
#     change_vals = {
#         '0': 0,
#         '1': 1,
#         '2': 2,
#         '3': 3,
#         '4': 4,
#         '5': 5,
#         '6': 6,
#         '7': 7,
#         '8': 8,
#         '9': 9,
#         'A': 1,
#         'B': 2,
#         'C': 3,
#         'D': 4,
#         'E': 5,
#         'F': 6,
#         'G': 7,
#         'H': 8,
#         'J': 1,
#         'K': 2,
#         'L': 3,
#         'M': 4,
#         'N': 5,
#         'P': 7,
#         'R': 9,
#         'S': 2,
#         'T': 3,
#         'U': 4,
#         'V': 5,
#         'W': 6,
#         'X': 7,
#         'Y': 8,
#         'Z': 9}
#     formals = []

#     if len(in_vin) == 17:
#         print('输入为：%s' % in_vin[:check_index - 1] + ' ' + in_vin[check_index - 1] + ' ' + in_vin[check_index:])
#         for ind, i in enumerate(in_vin):
#             if ind+1 != 9:
#                 weight_val = weight_values[ind+1]
#                 try:
#                     change_val = change_vals[i]
#                 except KeyError:
#                     print('\n输入VIN码含有非法字符"%s",请检查输入的VIN码\n' %i)

#                 formals.append(weight_val * change_val)
#         else:
#             out = sum(formals)
#             out = out % 11
#             if out == 10:
#                 out = 'X'

#         if in_vin[check_index-1] != str(out):
#             print('原检验位:%s,经计算校验位应为%s' % (in_vin[check_index-1], out))
#             msg = '原检验位:%s,经计算校验位应为%s' % (in_vin[check_index-1], out)
#             out_vin = in_vin[:check_index-1] + str(out) + in_vin[check_index:]
#         else:
#             print('第%s位校验位符合规律：%s' % (check_index,out))
#             msg = '第%s位校验位符合规律：%s' % (check_index,out)
#     else:
#         # print('输入位数不等于17')
#         msg = '输入位数不等于17'
#         return False,msg
        
#     return out_vin,msg


def get_vin(in_vin):

	try:
		vin_hex = vin_tool.vin2hex(in_vin)
	except:
		pass
	
	vin_hexs = vin_hex.split(' ')
	return vin_hexs

def _can(in_vin_hexs):
	obd_vin_hexs = obd_can + in_vin_hexs
	for i in range(1, int(len(obd_vin_hexs)/7)):
		obd_vin_hexs.insert(7*i+i-1,'2'+str(i))

	obd_vin_hexs.insert(0,'10')
	obd_vin_hexs = new_line(obd_vin_hexs,can_rowlen)
	return obd_vin_hexs


def _kw(in_vin_hexs):

	vin_hexs = copy.deepcopy(in_vin_hexs)

	out = [vin_hexs.pop(0) if i == '*' else i for i in obd_kw ]
	out = new_line(out,kw_rowlen)
	return out

def new_line(in_list,rowlen):

	for i in range(int(len(in_list)/rowlen)):
		in_list.insert(rowlen*i+i,'\n')

	return in_list

if __name__ == '__main__':
	l = get_vin('LNBMDBAF0GUO97436')
	print(vin_tool.check_vin('LNBMDBAF0GUO97436'))
	out = _can(l)
	# out = new_line(out,can_rowlen)
	print(' '.join(out))
