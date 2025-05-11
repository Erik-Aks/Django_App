from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'  # Должно совпадать с именем папки
    label = 'accounts'  # Уберите 'my_unique_accounts', если было