# /usr/bin/python3.7
# ------*.* coding="utf-8" *.*------

import pandas
import requests
import time
from datetime import datetime
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters


def find_day_value():
    the_day = input('查询的日期（月/日/年):')
    csv = pandas.read_csv('eth.csv', encoding='utf-8')
    value = ''
    for i in range(len(csv)):
        if csv.date[i] == the_day:
            value = csv.values[i, 1]
            print('当日价格为：' + str(csv.values[i, 1]))
    if value == '':
        print('输入错误或没有当日价格。\n')


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


def last_price():
    api = input('请输入你的api_code：')
    url = 'https://api.etherscan.io/api?module=stats&action=ethprice&apikey=' + str(api)
    req = requests.get(url).json()
    ethbtc, btc_time, ethusd, usd_time = req['result'].values()
    btc_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(btc_time)))
    usd_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(usd_time)))
    print('\n以太坊/比特币: ' + str(ethbtc) + '  获取时间：' + btc_time)
    print('以太坊/美元: ' + str(ethusd) + '  获取时间：' + usd_time + '\n')


def token_scan():
    token_address = input('代币的合约地址:')
    api = input('api_code:')
    url = 'https://api.etherscan.io/api' \
          '?module=stats&action=tokensupply&contractaddress='\
          + token_address + '&apikey=' + api

    req = requests.get(url).json()
    value = req['result']
    print('该代币总量为：' + value)


def address_token():
    contract_address = input('代币合约地址：')
    address = input('钱包的地址：')
    api = input('api_code:')
    url = 'https://api.etherscan.io/api' \
          '?module=account&action=tokenbalance&contractaddress=' \
          + contract_address + '&address=' + address \
          + '&tag=latest&apikey=' + api
    req = requests.get(url).json()
    token_value = req['result']
    print('该地址持有：' + token_value
          + '(提供的接口查询结果远小于1时返回的也是‘1’，此处是网站api的一个BUG。。)')


def address_info():
    address = input('钱包地址：')
    api = input('api_code:')
    url = 'https://api.etherscan.io/api' \
          '?module=account&action=balance&address='\
          + address + '&tag=latest&apikey=' + api

    req = requests.get(url).json()
    eth_value = req['result'].values()
    print(address + '该地址ETH：' + eth_value)


def default_task():
    print('输入错误')


def quit_loop():
    exit(0)


if __name__ == '__main__':
    register_matplotlib_converters()

    switch_dict = {
        '1': find_day_value,
        '2': historical_chart,
        '3': last_price,
        '4': token_scan,
        '5': address_token,
        '6': address_info,
        '0': quit_loop,
    }

    menu = '菜单：\n' \
           '1.历史信息\n' \
           '2.历史图表\n' \
           '3.实时价格\n' \
           '4.ETH链上其他代币总供应量查询\n' \
           '5.查询持有ETH链上其他代币数量\n' \
           '6.查询持有ETH数量\n' \
           '\n0.退出\n' \
           '请选择你的操作：'
    while True:
        check = input(menu)
        # 获取switch_dict字典的'check'的对应函数，默认为default_task
        switch_dict.get(check, default_task)()
        loop = input('\n是否继续(1.是，2.否)：')
        if loop == '2':
            break
