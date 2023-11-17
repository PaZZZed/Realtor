from django.contrib.auth.models import User
import xmlrpc.client

URL = "http://localhost:8069"
DB = "dev01"
UID = 0
COMMON = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(URL), allow_none=1)

class OdooRpc(object):

    def authenticate(username=None, password=None):
        user = None
        try:
            UID = COMMON.authenticate(DB,username,password,{})
            if UID == 0:
                raise Exception('Pssword or username incorrect!')
            else:
                print('======= UID: ',UID)
                user = User.objects.get(id=UID)
                    
        except User.DoesNotExist:
            print('======= NEW UID: ',UID)
            user = User.objects.create(username=username,password=password, id=UID)
            user.save()

        return user
        
    def get_appartments(self, user_id):
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL))
        password  = User.objects.get(id=user_id).password
        email = User.objects.get(id=user_id).username

        UID = COMMON.authenticate(DB,email,password,{}) 
        print('======= APT UID: ',UID)
        models.execute_kw(DB, UID, password ,'realtor.appartment', 'check_access_rights',['read'], {'raise_exception': False})
        appartments = models.execute_kw(DB, UID, password, 'realtor.appartment', 'search_read', [[]])
        return appartments
    
    def get_quantites(self, user_id):
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL))
        password  = User.objects.get(id=user_id).password
        email = User.objects.get(id=user_id).username

        UID = COMMON.authenticate(DB,email,password,{}) 
        print('======= QTIES UID: ',UID)
        appartments = self.get_appartments(self, user_id=user_id)
        all_quantities = {}
        for appartment in appartments:
            products = models.execute_kw(DB, UID, password, 'product.product', 'search_read', [[['appartment_id', '=', appartment.get("id") ]]])
            for product in products:
                stock =  models.execute_kw(DB, UID, password, 'stock.inventory.line', 'search_read', [[['product_id', '=', product.get("id") ]]])
                for s in stock :
                    all_quantities.update({appartment.get("id") : int(s.get("product_qty"))})
        return all_quantities
    
    def create_offer(user_id, bid_offer , appartment_id):
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL))
        password  = User.objects.get(id=user_id).password
        email = User.objects.get(id=user_id).username
        UID = COMMON.authenticate(DB,email,password,{})
        models.execute_kw(DB, UID, password ,'realtor.appartment', 'write',
                                        [[appartment_id], {'best_offer_amount': bid_offer, 'best_offer_buyer' : UID}])
        
    def get_offer_apart(self, user_id, appartment_id):
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(URL))
        password  = User.objects.get(id=user_id).password
        email = User.objects.get(id=user_id).username
        UID = COMMON.authenticate(DB,email,password,{})
        record = models.execute_kw(DB, UID, password, 'realtor.appartment', 'read', [[appartment_id]])
        return record