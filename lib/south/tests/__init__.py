
import unittest
from django.conf import settings

# Note: the individual test files are imported below this.

class Monkeypatcher(unittest.TestCase):

    """
    Base test class for tests that play with the INSTALLED_APPS setting at runtime.
    """

    def create_fake_app(self, name):
        
        class Fake:
            pass
        
        fake = Fake()
        fake.__name__ = name
        return fake


    def create_test_app(self):
        
        class Fake:
            pass
        
        fake = Fake()
        fake.__name__ = "fakeapp.migrations"
        fake.__file__ = os.path.join(test_root, "fakeapp", "migrations", "__init__.py")
        return fake
    
    
    def monkeypatch(self):
        """Swaps out various Django calls for fake ones for our own nefarious purposes."""
        
        def new_get_apps():
            return ['fakeapp']
        
        from django.db import models
        from django.conf import settings
        models.get_apps_old, models.get_apps = models.get_apps, new_get_apps
        settings.INSTALLED_APPS, settings.OLD_INSTALLED_APPS = (
            ["fakeapp"],
            settings.INSTALLED_APPS,
        )
        self.redo_app_cache()
    setUp = monkeypatch
    
    
    def unmonkeypatch(self):
        """Undoes what monkeypatch did."""
        
        from django.db import models
        from django.conf import settings
        models.get_apps = models.get_apps_old
        settings.INSTALLED_APPS = settings.OLD_INSTALLED_APPS
        self.redo_app_cache()
    tearDown = unmonkeypatch
    
    
    def redo_app_cache(self):
        from django.db.models.loading import AppCache
        a = AppCache()
        a.loaded = False
        a._populate()

# Try importing all tests if asked for (then we can run 'em)
try:
    skiptest = settings.SKIP_SOUTH_TESTS
except:
    skiptest = False

if not skiptest:
    from south.tests.db import *
    from south.tests.logic import *
    from south.tests.modelsparser import *