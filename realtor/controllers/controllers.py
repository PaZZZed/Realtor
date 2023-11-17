# -*- coding: utf-8 -*-
# from odoo import http


# class /mnt/extra-addons/realtor(http.Controller):
#     @http.route('//mnt/extra-addons/realtor//mnt/extra-addons/realtor/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//mnt/extra-addons/realtor//mnt/extra-addons/realtor/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/mnt/extra-addons/realtor.listing', {
#             'root': '//mnt/extra-addons/realtor//mnt/extra-addons/realtor',
#             'objects': http.request.env['/mnt/extra-addons/realtor./mnt/extra-addons/realtor'].search([]),
#         })

#     @http.route('//mnt/extra-addons/realtor//mnt/extra-addons/realtor/objects/<model("/mnt/extra-addons/realtor./mnt/extra-addons/realtor"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/mnt/extra-addons/realtor.object', {
#             'object': obj
#         })
