import xmlrpc.client
import getpass

# Demande à l'utilisateur de saisir son login et son mot de passe (ou sa clé API)
db = 'dev01'
url = 'http://localhost:8069'
username = input("Entrez votre login : ")
password = getpass.getpass("Entrez votre mot de passe (ou votre clé API) : ")

# Se connecte à l'instance d'Odoo via XML-RPC
try:
	common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
	uid = common.authenticate(db,username,password,{})
	if uid == 0:
		raise Exception('Credentials are wrong for remote system access')
	else:
		message = 'Connection Stablished Successfully'
except Exception as e:
	print('Remote system access Issue \n ', e)

# Obtient l'objet "Appartement" (realtor.appartment)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

while True:
    # Demande à l'utilisateur de saisir le nom de l'appartement à rechercher
    name = input("Entrez le nom de l'appartement à rechercher (ou 'q' pour quitter) : ")
    if name == 'q':
        break

    # Recherche les appartements qui correspondent au nom saisi
    appartments = models.execute_kw(db, uid, password, 'realtor.appartment', 'search_read', [[['name', '=', name]]] )

    # Pour chaque appartement trouvé, affiche ses informations détaillées
    if len(appartments) ==  0:
        print("APPARTMENT NON TORUVE")
    else:
        for appartment in appartments:
            print("Nom de l'appartement : ", appartment.get("name"))
            print("Date de disponibilité : ", appartment.get("availability"))
            print("Description de l'appartement : ", appartment.get("description"))
            print("Prix de l'appartement : ", appartment.get("price"))
            print("Surface de l'appartement : ", appartment.get("surface"))
            print("Surface de la terrasse : ", appartment.get("terrace_surface"))
            print("Meilleure offre pour l'appartement : ", appartment.get("best_offer_amount"))

            products = models.execute_kw(db, uid, password, 'product.product', 'search_read', [[['appartment_id', '=',appartment.get("id") ]]])
            if len(products) == 0:
                print('Nous n\'avons pas cet appartement en stock')
            else:
                inventory_line =  models.execute_kw(db, uid, password, 'stock.inventory.line', 'search_read', [[['product_id', '=', products[0].get("id") ]]])
                print('Nous aovns: ', int(inventory_line[0].get("product_qty")),' appartments en stock pour votre recherche.')