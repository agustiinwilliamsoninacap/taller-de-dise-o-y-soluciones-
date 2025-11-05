#!/usr/bin/env python
import os
import sys

def main():
    # apunta al settings correcto dentro del paquete
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "mermeladas_django.mermeladas.settings",
    )
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
