"""
python {file_path}\main.py
"""
from FinanceManager import *

try:
    my_fm = FinanceManager('test.txt')
    my_fm.initUserMenu()
except ValueError as e:
    print(e)
    exit()
except Exception as e:
    print('Unexpected Error! ',e)
    exit()



