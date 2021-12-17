from datetime import datetime
from IInvoice import *
import ast
class FinanceManager():
    def __init__(self, file_name = None):
        if file_name is None:
            self.file_name = 'fin_db.txt'
        else:
            self.file_name = file_name
        self.invoicesStorage = dict()
        self.mainMenu = [
            {
                'name': 'Расходы',
                'indx': 'Expenses',
                },
            {
                'name': 'Доходы',
                'indx': 'Income',
                },
            {
                'name': 'Итоги',
                'indx': 'Report',
                },
            {
                'name': 'Планируемые расходы',
                'indx': 'Plan_Expenses',
                },
            {
                'name': 'Планируемые доходы',
                'indx': 'Plan_Income',
                },
            {
                'name': 'Завершить работу',
                'indx': 'Exit',
                },
        ]

        self.secMenu = [
            {
                'name' : 'Добавить',
                'indx' : 'Add',
                },
            {
                'name' : 'Редактировать',
                'indx' : 'Edit',
                },
            {
                'name' : 'Удалить',
                'indx' : 'Remove',
                },
            {
                'name' : 'Назад',
                'indx' : 'GoBack',
                },
            {
                'name' : 'Завершить работу',
                'indx' : 'Exit',
                },
        ]
        self.loadFromFile()
        
    def saveToFile(self, file_name=None):
        """Save storage to file"""
        if file_name is None:
            file_name = self.file_name
        try:
            with open(file_name,'w') as f:
                for invoices in self.invoicesStorage.values():
                    for invoice in invoices.get():
                        text = "{ "
                        for key, val in invoice.items():
                            if key == 'summ':
                                text += "'{}' : {}, ".format(key, val)
                            elif key == 'time':
                                #print(key, datetime.strftime(val,'%d.%m.%Y'))
                                text += "'{}' : '{}', ".format(key, datetime.strftime(val,'%d.%m.%Y'))
                            else:
                                text += "'{}' : '{}', ".format(key, val)
                        text += "}\n"
                        f.write(text)
            print("Данные были успешно сохранены\n")         
        except Exception as e:
            print(e)
            raise e
            
    def loadFromFile(self, file_name=None):
        """Load file to storage"""
        if file_name is None:
            file_name = self.file_name
        try:
            with open(file_name,'r') as f:
                text = f.readlines()
                cntr = 0
                for item in text:
                    tmp = ast.literal_eval(item)
                    tmp['time'] = datetime.strptime(tmp['time'],'%d.%m.%Y')
                    self.addInvoice(tmp)
            print("Данные были успешно загружены\n")            
        except Exception as e:
            print(e)
            raise e
        
    def sort(self):
        def get_obj_type(_object):
            return _object.get('obj_type')
        tmp = list()
        for item in self.invoicesStorage:
            tmp.extend(item.get())
        tmp.sort(key=get_obj_type)
        return tmp
    
    def find(self, _invoice: dict):
        """Returns invoice object what found except returns @None@"""
        if isinstance(_invoice, dict):
            for invoices in  self.invoicesStorage:
                for invoice in invoices.get():
                    if (invoice['obj_type'] == _invoice['obj_type']
                    and invoice['info'] == _invoice['info']):
                        return invoice
        elif isinstance(_invoice, Invoice):
            for _tmp in _invoice.get():
                for invoices in self.invoicesStorage:
                    for invoice in invoices.get():
                        if (invoice['obj_type'] == _tmp['obj_type']
                        and invoice['info'] == _tmp['info']):
                            return invoice
        elif _invoice in self.invoicesStorage:
            return _invoice
        
    def getInvoice(self, _invoice=None, _filter=None):
        """Returns invoice's list in storage what found except returns @None@"""
        if _filter is not None:
            tmp = self.invoicesStorage.get(type(_filter['type_name']))
            if tmp:
                return tmp.get()
            else:
                for key, val in self.invoicesStorage.items():
                    if str(_filter['type_name']).lower() in str(key).lower():
                        return val.get()#[_filter['index']]
        return self.invoicesStorage.get(type(_invoice))
    
    def addInvoice(self, _invoice):
        """Appends/Create new invoice to storage"""
        if isinstance(_invoice, Invoice):
            tmp = self.getInvoice(_invoice)
            if tmp is None:
                self.invoicesStorage.update({type(_invoice): _invoice})
            else:
                tmp.add(_invoice.get())
        elif isinstance(_invoice, dict) and _invoice.get('obj_type') is not None:
            if _invoice['obj_type'] in ['Income']:
                self.addInvoice(Income(_invoice))
            elif _invoice['obj_type'] in ['Expenses']:
                self.addInvoice(Expenses(_invoice))
            elif _invoice['obj_type'] in ['Plan_Income']:
                self.addInvoice(Plan_Income(_invoice))
            elif _invoice['obj_type'] in ['Plan_Expenses']:
                self.addInvoice(Plan_Expenses(_invoice))
            
        elif isinstance(_invoice, (list, tuple, set)):
            for item in _invoice:
                self.addInvoice(item)    

    def removeInvoice(self, _type_name='', _index=''):#self.removeInvoice(_main_point['indx'], indexInput)
        """Calling IInvoice.remove() method if found invoice in storage"""
        for key, val in self.invoicesStorage.items():
            if str(_type_name).lower() in str(key).lower():
                tmp = val.remove(_index)
                
    def toString(self, type_name=None):
        """Returns repr string"""
        _log = ''
        for key, val in self.invoicesStorage.items():
            if type_name is not None:
                if val.__class__.__name__ == type_name:
                    _log+=val.toString()
            else:
                _log+=val.toString()
        if _log == '':
            _log = "{} is empty.\n".format(type_name)
        return _log

    def getTotal(self, type_name, period_start_date:datetime, period_end_date:datetime, offered=None):
        """Returns total by invoices type name and period"""
        total = 0
        for key, val in self.invoicesStorage.items():
            if val.__class__.__name__ == type_name:
                for item in val.get():
                    if period_start_date<= item['time']<= period_end_date:
                        if offered is not None:
                            if item.get('offered') is not None and item['offered']==True:
                                total += item['summ']
                        else:
                            total += item['summ']
        return total        
    
    def getReport(self, period_start_date:datetime, period_end_date:datetime):
        """Returns report by period"""
        income = self.getTotal("Income", period_start_date, period_end_date)
        expenses = self.getTotal("Expenses", period_start_date, period_end_date)

        incomePlan = self.getTotal("Plan_Income", period_start_date, period_end_date)
        expensesPlan = self.getTotal("Plan_Expenses", period_start_date, period_end_date)

        offeredIncomePlan = self.getTotal("Plan_Income", period_start_date, period_end_date, offered=True)
        offeredExpensesPlan = self.getTotal("Plan_Expenses", period_start_date, period_end_date, offered=True)

        total = income - expenses + offeredIncomePlan - offeredExpensesPlan

        return  ("Балансовый отчет за период ({} - {})\n"
                "Фактические:\n\tдоходы: {}\n\tрасходы: {}\n\tбаланс: {}\n"
                "Плановые:\n\tдоходы: {}\n\tрасходы: {}\n\tбаланс: {}\n"
                "\tиз них реализовано:\n\t\tдоходы: {}\n\t\tрасходы: {}\n\t\tбаланс:{}\n"
                "Итого: {}").format(
            datetime.strftime(period_start_date,'%d.%m.%Y'),
            datetime.strftime(period_end_date,'%d.%m.%Y'),
            round(income, 2),
            round(expenses, 2),
            round(income-expenses, 2),
            round(incomePlan, 2),
            round(expensesPlan, 2),
            round(incomePlan - expensesPlan, 2),
            round(offeredIncomePlan, 2),
            round(offeredExpensesPlan, 2),
            round(offeredIncomePlan - offeredExpensesPlan, 2),
            round(total, 2)
            )
    def getMainMenu(self):
        """Returns main menu points"""
        return self.mainMenu
    def getSecMenu(self):
        """Returns second menu points"""
        return self.secMenu
    
    def initUserMenu(self):
        """Use this to start program in main"""
        while(True):
            curr_menu = self.getMainMenu()
            cntr = 0
            
            for item in curr_menu:
                cntr+=1
                print("{}. {}".format(cntr, item['name']), end='\n\n')

            userInput = input("Укажите желаемый номер пункта меню: ")
            try:
                curr_main_point = curr_menu[ (int(userInput) -1)%len(curr_menu) ]
            except IndexError:
                self.saveToFile()
                raise IndexError("Вы указали значение, которое не является пунктом этого меню") 
            except ValueError:
                self.saveToFile()
                raise ValueError("Вы указали значение, которое не является целым числом")        
            if curr_main_point['indx']=='Exit':
                self.saveToFile()
                break
                exit()
            if curr_main_point['indx']=='Report':
                userInput = input("Введите дату начала периода в формате ДД.ММ.ГГГГ: \n")
                try:
                    start = datetime.strptime(userInput, '%d.%m.%Y')
                except ValueError:
                    self.saveToFile()
                    raise ValueError("Вы указали значение, которое не соответствует формату")
                userInput = input("Введите дату окончания периода в формате ДД.ММ.ГГГГ: \n")
                try:
                    end = datetime.strptime(userInput, '%d.%m.%Y')
                except ValueError:
                    self.saveToFile()
                    raise ValueError("Вы указали значение, которое не соответствует формату")
                print(self.getReport(start, end))
                continue
            while(True):                
            
                print(self.toString(curr_main_point['indx']))
                
                curr_menu = self.getSecMenu()
                cntr = 0
                
                for item in curr_menu:
                    cntr+=1
                    print("{}. {}".format(cntr, item['name']), end='\n\n')

                userInput = input("Укажите желаемый номер пункта меню: ")
                try:
                    curr_point = curr_menu[ (int(userInput)-1)%len(curr_menu) ]
                except IndexError:
                    self.saveToFile()
                    raise IndexError("Вы указали значение, которое не является пунктом этого меню") 
                except ValueError:
                    self.saveToFile()
                    raise ValueError("Вы указали значение, которое не является целым числом") 
                if curr_point['indx']=='Exit':
                    self.saveToFile()
                    exit()
                elif curr_point['indx']=='GoBack':
                    break
                
                self.menuManager(curr_main_point, curr_point)
                
    def menuManager(self, _main_point:dict, _point:dict ):
        """Manage chosen points"""
        if _point['indx'] in ['Add']:
            dateInput = datetime.strptime(input("Введите дату в формате ДД.ММ.ГГГГ: \n"), '%d.%m.%Y')
            infoInput = str( input(
                "Введите информацию/наименование для {}: \n".format(
                    _main_point['name'].lower()
                    )
                ))
            summInput = round( float( input(
                "Введите сумму для {}: \n".format(
                    _main_point['name'].lower()
                    )
                )), 2 )
            
            if summInput<0:
                self.saveToFile()
                raise ValueError("Сумма не может быть меньше нуля")
            
            if _main_point['indx'] in ['Plan_Income', 'Plan_Expenses']:
                offerInput = input(
                    "Введите \"Да\" если {} был осуществлен:\n".format(
                        _main_point['name'].lower()
                        )
                    )
                if _main_point['indx'] in ['Plan_Income']:
                    self.addInvoice(
                        Plan_Income(
                            {
                                'time':dateInput,
                                'info':infoInput,
                                'summ' : summInput,
                                'offered': bool(str(offerInput).lower()=='да'),
                                },
                            )
                        )
                elif _main_point['indx'] in ['Plan_Expenses']:
                    self.addInvoice(
                        Plan_Expenses(
                            {
                                'time':dateInput,
                                'info':infoInput,
                                'summ' : summInput,
                                'offered': bool(str(offerInput).lower()=='да'),
                                },
                            )
                        )  
            elif _main_point['indx'] in ['Income']:
                self.addInvoice(
                    Income(
                        {
                            'time':dateInput,
                            'info':infoInput,
                            'summ':summInput,
                            },
                        )
                    )
            elif _main_point['indx'] in ['Expenses']:
                self.addInvoice(
                    Expenses(
                        {
                            'time':dateInput,
                            'info':infoInput,
                            'summ':summInput,
                            },
                        )
                    )
        elif _point['indx'] in ['Edit', 'Remove']:
            tmp = self.getInvoice(
                _filter = {
                    'type_name': _main_point['indx'],
                    },
                )
            indexInput =  int(input(
                "Введите номер {} для того, чтобы {} его:\n".format(
                    _main_point['name'].lower(),
                    _point['name'].lower()
                    )
                ))-1
            
            if indexInput<0 or indexInput>len(tmp):
                self.saveToFile()
                raise IndexError("Выход за пределы массива")
            curr_invoice = tmp[indexInput]
            
            if curr_invoice is not None:
                if _point['indx'] in ['Edit']:
                    dateInput = datetime.strptime(input(
                        "Введите дату в формате ДД.ММ.ГГГГ: \n"
                        ), '%d.%m.%Y')
                    infoInput = str(input(
                        "Введите информацию/наименование для {}: \n".format(
                            _main_point['name'].lower()
                            )
                        ))
                    summInput = round(float(input(
                        "Введите сумму для {}: \n".format(
                            _main_point['name'].lower()
                            )
                        )), 2)
                    if summInput<0:
                        self.saveToFile()
                        raise ValueError("Сумма не может быть меньше нуля")
                    if _main_point['indx'] in ['Plan_Income', 'Plan_Expenses']:
                        offerInput = input(
                            "Введите \"Да\" если {} был осуществлен:".format(
                                _main_point['name'].lower()
                                )
                            )
                        commitInput = input(
                            "Введите \"Да\" если {} действительно нужно {}:\n".format(
                                _main_point['name'].lower(),
                                _point['name'].lower()
                                )
                            )
                        print(commitInput.lower(), type(commitInput.lower()))
                        if commitInput.lower()=='да':
                            curr_invoice.update(
                                {
                                    'time' : dateInput,
                                    'info' : infoInput,
                                    'summ' : summInput,
                                    'offered': bool(str(offerInput).lower()=='да'),
                                    },
                                )
                    else:
                        commitInput = str(input(
                            "Введите \"Да\" если {} действительно нужно {}:\n".format(
                                _main_point['name'].lower(),
                                _point['name'].lower()
                                )
                            ))
                        
                        print(commitInput.lower(), type(commitInput.lower()))
                        if commitInput.lower() == 'да':
                            curr_invoice.update(
                                {
                                    'time' : dateInput,
                                    'info' : infoInput,
                                    'summ' : summInput,
                                    },
                                )
                else:
                    commitInput = str(input(
                        "Введите \"Да\" если {} действительно нужно {}:\n".format(
                            _main_point['name'].lower(),
                            _point['name'].lower()
                            )
                        ))
                    if commitInput.lower() in 'да':
                        self.removeInvoice(_main_point['indx'], indexInput)
            else:
                self.saveToFile()
                raise Exception("Такого объекта не существует")
        else:
            pass
