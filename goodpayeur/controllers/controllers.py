# -*- coding: utf-8 -*-
from odoo import http

# class Goodpayeur(http.Controller):
#     @http.route('/goodpayeur/goodpayeur/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/goodpayeur/goodpayeur/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('goodpayeur.listing', {
#             'root': '/goodpayeur/goodpayeur',
#             'objects': http.request.env['goodpayeur.goodpayeur'].search([]),
#         })

#     @http.route('/goodpayeur/goodpayeur/objects/<model("goodpayeur.goodpayeur"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('goodpayeur.object', {
#             'object': obj
#         })