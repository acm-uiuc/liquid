# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tray'
        db.create_table('trays_tray', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tray_number', self.gf('django.db.models.fields.IntegerField')(unique=True, max_length=11)),
            ('soda', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['soda.Soda'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=11)),
            ('price', self.gf('django.db.models.fields.DecimalField')(default=0.5, max_digits=10, decimal_places=2)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('detect_override', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('trays', ['Tray'])


    def backwards(self, orm):
        # Deleting model 'Tray'
        db.delete_table('trays_tray')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'intranet.member': {
            'Meta': {'object_name': 'Member', '_ormbases': ['auth.User']},
            'left_uiuc': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '255'}),
            'uin': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'soda.soda': {
            'Meta': {'object_name': 'Soda'},
            'caffeine': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '11'}),
            'calories': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '11'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'default': '0.5', 'max_digits': '6', 'decimal_places': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'total_sold': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '11'}),
            'votes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['intranet.Member']", 'symmetrical': 'False'})
        },
        'trays.tray': {
            'Meta': {'object_name': 'Tray'},
            'detect_override': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': '0.5', 'max_digits': '10', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '11'}),
            'soda': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['soda.Soda']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'tray_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '11'})
        }
    }

    complete_apps = ['trays']