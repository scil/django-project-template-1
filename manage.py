#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ project_name }}.settings')
    
    # hack scil
    # to use this var DJANGO_SETTINGS_MODULE
    import environ
    root = environ.Path(__file__) - 1
    env = environ.Env(DEBUG=(bool, False), )  # set default values and casting
    environ.Env.read_env(root('.env'))  # reading .env file

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            'Couldn\'t import Django. Are you sure it\'s installed and '
            'available on your PYTHONPATH environment variable? Did you '
            'forget to activate a virtual environment?') from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
