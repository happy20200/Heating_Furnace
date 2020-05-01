from bases import *


def get_energy_gas(data, s, num):
    global error_dict
    global case_id
    ex = load_workbook(s, data_only=True)['이력']
    MM = ex.max_row
    for i in range(2, MM):
        # print(i)
        temp_time = dt.datetime.strptime(ex['B' + str(i)].value, "%Y-%m-%d %H:%M:%S")
        # print(ex['B' + str(i)].value, 'row :', i)
        # print(ex['C' + str(i)].value, type(ex['C' + str(i)].value))
        if str(ex['C' + str(i)].value) == '-' or int(ex['C' + str(i)].value) == 0:
            # print('gas off in')
            temp_tem = 0
            temp_off = 1
        else:
            # print('gas right in')
            temp_tem = float(ex['C' + str(i)].value)
            temp_off = 0
        # print(ex['D' + str(i)].value, type(ex['D' + str(i)].value), ex['D' + str(i)].value == '-')
        if str(ex['D' + str(i)].value) == '-' or float(ex['D' + str(i)].value) < 0:
            # print('tmpe off in')
            temp_gas = 0
            gas_off = 1
        else:
            if i < MM and str(ex['D' + str(i + 1)].value) != '-':
                if float(ex['D' + str(i + 1)].value) > 200:
                    print('error!! : ', temp_time, float(ex['D' + str(i + 1)].value))
                    for k in range(-2, 5):
                        error_dict['case'].append(case_id)
                        error_dict['가열로 호기'].append(num)
                        error_dict['시간'].append(ex['B' + str(i + k)].value)
                        error_dict['온도'].append(ex['C' + str(i + k)].value)
                        error_dict['가스'].append(ex['D' + str(i + k)].value)
                    temp_gas = 0
                    gas_off = 1
                    case_id += 1
                else:
                    temp_gas = float(ex['D' + str(i)].value)
                    gas_off = 0
            else:
                temp_gas = float(ex['D' + str(i)].value)
                gas_off = 0
        data.append(
            {'TEMPERATURE': temp_tem, 'GAS': temp_gas, 'TIME': temp_time, 'GAS_OFF': gas_off, 'TEMP_OFF': temp_off})


def get_heat_steel_part1(s, s2, df):
    ex1 = load_workbook(s, data_only=True)['생산계획']
    index = 9
    # print(ex1.max_row, type(ex1.max_row))
    for i in range(index, ex1.max_row, 2):
        # print(i, len((ex1['AR' + str(i)].value).split('\n')), (ex1['AR' + str(i)].value).split('\n'))
        # print(i, ex1['AR' + str(i)].value)
        second_index = 2
        if ex1['AR' + str(i)].value is None or ex1['AR' + str(i)].value == '-' or type(ex1['AR' + str(i)].value) != str:
            pass
        else:
            # print()
            # print(i)
            # print(ex1['AR' + str(i)].value)
            # print('in')
            arr1 = (ex1['AR' + str(i)].value).split('\n')
            arr2 = []
            flag = 0
            while flag == 0:
                second_index += 2
                if ex1['AR' + str(i + second_index)].value is not None:
                    flag = 1
                if (i + second_index) == ex1.max_row:
                    flag = 1
                # print('second index : ', second_index)
                # print(ex1['AR' + str(i + second_index)].value)
            # print('second index : ', second_index)
            if len(arr1) > 1:
                # print(arr1)
                for t in range(len(arr1)):
                    if len(arr1[t].split(' ')) > 1:
                        arr1[t] = arr1[t].split(' ')[0]
                for i2 in range(1, second_index, 2):
                    if ex1['AS' + str(i + i2)].value is not None:
                        get_heat_steel_part2(ex1, i, i2, arr2)
            elif len((ex1['AR' + str(i)].value).split('\n')) == 1:
                # print(arr1)
                if arr1[0] == '냉괴이송':
                    pass
                else:
                    for i2 in range(1, second_index, 2):
                        if ex1['AS' + str(i + i2)].value is not None:
                            get_heat_steel_part2(ex1, i, i2, arr2)
            if len(arr2) != 0:
                # pass
                # print(i)
                # print(arr1)
                # print(arr2)
                for t in arr2:
                    # print(t)
                    df = df.append([[t[0], t[1], t[2], s2]])
                    df = df.reset_index(drop=True)
    return df


