# -*- coding: UTF-8 -*-

import unittest

from south.db import db
from south.tests import Monkeypatcher
from south.tests.fakeapp.models import HorribleModel, Other1, Other2

from south.modelsparser import get_model_fields, get_model_meta

class TestModelParsing(Monkeypatcher):

    """
    Tests parsing of models.py files against the test one.
    """
    
    def test_fields(self):
        
        fields = get_model_fields(HorribleModel)
        self.assertEqual(
            fields,
            {
                'id': ('models.AutoField', [], {'primary_key': 'True'}),
                
                'name': ('models.CharField', [], {'max_length': '255'}), 
                'short_name': ('models.CharField', [], {'max_length': '50'}),
                'slug': ('models.SlugField', [], {'unique': 'True'}), 
                
                'o1': ('models.ForeignKey', ['Other1'], {}),
                'o2': ('models.ForeignKey', ["'Other2'"], {}),
                
                'user': ('models.ForeignKey', ['User'], {'related_name': '"horribles"'}),
                
                'code': ('models.CharField', [], {'max_length': '25', 'default': '"↑↑↓↓←→←→BA"'}),
                
                'choiced': ('models.CharField', [], {'max_length': '20', 'choices': 'choices'}),
                
                'multiline': ('models.TextField', [], {}),
            },
        )
        
        fields2 = get_model_fields(Other2)
        self.assertEqual(
            fields2,
            {'close_but_no_cigar': ('models.PositiveIntegerField', [], {'primary_key': 'True'})},
        )
        
        fields3 = get_model_fields(Other1)
        self.assertEqual(
            fields3,
            {'id': ('models.AutoField', [], {'primary_key': 'True'})},
        )
    
    
    def test_meta(self):
        
        meta = get_model_meta(HorribleModel)
        self.assertEqual(
            meta,
            {'db_table': '"my_fave"', 'verbose_name': '"Dr. Strangelove,"+"""or how I learned to stop worrying\nand love the bomb"""'},
        )