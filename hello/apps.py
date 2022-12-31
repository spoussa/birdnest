from django.apps import AppConfig

class HelloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hello'
    def ready(self):
        import get
        import threading
        thread = threading.Thread(target = get.violators)
        print("starting thread")
        thread.start()
        
