import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')

def main():
    """Run administrative tasks."""
    # Check for the --app argument
    app_arg = None
    for arg in sys.argv:
        if arg.startswith("--app="):
            app_arg = arg.split("=")[1]
            sys.argv.remove(arg)  # Remove the custom argument to avoid errors

    if app_arg:
        os.environ["DJANGO_TARGET_APP"] = app_arg

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

# STARTING THE MICROSERVICES
# python manage.py runserver 127.0.0.1:8000 --app=datascraper
# python manage.py runserver 127.0.0.1:8001 --app=lstm
# python manage.py runserver 127.0.0.1:8002 --app=nlp
#TODO admin site