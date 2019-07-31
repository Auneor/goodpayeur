# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from .connecteur import api_goodpayeur
import datetime


class ResPartnerGood(models.Model):
    _inherit = "res.partner"
    sync_goodpayeur = fields.Boolean(
        "Synchronized with GOOD Payeur", copy=False, default=True
    )
    last_goodpayeur_update = fields.Date(
        "Last GOOD Payeur update", readonly="1", copy=False
    )
    score_goodpayeur = fields.Html(
        "GOOD Payeur Score",
        readonly="1",
        copy=False,
        help="Number between 0 and 100 that reflects the payment behaviour of a company",
    )
    siren_goodpayeur = fields.Char("Siren", compute="_get_siren_good", copy=False)
    success_good = fields.Boolean("Fetching is successfull", default=False)
    details_goodpayeur = fields.Html("Details", readonly="1")

    def _get_siren_good(self):
        st = _("credit_limit")
        for record in self:
            if record.siret:
                siret = record.siret.replace(" ", "")
                siret = siret.strip()
                siren = siret[:9]
                if len(siren) == 9:
                    record.siren_goodpayeur = siren
                    continue
                record.siren_goodpayeur = ""

    def _get_default_goodpayeur_credentials(self):
        return self.env["base.config.settings"].get_default_goodpayeur_credentials()

    def _get_color(self, value):
        if value < 50:
            color = "#ff8566"
        elif value < 70:
            color = "yellow"
        else:
            color = "#80ff80"
        res = (
            "<h2>"
            + _("Goodpayeur Score: ")
            + "<span style='background-color:"
            + color
            + "'>"
            + str(value)
            + "<span></h2>"
        )
        return res

    def fetch_good(self):
        cred = self._get_default_goodpayeur_credentials()
        gpa = api_goodpayeur.GoodPayeurAPI(
            self,
            cred["goodpayeur_user"],
            cred["goodpayeur_password"],
            cred["goodpayeur_url"],
            cred["goodpayeur_token"],
        )

        if self.country_id:
            code = self.country_id.code
        else:
            code = "FR"

        succedeed, rep = gpa.get_info(self.siren_goodpayeur, code)
        self.last_goodpayeur_update = datetime.date.today()
        if succedeed:
            self.score_goodpayeur = self._get_color(rep["score"])
            li = []
            gpa.pretty_items(li, rep)
            self.details_goodpayeur = " ".join(li)
            self.success_good = True
        else:
            chaineatrad = [
                _("Requested business could not be found"),
                _("Requested country is not supported"),
            ]
            self.success_good = False

            if u"error" in rep:
                self.score_goodpayeur = rep[u"error"]
