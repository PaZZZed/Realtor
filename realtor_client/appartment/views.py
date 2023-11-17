from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import OfferForm
from connection_config.odoo_rpc import OdooRpc
from django.http import HttpResponseRedirect
from django.contrib import messages
import logging
    

def apartAll(request) :
    try:
        id = str(request.user.id)
        appartments = OdooRpc.get_appartments(OdooRpc,user_id=id)
        quantities = OdooRpc.get_quantites(OdooRpc, user_id=id)
        form = OfferForm()
    except Exception:
        messages.error(request,"ERROR charging appartments, back to login!")
        logging.exception("Erreur lors du chargement des appartements")
        return HttpResponseRedirect('/')

    return render(request,"appartment/index.html",{'appartments' : appartments, 'quantities' : quantities,'form' :form})
        
        
def create(request,appart_id):
    form = OfferForm(request.POST)
    if form.is_valid():
        new_offer=form.cleaned_data['offer']
        try:
            user_id = str(request.user.id)
            old_offer = OdooRpc.get_offer_apart(OdooRpc,user_id=user_id,appartment_id=appart_id)
            best_offer = old_offer[0]["best_offer_amount"]

            if best_offer >= new_offer:
                raise Exception("La nouvelle offre doit être strictement supérieur à l'offre actuelle")

            OdooRpc.create_offer(user_id=user_id,bid_offer=new_offer,appartment_id=appart_id)
        except Exception:
            messages.error(request,"L'offre soumise doit être minimum de 90% du prix standard et supérieure à la meilleure offre actuelle !")
            logging.exception("Erreur lors de la soumission de l'offre !")
            
            

        return HttpResponseRedirect('/appartment')
  
    

 

