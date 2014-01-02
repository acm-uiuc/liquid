# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Quote.quote_posters'
        db.add_column('quote_quote', 'quote_posters', self.gf('django.db.models.fields.CharField')(default='', max_length=100), keep_default=False)

        # Adding field 'Quote.quote_poster_html'
        db.add_column('quote_quote', 'quote_poster_html', self.gf('django.db.models.fields.CharField')(default='', max_length=200), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Quote.quote_posters'
        db.delete_column('quote_quote', 'quote_posters')

        # Deleting field 'Quote.quote_poster_html'
        db.delete_column('quote_quote', 'quote_poster_html')


    models = {
        'quote.quote': {
            'Meta': {'object_name': 'Quote'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quote_poster_html': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'quote_posters': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quote_source_html': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'quote_sources': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'quote_text': ('django.db.models.fields.TextField', [], {'max_length': '700'})
        }
    }

    complete_apps = ['quote']
