#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from projeto1.middlewares import set_db_for_router

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto1.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    for index, arg in enumerate(sys.argv):
        param = arg.split('=')
        if '--database' in param and len(param) == 2:
            db = param[1]
            set_db_for_router(db)
            del sys.argv[index]
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
