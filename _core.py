import os
import re
import requests
import numpy as np
import matplotlib.pyplot as plt


class Ticker:
    '''
    This class will load business data and analyze a stock. Data is from the site macrotrends.com.
    '''
    metrics = {
        "eps": "eps-earnings-per-share-diluted",
        "equity": "total-share-holder-equity",
        "cash_flow": "cash-flow-from-operating-activities",
        "shares": "shares-outstanding",
        "revenue": "revenue",
        "price": "stock-price-history"
    }

    def __init__(self, ticker):
        self._ticker = ticker

    def get_html_content(self, metric):
        site = r"https://www.macrotrends.net/stocks/charts/" + self._ticker + "//" + metric
        return requests.get(site).text
    
    def get_tables(self, html_content):
        return re.findall(r"(<table.*?>.*?</table>)", html_content, re.DOTALL)

    def str2int(self, string):
        try:
            return float(''.join(re.findall(r"[-\d.\d]", string)))
        except:
            return 0

    def get_table_content(self, table):
        table_content = []
        for row in re.findall(r"(<tr.*?>.*?</tr>)", table, re.DOTALL):
            new_row = re.findall(r"<td.*?>(.*?)</td>", row, re.DOTALL)
            if len(new_row) > 0:
                table_content.append([self.str2int(num) for num in new_row])

        array = np.array(table_content)
        
        return array[np.argsort(array[:,0]), :]

    def process_all(self, metric, column=1):
        try:
            html_content = self.get_html_content(metric)
            return self.get_table_content(self.get_tables(html_content)[0])[:,column]
        except:
            return np.array([[0]])


    def load_data(self):
        self._shares = self.process_all(Ticker.metrics['shares'])
        self._eps = self.process_all(Ticker.metrics["eps"])
        self._equity = self.process_all(Ticker.metrics['equity'])
        self._cash_flow = self.process_all(Ticker.metrics["cash_flow"])
        self._revenue = self.process_all(Ticker.metrics['revenue'])
        self._year = np.array(self.process_all(Ticker.metrics['eps'], column=0), dtype='int')

        try:
            self._equitypershare = self._equity / self._shares
        except:
            self._equitypershare = np.arange(len(self._shares))
        try:
            self._ocfps = self._cash_flow / self._shares
        except:
            self._ocfps = np.arange(len(self._shares)) / self._shares

    def plot_moat(self):
        plt.plot(self._year, self._eps / np.max(self._eps), label='EPS')
        plt.plot(self._year, self._equitypershare / np.max(self._equitypershare), label='Equity/Share')
        plt.plot(self._year, self._ocfps / np.max(self._ocfps), label='OCFPS')
        plt.plot(self._year, self._revenue / np.max(self._revenue), label='Revenue')
        plt.xlim(min(self._year), max(self._year))
        plt.xlabel('Year')
        plt.title(f'Moat Plot of {self._ticker}')
        plt.legend()
        plt.show()

    def stock_price(self):
        self._prices = self.process_all('stock-price-history')
        self._current = self._prices[-1]

    def buy(self):
        try:
            if self._equitypershare[-1] > self._current:
                print(f"{self._ticker}: BUY!!!")
                print(round(self._equitypershare[-1], 2), round(self._current, 2))
        except:
            print(f"Could not compare {self._ticker}")




