import re
import requests
import numpy as np
import pandas as pd

def generate_table(table_data):
    '''
    This function takes in table data and prints it in html for copying and pasting.
    
    Args:
        table_data (arr): Numpy array of the table contents
    '''
    
    size = table_data.shape
    print("<table>")
    for r in range(size[0]):
        print("\t<tr>")
        for c in range(size[1]):
            print(f"\t\t<td>{table_data[r, c]}</td>")
        print("\t</tr>")
    print("</table>")
    
def string2number(string):
    # Check if the string is a number in accounting notation
    if re.match(r'^[\(\-]?[\d,]+(?:\.\d+)?$', string):
        # Remove commas and parentheses if present
        string = string.replace(',', '').replace('(', '-').replace(')', '')

        # Convert to float or int based on decimal part
        if '.' in string:
            return float(string)
        else:
            return int(string)

    return string  # Return the original string if not a number in accounting notation

def extract_table_info(table):
    '''
    This function returns all the contents of an html table in a numpy array. It fills in column spans with nans.
    
    Args:
        table (string): html table to process.
        
    Returns
        table_data (arr): Numpy array with the table contents.
    '''
    # Count the number of rows
    r = table.count("<tr")
    
    # Find the number of columns
    pattern = re.compile(r"<tr.*?>(.*?)</tr>", re.DOTALL | re.IGNORECASE)
    rows = re.findall(pattern, table)
    c = rows[0].count("<td")
    
    # Iterate through each row and get data
    table_data = []
    pattern = re.compile(r"<td.*?>.*?</td>", re.DOTALL | re.IGNORECASE)
    for row in rows:
        new_row = []
        for data in re.findall(pattern, row):
            #print(data)
            try:
                colspans = int(re.findall(r"colspan=\"(\d)\"", data)[0])
                new_row.append(string2number(re.findall(r">(.*?)<", data)[0]))
                for _ in range(colspans - 1):
                    new_row.append(float('nan'))
            except:
                new_row.append(string2number(re.findall(r"<td.*?>(.*?)</td>", data)[0]))
        table_data.append(new_row)
    
    table_data = np.array(table_data)
    return table_data
    
def print_table(table):
    '''
    This function takes in generic html table and prints it out in a stripped version for easy reading.
    
    Args:
        table (string): html table to print
    '''

    # Print table tag
    print("<table>")

    # Iterate through each row and print contents
    for row in re.findall(r"<tr.*?>.*?</tr>", table):
        print("\t<tr>")
        for data in re.findall(r"<td.*?>.*?</td>", row):
            print("\t\t" + data)
        print("\t</tr>")

    # Print closing table tag
    print("</table>")




