import threading
from .utils import tenant_db_from_the_request

Thread_Local = threading.local()


class DatabaseRouteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        db = tenant_db_from_the_request(request)
        setattr(Thread_Local, "db", db)
        request.session["rede"] = db
        response = self.get_response(request)
        return response


def get_current_db_name():
    return getattr(Thread_Local, "db", None)


def set_db_for_router(db):
    setattr(Thread_Local, "db", db)
