# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'hotels_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'hotels', ['Tag'])

        # Adding model 'Hotel'
        db.create_table(u'hotels_hotel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('stars', self.gf('django.db.models.fields.IntegerField')()),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'hotels', ['Hotel'])

        # Adding M2M table for field tags on 'Hotel'
        m2m_table_name = db.shorten_name(u'hotels_hotel_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('hotel', models.ForeignKey(orm[u'hotels.hotel'], null=False)),
            ('tag', models.ForeignKey(orm[u'hotels.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['hotel_id', 'tag_id'])

        # Adding model 'RoomType'
        db.create_table(u'hotels_roomtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'hotels', ['RoomType'])

        # Adding model 'Room'
        db.create_table(u'hotels_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hotels.RoomType'])),
            ('hotel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hotels.Hotel'])),
        ))
        db.send_create_signal(u'hotels', ['Room'])

        # Adding unique constraint on 'Room', fields ['number', 'hotel']
        db.create_unique(u'hotels_room', ['number', 'hotel_id'])

        # Adding model 'Reservation'
        db.create_table(u'hotels_reservation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hotels.Room'])),
        ))
        db.send_create_signal(u'hotels', ['Reservation'])


    def backwards(self, orm):
        # Removing unique constraint on 'Room', fields ['number', 'hotel']
        db.delete_unique(u'hotels_room', ['number', 'hotel_id'])

        # Deleting model 'Tag'
        db.delete_table(u'hotels_tag')

        # Deleting model 'Hotel'
        db.delete_table(u'hotels_hotel')

        # Removing M2M table for field tags on 'Hotel'
        db.delete_table(db.shorten_name(u'hotels_hotel_tags'))

        # Deleting model 'RoomType'
        db.delete_table(u'hotels_roomtype')

        # Deleting model 'Room'
        db.delete_table(u'hotels_room')

        # Deleting model 'Reservation'
        db.delete_table(u'hotels_reservation')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'hotels.hotel': {
            'Meta': {'object_name': 'Hotel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'stars': ('django.db.models.fields.IntegerField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['hotels.Tag']", 'symmetrical': 'False'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'hotels.reservation': {
            'Meta': {'object_name': 'Reservation'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hotels.Room']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'hotels.room': {
            'Meta': {'unique_together': "(('number', 'hotel'),)", 'object_name': 'Room'},
            'hotel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hotels.Hotel']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hotels.RoomType']"})
        },
        u'hotels.roomtype': {
            'Meta': {'object_name': 'RoomType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'hotels.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['hotels']