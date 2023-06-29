import os
import re
import requests
import numpy as np
import matplotlib.pyplot as plt


class Ticker:
    '''
    This class will load business data and analyze a stock. Data is from the site macrotrends.com.
    '''

    def __init__(self, ticker, name):
        self._ticker = ticker
        self._name = name

    def __repr__(self):
        print(f"Ticker: {self.get_ticker}")

    @property
    def ticker(self):
        self._ticker = ticker

    @property
    def name(self):
        self._name = name

    def get_data(self):
        site = f"https://www.macrotrends.net/stocks/charts/{self._ticker}/{self._name}/eps-earnings-per-share-diluted"
        data = requests.get(site).text
        tables_start = re.findall(r"<table.*?>", data)
        tables_end = re.findall(r"</table>", data)
        tables_start

        table_info = []
        n1 = 0;n2 = 0;n3 = 0
        for i in range(len(tables_start)):
            n1 += data[n3:].find(tables_start[i]) + n3
            n2 += n1 + len(tables_start[i])
            n3 += data[n3:].find(tables_end[i]) + n3
            table_info.append(data[n2:n3])    

        
        shares = format_table(table_info[0])
        array_shares = html_table_to_array(shares)

        self._eps = array_shares

    def plot_eps(self):
        plt.plot(self._eps[:,0], self._eps[:,1], label='EPS');
        plt.legend()
        plt.xlim([self._eps[0,0], self._eps[-1,0]])
        plt.show()





def format_table(table_info, ret=True, disp = False):
    revenues = table_info.replace('\n', '').replace('\t', '').replace(' ', '').replace('$', '').strip()

    # Remove table head
    revenues = re.sub(r"(<thead.*?>)(.*?)(</thead>)", r"", revenues)

    # Remove table and tbody tags
    revenues = re.sub(r"<tbody>|</tbody>", "", revenues)
    revenues = re.sub(r"<table>|</table>", "", revenues)


    # Remove any styling options
    revenues = re.sub(r"(<td)(.*?)(>)", "<td>", revenues)
    revenues = re.sub(r"(<th)(.*?)(>)", "<td>", revenues)
    revenues = re.sub(r"<span.*?>|</span>", "", revenues)

    # Add table tags
    revenues = r"<table>" + revenues + r"</table>"

    # Add newline characters
    revenues = re.sub(r"<tr>", r"\t<tr>\n", revenues)
    revenues = re.sub(r"(<td.*?/td>)", r"\t\t\1\n", revenues)
    revenues = re.sub(r"</tr>", r"\t</tr>\n", revenues)
    revenues = re.sub(r"<table>", r"<table>\n", revenues)
    
    if disp:
        print(revenues)
    
    if ret:
        return revenues
    
def str2num(string):
    if '.' in string:
        return float(string.replace(',', ''))
    else:
        return int(string.replace(',', ''))
    
def get_table_size(table):
    m = len(re.findall(r"<tr>", table))
    n = int(len(re.findall(r"<td>", table)) / m)
    return m, n

def html_table_to_array(table):
    data = re.findall(r"<td>(.*?)</td>", table)
    m, n = get_table_size(table)
    
    array = np.array([float('nan')] * m * n).reshape(m,n)
    count = 0
    for i in range(m):
        for j in range(n):
            array[i,j] = str2num(data[count])
            count += 1
            
    
    
    return array[np.argsort(array[:,0]),:]


def process(site, name):
    data = requests.get(site).text
    tables_start = re.findall(r"<table.*?>", data)
    tables_end = re.findall(r"</table>", data)
    tables_start

    table_info = []
    n1 = 0;n2 = 0;n3 = 0
    for i in range(6):
        n1 += data[n3:].find(tables_start[i]) + n3
        n2 += n1 + len(tables_start[i])
        n3 += data[n3:].find(tables_end[i]) + n3
        #print(n1, n2, n3)
        table_info.append(data[n2:n3])

    

example = '''
data = requests.get(r'https://www.macrotrends.net/stocks/charts/TXT/textron/shares-outstanding').text

tables_start = re.findall(r"<table.*?>", data)
tables_end = re.findall(r"</table>", data)
tables_start

table_info = []
n1 = 0;n2 = 0;n3 = 0
for i in range(6):
    n1 += data[n3:].find(tables_start[i]) + n3
    n2 += n1 + len(tables_start[i])
    n3 += data[n3:].find(tables_end[i]) + n3
    #print(n1, n2, n3)
    table_info.append(data[n2:n3])
    
revenues = format_table(table_info[0])

array_shares = html_table_to_array(revenues)

plt.plot(array_revenues[:,0], array_revenues[:,1]);'''
