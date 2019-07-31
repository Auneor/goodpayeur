# -*- coding: utf-8 -*-
from openerp import models, fields, api
from .connecteur import api_goodpayeur
import datetime
import logging

_logger = logging.getLogger(__name__)
import pprint


class AccountInvoiceGood(models.Model):
    _inherit = "account.invoice"
    textg = fields.Html(string="GOOD payeur info", copy=False, readonly=True)
    score_goodpayeur = fields.Html(
        "GOOD Payeur Score", related="partner_id.score_goodpayeur"
    )
    payment_date = fields.Date("Payment Date", compute="_compute_payment_date")
    sync_goodpayeur = fields.Boolean(
        "GOOD Payeur synchronisation", related="partner_id.sync_goodpayeur"
    )
    etat_goodpayeur = fields.Selection(
        [
            ("nothing", "Nothing to do"),
            ("to_send", "To be send"),
            ("sent", "Sent"),
            ("to_send_payed", "Payment to be send"),
            ("to_create_and_send_payed", "Payment+Invoice to be send"),
            ("sent_payed", "Payment sent"),
            ("to_delete", "To delete"),
            ("deleted", "Deleted"),
        ],
        copy=False,
        readonly="1",
        string="GOOD Payeur state",
        default="nothing",
        required=True,
        help="GOOD payeur state",
    )

    def _get_default_goodpayeur_credentials(self):
        return self.env["base.config.settings"].get_default_goodpayeur_credentials()

    def action_invoice_open(self):
        res = super(AccountInvoiceGood, self).action_invoice_open()
        if self.partner_id.sync_goodpayeur and self.type == "out_invoice":
            self.etat_goodpayeur = "to_send"
        return res

    def action_invoice_paid(self):
        res = super(AccountInvoiceGood, self).action_invoice_paid()
        #        _logger.info("la facture est payee")
        if self.partner_id.sync_goodpayeur:
            if self.etat_goodpayeur != "to_send":
                self.etat_goodpayeur = "to_send_payed"
            else:
                self.etat_goodpayeur = "to_create_and_send_payed"
        return res

    def send_goodpayeur(self):
        siren = self.partner_id.siren_goodpayeur
        _logger.info(str(self.partner_id) + str(self.partner_id.name))
        if not siren:
            _logger.info("pas de siren")
            return
        cred = self._get_default_goodpayeur_credentials()
        gpa = api_goodpayeur.GoodPayeurAPI(
            self,
            cred["goodpayeur_user"],
            cred["goodpayeur_password"],
            cred["goodpayeur_url"],
            cred["goodpayeur_token"],
        )
        datei = fields.Date.from_string(self.date_invoice)
        if datei == datetime.date.today():
            _logger.info(
                "on ne peut pas envoyer la facture "
                + self.number
                + " car la date est trop recente"
            )
            datei -= datetime.timedelta(1)
        #       return # TODO mettre ce code en action

        dico = {
            "identifier": siren,
            "invoice_number": self.number,
            "invoice_date": fields.Date.to_string(datei),
            # "2019-06-13",  # self.date_invoice,
            "due_date": self.date_due,
            "country": self.partner_id.country_id.code
            or self.env.user.company_id.country_id.code
            or "FR",
            "address": self.partner_id.street,
            "address2": self.partner_id.street2,
            "business_name": self.partner_id.name,
            "city": self.partner_id.city,
            "postal_code": self.partner_id.zip,
            "state": self.partner_id.state_id.name,
        }
        _logger.info(dico)
        res = gpa.create_invoice(dico)
        self.textg = pprint.pformat(res)
        if res:
            if self.etat_goodpayeur != "to_send":
                self.etat_goodpayeur = "to_send_payed"
            else:
                self.etat_goodpayeur = "sent"

    def send_payed_goodpayeur(self):
        cred = self._get_default_goodpayeur_credentials()
        gpa = api_goodpayeur.GoodPayeurAPI(
            self,
            cred["goodpayeur_user"],
            cred["goodpayeur_password"],
            cred["goodpayeur_url"],
            cred["goodpayeur_token"],
        )
        if self.payment_date and fields.Date.from_string(
            self.payment_date
        ) >= fields.Date.from_string(self.date_invoice):
            dap = self.payment_date
        else:
            dap = self.date_invoice
        dico = {"payment_date": dap}
        res = gpa.update_invoice(self.number, dico)
        _logger.info("update +" + str(res))
        if res:
            self.etat_goodpayeur = "sent_payed"

    def _compute_payment_date(self):
        for record in self:
            day = datetime.date(1970, 1, 1)
            for pay in record.payment_ids:
                if fields.Date.from_string(pay.payment_date) > day:
                    day = fields.Date.from_string(pay.payment_date)
            if day != datetime.date(1970, 1, 1):
                record.payment_date = fields.Date.to_string(day)

    def recup_info_good(self):
        cred = self._get_default_goodpayeur_credentials()
        gpa = api_goodpayeur.GoodPayeurAPI(
            self,
            cred["goodpayeur_user"],
            cred["goodpayeur_password"],
            cred["goodpayeur_url"],
            cred["goodpayeur_token"],
        )
        if self.number:
            #            self.textg = pprint.pformat()
            rep = gpa.get_invoice(self.number)
            li = []
            gpa.pretty_items(li, rep)
            self.textg = " ".join(li)

    def delete_good(self):
        cred = self._get_default_goodpayeur_credentials()
        gpa = api_goodpayeur.GoodPayeurAPI(
            self,
            cred["goodpayeur_user"],
            cred["goodpayeur_password"],
            cred["goodpayeur_url"],
            cred["goodpayeur_token"],
        )
        if self.number:
            self.textg = _("Deleted")
            gpa.delete_invoice(self.number)
            self.etat_goodpayeur = "deleted"

    def _cron_process_invoices(self):
        to_send = self.search(
            [("etat_goodpayeur", "in", ["to_send", "to_create_and_send_payed"])]
        )
        for t in to_send:
            _logger.info(t)
            t.send_goodpayeur()
        to_send_payed = self.search([("etat_goodpayeur", "=", "to_send_payed")])
        for t in to_send_payed:
            _logger.info("on a trouve les factures payees " + str(t))
            t.send_payed_goodpayeur()
            
    def force_good(self):
        for record in self:
            if record.etat_goodpayeur in  ["to_send", "to_create_and_send_payed"]:
                _logger.info("force goodpayeur sending "+str(record.id))
                record.send_goodpayeur()
                record.recup_info_good()
            elif record.etat_goodpayeur == "to_send_payed":
                _logger.info("force goodpayeur sending "+str(record.id))
                record.send_payed_goodpayeur()
                record.recup_info_good()
