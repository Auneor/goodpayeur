import json
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import TokenExpiredError
from openerp import models, fields, api, _


class GoodPayeurAPI:
    def __init__(self, oneselfodoo, client_id, client_secret, base_url, token=""):
        self.client_id = client_id
        self.oneselfodoo = oneselfodoo
        self.client_secret = client_secret
        self.base_url = base_url
        self.token = token
        self.authorize_service = base_url + "/oauth/token"
        self.scopes = ["*"]
        if not token:
            self.refresh_token()

    def pretty_items(
        self,
        r,
        d,
        nametag="<strong>%s: </strong>",
        itemtag="<li>%s</li>",
        valuetag="%s",
        blocktag=("<ul>", "</ul>"),
    ):
        to_translate = [
            _("count_invoices_tracked"),
            _("due_date"),
            _("credit_limit"),
            _("legal_information"),
            _("name"),
            _("economic_activity"),
            _("creation_date"),
            _("address"),
            _("city"),
            _("country"),
            _("postal_code"),
            _("complete_country"),
            _("address"),
            _("identifier"),
            _("juridical_nature"),
            _("average_late_delay_sector"),
            _("financial_status"),
            _("has_dgccrf_convictions"),
            _("paid_in_terms"),
            _("score"),
            _("generated_date"),
            _("average_late_delay"),
            _("has_signed_goodpayeur_charter"),
            _("financial_solidity"),
            _("has_badpayeur_claims"),
            _("payment_date"),
            _("due_date"),
            _("address2"),
            _("address"),
            _("invoice_date"),
            _("state"),
            _("economic_sector_code"),
            _("business_name"),
            _("times_recontacted"),
            _("invoice_number"),
            _("True"),
            _("False"),
        ]
        if isinstance(d, dict):
            r.append(blocktag[0])
            for k, v in d.iteritems():
                #                print(k)
                name = nametag % _(k)
                if isinstance(v, dict) or isinstance(v, list):
                    r.append(itemtag % name)
                    self.pretty_items(r, v)
                else:
                    value = valuetag % v
                    r.append(itemtag % (name + value))
            r.append(blocktag[1])
        elif isinstance(d, list):
            r.append(blocktag[0])
            for i in d:
                if isinstance(i, dict) or isinstance(i, list):
                    r.append(itemtag % " - ")
                    self.pretty_items(r, i)
                else:
                    r.append(itemtag % i)
            r.append(blocktag[1])

    def refresh_token(self):
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        self.token = str(
            oauth.fetch_token(
                token_url=self.authorize_service,
                client_id=self.client_id,
                client_secret=self.client_secret,
            )
        )
        self.oneselfodoo.env["ir.config_parameter"].set_param(
            "goodpayeur_token", self.token, groups=["base.group_system"]
        )

    def get_info(self, siren, country="FR"):
        url = self.base_url + "/public/report"
        try:
            #            print(eval(self.token))
            client = OAuth2Session(self.client_id, token=eval(self.token))
            # print(url)
            # print(self.token)
            res = client.get(url, params={"identifier": siren, "country": country})
        except TokenExpiredError as e:
            self.refresh_token()
            client = OAuth2Session(self.client_id, token=eval(self.token))
            res = client.get(url)
        print(res.status_code)
        print(res.text)
        if res.status_code == 200:
            return True, res.json()  # request succeded
        else:
            return False, res.json()

    #        return res.status_code == 200 and res.json() or None

    def create_invoice(self, dico):
        req = []
        for k, v in dico.items():
            if v:
                req.append((k, (None, (v))))
        try:
            #           print(self.token)
            client = OAuth2Session(self.client_id, token=eval(self.token))
            #          print(req)
            rep = client.post(url=self.base_url + "/public/depot", files=req)
        except TokenExpiredError as e:
            self.refresh_token()
            client = OAuth2Session(self.client_id, token=eval(self.token))
            rep = client.post(url=self.base_url + "/public/depot", files=req)
        #     print(rep, rep.status_code, rep.reason)
        return rep.status_code == 200 and rep.json() or None

    def get_invoice(self, number):
        url = self.base_url + "/public/depot/" + number
        try:
            client = OAuth2Session(self.client_id, token=eval(self.token))
            res = client.get(url)
        except TokenExpiredError as e:
            self.refresh_token()
            client = OAuth2Session(self.client_id, token=eval(self.token))
            res = client.get(url)
        return res.status_code == 200 and res.json() or None

    def update_invoice(self, number, dico):
        url = self.base_url + "/public/depot/" + number
        #        print(url)
        try:
            client = OAuth2Session(self.client_id, token=eval(self.token))
            rep = client.put(url, params=dico)
        except TokenExpiredError as e:
            self.refresh_token()
            client = OAuth2Session(self.client_id, token=eval(self.token))
            rep = client.put(url, params=dico)
        #       print("update done")
        #       print(rep, rep.status_code, rep.reason)
        return rep.status_code == 200

    def delete_invoice(self, number):
        url = self.base_url + "/public/depot/" + number
        try:
            client = OAuth2Session(self.client_id, token=eval(self.token))
            rep = client.delete(url)
        except TokenExpiredError as e:
            self.refresh_token()
            client = OAuth2Session(self.client_id, token=eval(self.token))
            rep = client.delete(url)
        #    print(rep, rep.status_code, rep.reason, rep.text)
        return rep.status_code == 200 and rep.json() or None
