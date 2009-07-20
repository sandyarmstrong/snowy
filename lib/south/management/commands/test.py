from django.core import management
from django.core.management.commands import test
from django.core.management.commands import syncdb
from django.conf import settings

class Command(test.Command):
    
    def handle(self, *args, **kwargs):
        if not hasattr(settings, "SOUTH_TESTS_MIGRATE") or not settings.SOUTH_TESTS_MIGRATE:
            # point at the core syncdb command when creating tests
            # tests should always be up to date with the most recent model structure
            management.get_commands()
            management._commands['syncdb'] = 'django.core'
        super(Command, self).handle(*args, **kwargs)