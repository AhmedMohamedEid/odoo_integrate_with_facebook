# -*- coding: utf-8 -*-
from odoo import http

# class ../atec/facebookAndOdoo(http.Controller):
#     @http.route('/../atec/facebook_and_odoo/../atec/facebook_and_odoo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/../atec/facebook_and_odoo/../atec/facebook_and_odoo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('../atec/facebook_and_odoo.listing', {
#             'root': '/../atec/facebook_and_odoo/../atec/facebook_and_odoo',
#             'objects': http.request.env['../atec/facebook_and_odoo.../atec/facebook_and_odoo'].search([]),
#         })

#     @http.route('/../atec/facebook_and_odoo/../atec/facebook_and_odoo/objects/<model("../atec/facebook_and_odoo.../atec/facebook_and_odoo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('../atec/facebook_and_odoo.object', {
#             'object': obj
#         })