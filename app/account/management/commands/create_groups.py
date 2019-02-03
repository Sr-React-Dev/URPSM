from django.core.management.base import BaseCommand, CommandError
from mobilify import utils
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Create Groups for different access permissions'

    def handle(self, *args, **options):
        endpoint_monitor_group = Group.objects.get_or_create(name=utils.ENDPOINT_MONITOR_GROUP)[0]
        permissions = Permission.objects.filter(codename__in=['add_endpoint', 'change_endpoint'])
        for permission in permissions:
            endpoint_monitor_group.permissions.add(permission)
            self.stdout.write('added permission ' + permission.codename)
        self.stdout.write('Created endpoint monitor')

        shop_monitor_group = Group.objects.get_or_create(name=utils.SHOP_MONITOR_GROUP)[0]
        permissions = Permission.objects.filter(codename__in=['add_shop', 'change_shop', 'add_banner', 'change_banner'])
        for permission in permissions:
            shop_monitor_group.permissions.add(permission)
            self.stdout.write('added permission ' + permission.codename)
        self.stdout.write('Created shop monitor')

        order_monitor_group = Group.objects.get_or_create(name=utils.ORDER_MONITOR_GROUP)[0]
        permissions = Permission.objects.filter(codename__in=['add_serverorder', 'change_serverorder',
                                                              'add_shoporder', 'change_shoporder'])
        for permission in permissions:
            order_monitor_group.permissions.add(permission)
            self.stdout.write('added permission ' + permission.codename)
        self.stdout.write('Created order monitor')

        components_monitor_group = Group.objects.get_or_create(name=utils.COMPONENT_MONITOR_GROUP)[0]
        permissions = Permission.objects.filter(codename__in=['add_component', 'change_component',
                                                              'add_type', 'change_type'])
        for permission in permissions:
            components_monitor_group.permissions.add(permission)
            self.stdout.write('added permission ' + permission.codename)
        self.stdout.write('Created component monitor')

        clients_monitor_group = Group.objects.get_or_create(name=utils.CLIENT_MONITOR_GROUP)[0]
        permissions = Permission.objects.filter(codename__in=['add_client', 'change_client',
                                                              'add_addon', 'change_addon',
                                                              'add_image', 'change_image'])
        for permission in permissions:
            clients_monitor_group.permissions.add(permission)
            self.stdout.write('added permission ' + permission.codename)
        self.stdout.write('Created clients monitor')

        phone_monitor_group = Group.objects.get_or_create(name=utils.PHONE_MONITOR_GROUP)[0]
        permissions = Permission.objects.filter(codename__in=['add_brand', 'change_brand',
                                                              'add_model', 'change_model',
                                                              'add_picture', 'change_picture'])
        for permission in permissions:
            phone_monitor_group.permissions.add(permission)
            self.stdout.write('added permission ' + permission.codename)
        self.stdout.write('Created phone monitor')

        user_monitor_group = Group.objects.get_or_create(name=utils.USER_MONITOR_GROUP)[0]
        permissions = Permission.objects.filter(codename__in=['add_user', 'add_group', 'add_site',
                                                              'change_user', 'change_group', 'change_site'])
        for permission in permissions:
            user_monitor_group.permissions.add(permission)
            self.stdout.write('added permission ' + permission.codename)
        self.stdout.write('Created user monitor')

        paypal_ipn_monitor_group = Group.objects.get_or_create(name=utils.PAYPAL_IPN_MONITOR_GROUP)[0]
        permissions = Permission.objects.filter(codename__in=['add_paypalipn', 'change_paypalipn'])
        for permission in permissions:
            paypal_ipn_monitor_group.permissions.add(permission)
            self.stdout.write('added permission ' + permission.codename)
        self.stdout.write('Paypal IPN monitor')


        subcontractor_group = Group.objects.get_or_create(name=utils.SUBCONTRACTOR_GROUP)[0]
        permissions = Permission.objects.filter(codename__in=['add_endpoint', 'change_endpoint', 'add_brand',
                                                              'change_brand', 'add_client', 'change_client',
                                                              'add_addon', 'change_addon', 'add_image', 'change_image'
                                                              'add_model', 'change_model', 'add_picture',
                                                              'change_picture', 'add_component', 'change_component',
                                                              'add_type', 'change_type', 'add_serverorder',
                                                              'change_serverorder', 'add_shoporder', 'change_shoporder',
                                                              'add_shop', 'change_shop', 'add_banner', 'change_banner'])
        for permission in permissions:
            paypal_ipn_monitor_group.permissions.add(permission)
            self.stdout.write('added permission ' + permission.codename)
        self.stdout.write('Subcontractor group')





