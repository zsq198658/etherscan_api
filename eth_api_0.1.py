# /usr/bin/python3.7
# ------*.* coding="utf-8" *.*------

import pandas, requests, time
from datetime import datetime
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters


def find_day_value(the_day):
    csv = pandas.read_csv('eth.csv', encoding='utf-8')
    value = ''
    for i in range(len(csv)):
        if csv.date[i] == the_day:
            value = csv.values[i, 1]
            print('当日价格为：' + str(csv.values[i, 1]))
    if value != '':
        return value
    else:
        print('输入错误或没有当日价格。\n')
        return


def last_price():
    api = input('请输入你的api号：')
    url = 'https://api.etherscan.io/api?module=stats&action=ethprice&apikey=' + str(api)
    req = requests.get(url).json()
    ethbtc, btc_time, ethusd, usd_time = req['result'].values()
    btc_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(btc_time)))
    usd_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(usd_time)))
    print('\n以太坊/比特币: ' + str(ethbtc) + '  获取时间：' + btc_time)
    print('以太坊/美元: ' + str(ethusd) + '  获取时间：' + usd_time + '\n')


def historical_chart():
    csv = pandas.read_csv('eth.csv', encoding='utf-8')
    date, value = [], []

    for i in range(len(csv)):
        date.append(csv.date[i])
        value.append(csv.values[i, 1])

    xs = [datetime.strptime(d, '%m/%d/%Y').date() for d in date]
    plt.plot(xs, value)
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.show()


if __name__ == '__main__':
    register_matplotlib_converters()

    menu = '请选择你的操作：\n1.历史信息。\n2.实时信息。\n'
    check = input(menu)

    if check == '1':
        menu1 = '请选择你的操作:\n1.某日价格\n2.历史图表\n'
        check1 = input(menu1)
        if check1 == '1':
            find_day = input('日期（月/日/年):')
            find_day_value(find_day)
        elif check1 == '2':
            historical_chart()
        else:
            print('输入有误')

    elif check == '2':
        menu2 = '请选择你的操作：\n1.实时价格\n2.其他代币查询\n'
        check2 = input(menu2)
        if check2 == '1':
            last_price()
        elif check2 == '2':
            pass
        else:
            print('输入有误')
    else:
        print('输入有误。')


