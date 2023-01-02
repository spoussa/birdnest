from django.apps import AppConfig

class HelloConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hello'
    thread = None
    def ready(self): # in the ready function we start a thread to update the database of NDZ violators
        import get
        import threading
        import sys
        if "runserver" in sys.argv:
            self.thread = threading.Thread(target = get.violators)
            print("starting thread")
            self.thread.daemon = True
            self.thread.start()
            
        
