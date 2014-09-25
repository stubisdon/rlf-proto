from django.core import management
from django.contrib.staticfiles.management.commands.runserver \
    import Command as BaseCommand


class Command(BaseCommand):
    def inner_run(self, *args, **options):
        management.call_command('collectstatic', interactive=False)
        super(Command, self).inner_run(*args, **options)
