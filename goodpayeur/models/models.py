# -*- coding: utf-8 -*-

from odoo import models, fields, api
    # def _get_default_fcm_credentials(self):
    #     return self.env['base.config.settings'].get_default_fcm_credentials()

    # @api.model
    # def _push_notify_fcm(self, identities, message):
    #     # Divided into chunks because FCM supports only 1000 users in multi-cast
    #     message.ensure_one()
    #     identities_chunks = [identities[i:i+FCM_MESSAGES_LIMIT] for i in xrange(0, len(identities), FCM_MESSAGES_LIMIT)]
    #     payload = self._fcm_prepare_payload(message)
    #     for identities in identities_chunks:
    #         subscription_ids = identities.mapped('subscription_id')
    #         fcm_api_key = self._get_default_fcm_credentials()['fcm_api_key']

# class goodpayeur(models.Model):
#     _name = 'goodpayeur.goodpayeur'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
