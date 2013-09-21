# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Quote'
        db.create_table('quote_quote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quote_text', self.gf('django.db.models.fields.TextField')(max_length=700)),
            ('quote_sources', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('quote_source_html', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('quote', ['Quote'])


    def backwards(self, orm):
        
        # Deleting model 'Quote'
        db.delete_table('quote_quote')


    models = {
        'quote.quote': {
            'Meta': {'object_name': 'Quote'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quote_source_html': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'quote_sources': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quote_text': ('django.db.models.fields.TextField', [], {'max_length': '700'})
        }
    }

    complete_apps = ['quote']
