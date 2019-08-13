# -*- coding: utf-8 -*-
from openerp import models, fields, api


class FcmResConfig(models.TransientModel):
    _inherit = "base.config.settings"
    goodpayeur_url = fields.Char("URL")
    goodpayeur_user = fields.Char("User")
    goodpayeur_password = fields.Char("Password")
    goodpayeur_token = fields.Char("Token")
    # fcm_api_key = fields.Char("Server API Key")
    # fcm_project_id = fields.Char("Sender ID")

    @api.multi
    def set_goodpayeur_url(self):
        goodpayeur_url = self[0].goodpayeur_url or ""
        self.env["ir.config_parameter"].set_param(
            "goodpayeur_token", "", groups=["base.group_system"]
        )
        self.env["ir.config_parameter"].set_param(
            "goodpayeur_url", goodpayeur_url, groups=["base.group_system"]
        )

    @api.multi
    def set_goodpayeur_token(self):
        goodpayeur_token = self[0].goodpayeur_token or ""
        self.env["ir.config_parameter"].set_param(
            "goodpayeur_token", goodpayeur_token, groups=["base.group_system"]
        )

    @api.multi
    def set_goodpayeur_user(self):
        goodpayeur_user = self[0].goodpayeur_user or ""
        self.env["ir.config_parameter"].set_param(
            "goodpayeur_token", "", groups=["base.group_system"]
        )
        self.env["ir.config_parameter"].set_param(
            "goodpayeur_user", goodpayeur_user, groups=["base.group_system"]
        )

    @api.multi
    def set_goodpayeur_password(self):
        goodpayeur_password = self[0].goodpayeur_password or ""
        self.env["ir.config_parameter"].set_param(
            "goodpayeur_token", "", groups=["base.group_system"]
        )

        self.env["ir.config_parameter"].set_param(
            "goodpayeur_password", goodpayeur_password, groups=["base.group_system"]
        )

    @api.multi
    def get_default_goodpayeur_credentials(self, fields=None):
        get_param = self.env["ir.config_parameter"].sudo().get_param
        goodpayeur_url = get_param("goodpayeur_url", default="")
        goodpayeur_token = get_param("goodpayeur_token", default="")
        goodpayeur_user = get_param("goodpayeur_user", default="")
        goodpayeur_password = get_param("goodpayeur_password", default="")
        return {
            "goodpayeur_password": goodpayeur_password,
            "goodpayeur_url": goodpayeur_url,
            "goodpayeur_token": goodpayeur_token,
            "goodpayeur_user": goodpayeur_user,
        }