def get_heat_steel_part2(ex1, i, i2, arr2):
    index_front = 0
    index_back = len(ex1['AS' + str(i + i2)].value)
    index_front += ex1['AS' + str(i + i2)].value.count('(')
    index_back -= ex1['AS' + str(i + i2)].value.count(')')
    if len(ex1['AS' + str(i + i2)].value[index_front:index_back].split(',')) > 1:
        # print('i값 : ' + str(i) + ' / i2값 : ' + str(i2) + ' / i + i2 :' + str(i + i2))
        # print('원본 : ' + ex1['AS' + str(i + i2)].value[index_front:index_back])
        for t in ex1['AS' + str(i + i2)].value[index_front:index_back].split(', '):
            if len(t.split(',\n')) > 1:
                for k in t.split(',\n'):
                    # print(k)
                    arr2.append([k.strip(), ex1['AP' + str(i + i2 - 1)].value,
                                 [ex1['AT' + str(i)].value, ex1['AT' + str(i + i2 - 1)].value]])
            elif len(t.split('\n')) > 1:
                for k in t.split('\n'):
                    if len(k) < 1:
                        pass
                    else:
                        # print(k)
                        arr2.append([k.strip(), ex1['AP' + str(i + i2 - 1)].value,
                                     [ex1['AT' + str(i)].value, ex1['AT' + str(i + i2 - 1)].value]])
            elif len(t.split(' \n')) > 1:
                for k in t.split(' \n'):
                    if len(k) < 1:
                        pass
                    else:
                        # print(k)
                        arr2.append([k.strip(), ex1['AP' + str(i + i2 - 1)].value,
                                     [ex1['AT' + str(i)].value, ex1['AT' + str(i + i2 - 1)].value]])
            else:
                # print(t)
                arr2.append([t.strip(), ex1['AP' + str(i + i2 - 1)].value,
                             [ex1['AT' + str(i)].value, ex1['AT' + str(i + i2 - 1)].value]])
    else:
        # print('i값 : ' + str(i) + ' / i2값 : ' + str(i2) + ' / i + i2 :' + str(i + i2))
        # print('원본 : ' + ex1['AS' + str(i + i2)].value[index_front:index_back])
        # print(ex1['AS' + str(i + i2)].value[index_front:index_back])
        arr2.append([ex1['AS' + str(i + i2)].value[index_front:index_back], ex1['AP' + str(i + i2 - 1)].value,
                     [ex1['AT' + str(i)].value, ex1['AT' + str(i + i2 - 1)].value]])


# sensitive_file1
def sensitive(s):
    df = pd.read_csv(s, encoding='euc-kr')
    count = 0
    list1 = []
    list2 = []
    for i, row in df.iterrows():
        if df.loc[i, '민간한 재질'] == 'O' or df.loc[i, '아주 민감한 재질'] == 'O':
            list1.append(str(df.loc[i, '사내재질']))
            if df.loc[i, '아주 민감한 재질'] == 'O':
                list2.append(str(df.loc[i, '사내재질']))
            # print(i, df.loc[i, '사내재질'])
            count += 1
    # print(count)
    list3 = set(list1)
    list4 = set(list2)
    return list1, list2


# sensitive_file2
def sensitive2(s1, s2, s3):
    df = pd.read_csv(s1, encoding='euc-kr')
    df2 = pd.read_csv(s2, encoding='euc-kr')
    df3 = pd.read_csv(s3, encoding='euc-kr')
    list1 = []
    list2 = []
    list3 = []
    count = 0
    for i, row in df.iterrows():
        list1.append(df.loc[i, '사내재질'])
    for i2, row in df3.iterrows():
        list3.append(df3.loc[i2, '사내재질'])
    for i3, row in df2.iterrows():
        if df2.loc[i3, '사내재질'] not in list3:
            list2.append(df2.loc[i3, '사내재질'])
        else:
            print(df2.loc[i3, '사내재질'])
            count += 1
    print(len(list3))
    print(count)
    return list1, list2
