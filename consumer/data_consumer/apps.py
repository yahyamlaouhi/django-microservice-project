from django.apps import AppConfig


class DataConsumerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "data_consumer"

    def ready(self):
        import data_consumer.signals

        data_consumer.signals.__name__
