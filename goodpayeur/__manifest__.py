# -*- coding: utf-8 -*-
{
    'name': "goodpayeur",

    'summary': """
    Report Payments date for customers and retrieve a global score for existing payments
    """,

    'description': """
    Ce module ajoute, dans paramétres généraux (configuration -> paramètres généraux) une section 'goodpayeur integration' dans laquelle sont attendus:
    - l'url de base de goodpayeur (https://staging-api.goodpayeur.com pour le test et https://api.goodpayeur.com pour la production)
    - Le nom d'utilisateur
    - Le mot de passe

    Ensuite, il convient de selectionner les clients pour lesquels on veut avoir la traçabilité good payeur.
    Cela peut se faire, soit manuellement, dans l'en tête du contact, soit via un assistant, depuis la vue liste des contacts, fait une recherche, filtre les contacts de type company, selectionne ceux que l'on veut, et on clique sur action -> 'goodpayeur sync' 
    *A noter qu'il faut que le contact ait un numero de siren valide, sinon il ne se passera rien.*
    
    Quand on fait un nouveau devis à un client 'synchronisé', alors, en haut a droite s'affiche son score goodpayeur (avec une possibilité de le rafraichir)
    
    Quand on fait une facture à ce client, alors, un jour aprés la validation de celle ci, elle est envoyée à good payeur.
    Quand le paiement est fait, ce dernier est également envoyé à goodpayeur. (via un cron, qui tourne toutes les heures)
    Dans l'onglet goodpayeur de la facture, il est possible de consulter des infos sur l'état goodpayeur de la facture (et de l'annuler)

    """,

    'author': "Auneor Conseil",
    'website': "http://www.auneor-conseil.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Invoicing &amp; Payments',
    'version': '0.1',

    # any module necessary for this one to work correctly
#    'depends': ['l10n_fr_siret'],
    'depends': ['sovauda_contract'],
    'external_dependencies': {'python': ['requests_oauthlib']},

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/res_config.xml',
        'views/sale_order.xml',
        'views/account_invoice.xml',
        'views/res_partner.xml',
        'views/cron.xml',
        'views/wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
