from django.apps import AppConfig


class CustomerConfig(AppConfig):
    name = 'customer'
    def ready(self):
        print('signal is ready grey')
        import customer.signals
