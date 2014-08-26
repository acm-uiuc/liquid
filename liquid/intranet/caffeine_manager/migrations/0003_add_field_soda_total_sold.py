# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Soda.total_sold'
        db.add_column('caffeine_manager_soda', 'total_sold',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=11),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Soda.total_sold'
        db.delete_column('caffeine_manager_soda', 'total_sold')


    models = {
        'caffeine_manager.soda': {
            'Meta': {'object_name': 'Soda'},
            'caffeine': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'calories': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '11'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'default': '0.5', 'max_digits': '6', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'total_sold': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '11'})
        },
        'caffeine_manager.tray': {
            'Meta': {'object_name': 'Tray'},
            'detect_override': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'max_length': '11'}),
            'soda': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['caffeine_manager.Soda']", 'null': 'True', 'blank': 'True'}),
            'tray_number': ('django.db.models.fields.IntegerField', [], {'max_length': '11'})
        }
    }

    complete_apps = ['caffeine_manager']