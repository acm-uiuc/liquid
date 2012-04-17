# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Member'
        db.create_table('intranet_member', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('uin', self.gf('django.db.models.fields.CharField')(max_length=9, null=True)),
            ('left_uiuc', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='active', max_length=255)),
        ))
        db.send_create_signal('intranet', ['Member'])

        # Adding model 'Group'
        db.create_table('intranet_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date_formed', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('meeting_time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('meeting_day', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('meeting_location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('mailing_list', self.gf('django.db.models.fields.EmailField')(max_length=60)),
            ('status', self.gf('django.db.models.fields.CharField')(default='active', max_length=255)),
        ))
        db.send_create_signal('intranet', ['Group'])

        # Adding model 'GroupMember'
        db.create_table('intranet_groupmember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intranet.Group'])),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['intranet.Member'])),
            ('date_joined', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('is_chair', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.CharField')(default='active', max_length=255)),
        ))
        db.send_create_signal('intranet', ['GroupMember'])

        # Adding unique constraint on 'GroupMember', fields ['group', 'member']
        db.create_unique('intranet_groupmember', ['group_id', 'member_id'])

        # Adding model 'Project'
        db.create_table('intranet_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('lead', self.gf('django.db.models.fields.related.ForeignKey')(related_name='project_lead_set', to=orm['intranet.Member'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('intranet', ['Project'])

        # Adding M2M table for field groups on 'Project'
        db.create_table('intranet_project_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['intranet.project'], null=False)),
            ('group', models.ForeignKey(orm['intranet.group'], null=False))
        ))
        db.create_unique('intranet_project_groups', ['project_id', 'group_id'])

        # Adding M2M table for field members on 'Project'
        db.create_table('intranet_project_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['intranet.project'], null=False)),
            ('member', models.ForeignKey(orm['intranet.member'], null=False))
        ))
        db.create_unique('intranet_project_members', ['project_id', 'member_id'])

        # Adding model 'Event'
        db.create_table('intranet_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('starttime', self.gf('django.db.models.fields.DateTimeField')()),
            ('endtime', self.gf('django.db.models.fields.DateTimeField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('intranet', ['Event'])

        # Adding M2M table for field sponsors on 'Event'
        db.create_table('intranet_event_sponsors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['intranet.event'], null=False)),
            ('group', models.ForeignKey(orm['intranet.group'], null=False))
        ))
        db.create_unique('intranet_event_sponsors', ['event_id', 'group_id'])

        # Adding model 'Job'
        db.create_table('intranet_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('contact_email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type_full', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type_part', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type_intern', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='differ', max_length=10)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('intranet', ['Job'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'GroupMember', fields ['group', 'member']
        db.delete_unique('intranet_groupmember', ['group_id', 'member_id'])

        # Deleting model 'Member'
        db.delete_table('intranet_member')

        # Deleting model 'Group'
        db.delete_table('intranet_group')

        # Deleting model 'GroupMember'
        db.delete_table('intranet_groupmember')

        # Deleting model 'Project'
        db.delete_table('intranet_project')

        # Removing M2M table for field groups on 'Project'
        db.delete_table('intranet_project_groups')

        # Removing M2M table for field members on 'Project'
        db.delete_table('intranet_project_members')

        # Deleting model 'Event'
        db.delete_table('intranet_event')

        # Removing M2M table for field sponsors on 'Event'
        db.delete_table('intranet_event_sponsors')

        # Deleting model 'Job'
        db.delete_table('intranet_job')


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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 16, 22, 13, 35, 27428)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 4, 16, 22, 13, 35, 27265)'}),
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
        'intranet.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'endtime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['intranet.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'starttime': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'intranet.group': {
            'Meta': {'object_name': 'Group'},
            'date_formed': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'mailing_list': ('django.db.models.fields.EmailField', [], {'max_length': '60'}),
            'meeting_day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'meeting_location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'meeting_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['intranet.Member']", 'symmetrical': 'False', 'through': "orm['intranet.GroupMember']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'intranet.groupmember': {
            'Meta': {'unique_together': "(('group', 'member'),)", 'object_name': 'GroupMember'},
            'date_joined': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intranet.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_chair': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['intranet.Member']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '255'})
        },
        'intranet.job': {
            'Meta': {'object_name': 'Job'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contact_email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'differ'", 'max_length': '10'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type_full': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type_intern': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type_part': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'intranet.member': {
            'Meta': {'object_name': 'Member', '_ormbases': ['auth.User']},
            'left_uiuc': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '255'}),
            'uin': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'intranet.project': {
            'Meta': {'object_name': 'Project'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'project_group_set'", 'blank': 'True', 'to': "orm['intranet.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_lead_set'", 'to': "orm['intranet.Member']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'project_members_set'", 'blank': 'True', 'to': "orm['intranet.Member']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['intranet']
