class IInvoiceInterface:
    
    def find(_link: str, _type_name = None):
        """Returns foundet cost in storage by link and type if exist"""
        pass
    def add(self, _object: dict):
        """Add cost in storage"""
        pass
    def edit(self, _link: str, _object:dict):
        """Update cost in storage"""
        pass  
    def remove(self, _link: str):
        """Delete cost from storage"""
        pass
    def get(self):
        """Returns all costs from storage"""
        pass
    def toString(self):
        """Returns all costs from storage in formatted string"""
        pass
    
class Invoice(IInvoiceInterface):

    def __init__(self, params=None):
        
        self.storage = list()
        if isinstance(params, dict):
            if params is not None:
               self.add(params)
        elif isinstance(params, (set, list, tuple)):
            for item in params:
                if item is not None:
                   self.add(item)
    
    def makeObjType(self, _objects):
        if(isinstance(_objects, (list, tuple, set))):
            for item in _objects:
                if item is not None:
                    item.update({ 'obj_type': '{}'.format(self.__class__.__name__) })      
        elif(isinstance(_objects, (dict))):
            _objects.update({ 'obj_type': '{}'.format(self.__class__.__name__) })
        else:
            raise Exception("Object was'nt dictionary or iterable item")
        
    def find(self, _link:str, _type_name = None):
        for item in self.storage:
            if item['info'] == _link and item['obj_type'] == _type_name:
                return item
            
    def valueChek(self, _object:dict):
        if not (_object['time'] and _object['summ'] and _object['info'] ):
            raise ValueError("Object what adds wasn't fullfiled")
        if _object.get('obj_type') is None:
            raise ValueError("Object what adds wasn't fullfiled on key 'obj_type'")
        if _object['summ'] < 0:
            raise ValueError("Object what adds had summ less than zero") 
        return True

    def add(self, _objects: dict):
        if isinstance(_objects, (list, tuple, set)): 
            for item in _objects:
                self.add(item)
        elif isinstance(_objects, (dict)):
            if _objects.get('obj_type') is None:
                self.makeObjType(_objects)
            if self.valueChek(_objects):
                self.storage.append(_objects)
     
    def edit(self, _link: str, _objects:dict):
        if _objects.get('obj_type') is None:
            self.makeObjType(_objects)
        
        if self.valueChek(_objects):
            item = self.find(_link, _objects['obj_type'])
            if item:
                item.update(_objects)
    def remove(self, index: int):
        del self.storage[index]
        
        
    '''def remove(self, _link: str):
        item = self.find(_link, self.__class__.__name__)
        if item:
            self.storage.remove(item)'''

    def get(self):
        return self.storage

    def toString(self):
        _tittle = _log=''
        if self and self.storage:
            i=0
            for item in self.storage:
                i+=1
                _log += "\t\nnumber: {};\n".format( i )
                for key, val in item.items():
                    if key=='obj_type':
                        _tittle = val
                    else:
                        _log += "\t{}: {};\n".format( key, val)
            return _tittle + '\n' +_log
        else:
            return 'Current storage is empty'
        
class Expenses(Invoice):
    pass
class Income(Invoice):
    pass
class Plan_Expenses(Invoice):
    pass
class Plan_Income(Invoice):
    pass

