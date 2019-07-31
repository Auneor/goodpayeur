# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime


class SaleOrderGood(models.Model):
    _inherit = "sale.order"
    score_goodpayeur = fields.Html(
        "Score Goodpayeur", related="partner_id.score_goodpayeur", readonly="1"
    )
    sync_goodpayeur = fields.Boolean(
        "Synchronisé avec Goodpayeur",
        related="partner_id.sync_goodpayeur",
        readonly="1",
    )
    last_goodpayeur_update = fields.Date(
        "Derniere date d'update",
        related="partner_id.last_goodpayeur_update",
        readonly="1",
    )

    def fetch_good(self):
        if self.partner_id:
            self.partner_id.fetch_good()
