from app import webapp
from app import mysql


class Item():
    def __init__(self, item_id):
        self.item_id = int(item_id)
        self.data = self.getData() 

    def __getattr__(self, field):
        if field in self.data:
            return self.data[field]
        else:
            return None

    def getData(self):
        obj_cursor = mysql.connect().cursor()
        obj_cursor.execute("SELECT * FROM items WHERE item_id = %d" %(self.item_id))
        data = fetchOneAssoc(obj_cursor)
        data['price'] = float(data['price']) if data['price'] else data['price']
        data['security_deposit'] = 0#self.getSecurityDepositAmount()

        return data


    def getObj(self):
        item_obj = vars(self)
        item_obj = item_obj['data']
        item_obj['item_id'] = self.item_id
        
        item_obj = self.getTempVarsForBookModel(item_obj)

        return item_obj

    def getSecurityDepositAmount(self):
        security = 0
        if self.data['price']:
            security = max(1000, 0.5*self.data['price'])

        return security

    def getTempVarsForBookModel(self, item_obj):
        item_obj['isbn'] = item_obj['ISBN-10']
        item_obj['title'] = item_obj['item_name']
        item_obj['cover'] = ''
        item_obj['reviews'] = ''
        item_obj['deposit'] = item_obj['security_deposit']
        item_obj['delivery'] = 0
        item_obj['available_in_hours'] = 3
        item_obj['bound'] = ''
        item_obj['year'] = 2014
        item_obj['photos'] = []
        item_obj['return_days'] = []
        item_obj['rating_avg'] = int(item_obj['ratings'][0]) if item_obj['ratings'] else 0
        item_obj['rating_numbers'] = item_obj['num_ratings']
        
        del item_obj['ASIN']
        del item_obj['ISBN-10']
        del item_obj['ISBN-13']
        del item_obj['item_name']
        del item_obj['language']
        del item_obj['num_ratings']
        del item_obj['ratings']
        del item_obj['price']
        
        return item_obj

'''
Generic helpers
'''
def fetchOneAssoc(cursor) :
    data = cursor.fetchone()
    if data == None :
        return None
    desc = cursor.description

    dict = {}

    for (name, value) in zip(desc, data) :
        dict[name[0]] = value

    return dict


