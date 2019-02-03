SUIT_CONFIG = {
    'ADMIN_NAME': 'Unlock Repair Phone Shop Manager',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': False,
    'SEARCH_URL': '',
    'MENU': (
        # Shop
        {
            'label': 'Shop', 'icon': 'icon-shopping-cart',
            'models': ('shop.shop', ),
            'permissions': ('shop.add_shop', 'shop.change_shop')
        },
        #Server
        {
            'label': "Unlock'n Servers", 'icon': 'icon-bold',
            'models': ('server.server', )
        },
        #Charges
        {
            'label':"URPSM Charges",'icon':'icon-question-sign',
            'url':'/urpsmadminp/urpms-charges'

        },
        {
            'label':"Action History",'icon':'icon-list',
            'url':'/urpsmadminp/actionhistory'

        },
        #Invoices
        {
          'label':"Deposit Invoices",'icon':'icon-picture',
            'url':'/urpsmadminp/view-shop-invoices'
        },
    {
            'label': "Deposits", 'icon': 'icon-leaf',
            'models': [{
          'label':"Edit Site Texts",
            'url':'/urpsmadminp/edit-site'
        },
        {
            'label':"Edit deposit info",
            'url':'/urpsmadminp/edit-deposit-info'
        }]
        },
        #Edit Site Text

        # Components
        {
            'label': 'Component', 'icon': 'icon-th-large',
            'models': ('component.component', 'component.type', ),
            'permissions': ('component.add_component', 'component.change_component',
                            'component.add_type', 'component.change_type')
        },
        # Clients
        {
            'label': 'Client', 'icon': 'icon-user',
            'models': ('client.client', 'client.addon', 'client.image', ),
            'permissions': ('client.add_client', 'client.change_client',
                            'client.add_addon', 'client.change_addon',
                            'client.add_image', 'client.change_image')
        },
        # Phones
        {
            'label': 'Phone', 'icon': 'icon-fire',
            'models': ('phone.brand', 'phone.model', 'phone.picture', ),
            'permissions': ('phone.add_brand', 'phone.change_brand',
                            'phone.add_model', 'phone.change_model',
                            'phone.add_picture', 'phone.change_picture')
        },
        # Orders
        {
            'label': 'Orders', 'icon': 'icon-list-alt',
            'models': ('order.serverorder', ),
            'permissions': ('order.add_serverorder', 'order.change_serverorder')
        },
        {
            'label': 'Payment', 'icon': 'icon-picture',
            'models': ('payment.serverpaymenttransaction','payment.shoppaymenttransaction' ),
            'permissions': ('payment.add_serverpaymenttransaction', 'payment.change_serverpaymenttransaction',
                            'payment.add_shoppaymenttransaction', 'payment.change_shoppaymenttransaction')
        },
        {
            'label': 'Ticket', 'icon': 'icon-picture',
            'models': ('ticket.orderticket','ticket.message'),
            'permissions': ('ticket.add_orderticket', 'ticket.change_orderticket',
                            'ticket.add_message', 'ticket.change_message')
        },
        {
            'app': 'ipn', 'icon': 'icon-lock',
            },
        {
            'label': 'EndPoint API', 'icon': 'icon-tint',
            'models': ('endpoint.endpoint',),
            'permissions': ('endpoint.add_endpoint', 'endpoint.change_endpoint')
        },
        {
            'label': 'Adverts', 'icon': 'icon-picture',
            'models': ('shop.banner', ),
            'permissions': ('shop.add_banner', 'shop.change_banner')
        },
        #reviews
        {
            'label': 'Reviews', 'icon': 'icon-leaf',
            'models': ('ureview.shopreview', 'ureview.serverreview' ,)
        },
        {
            'label': 'Coming soon', 'icon': 'icon-time',
            'models': ('launch.launchrock', )
        },
        {
          'label':'SEO','icon':'icon-picture',
            'url':'/urpsmadminp/edit-meta-tags'
        },

        '-',

        {
            'label': 'Settings', 'icon': 'icon-cog',
            'models': ('auth.user', 'auth.group', 'sites.site', ),
            'permissions': ('auth.add_user', 'auth.add_group', 'sites.add_site',
                            'auth.change_user', 'auth.change_group', 'sites.change_site')
        },
        '-',
        {
            'label': 'Geography', 'icon': 'icon-globe',
            'models': ('simplecities.country', 'simplecities.city',  )
        },
        '-',
        {
            'label': 'Contact', 'icon': 'icon-phone',
            'models': ('public.contact',  {
          'label':"Messages",
            'url':'/urpsmadminp/adminmessages/'
        })
        }


    )
}
