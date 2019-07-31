# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo.tools.translate import _
from odoo.tools import email_split
from odoo.exceptions import UserError

from odoo import api, fields, models


_logger = logging.getLogger(__name__)


class GoodpayeurWizard(models.TransientModel):
    """
        A wizard to manage the creation/removal of goodpayeur users.
    """

    _name = "goodpayeur.wizard"
    _description = "Goodpayeur Access Management"

    @api.multi
    def action_apply(self):
        print(self.env.context)
        self.env["res.partner"].browse(self.env.context["active_ids"]).write(
            {"sync_goodpayeur": True}
        )
        return {"type": "ir.actions.act_window_close"}
