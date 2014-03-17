# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Config'
        db.create_table(u'core_config', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('xpBattleWinner', self.gf('django.db.models.fields.FloatField')()),
            ('xpBattleLoser', self.gf('django.db.models.fields.FloatField')()),
            ('reputationBattleWinner', self.gf('django.db.models.fields.FloatField')()),
            ('reputationBattleLoser', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'core', ['Config'])

        # Adding model 'Item'
        db.create_table(u'core_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('type_item', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('element', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('attribute', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('xpRequired', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'core', ['Item'])

        # Adding model 'UserGame'
        db.create_table(u'core_usergame', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('reputation', self.gf('django.db.models.fields.FloatField')(default=100)),
            ('hp', self.gf('django.db.models.fields.FloatField')(default=10)),
            ('xp', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('chest', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ChestItem', null=True, to=orm['core.Item'])),
            ('leg', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='LegItem', null=True, to=orm['core.Item'])),
            ('arm', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ArmItem', null=True, to=orm['core.Item'])),
            ('head', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='HeadItem', null=True, to=orm['core.Item'])),
            ('especial', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='EspecialItem', null=True, to=orm['core.Item'])),
        ))
        db.send_create_signal(u'core', ['UserGame'])

        # Adding M2M table for field items on 'UserGame'
        m2m_table_name = db.shorten_name(u'core_usergame_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usergame', models.ForeignKey(orm[u'core.usergame'], null=False)),
            ('item', models.ForeignKey(orm[u'core.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['usergame_id', 'item_id'])

        # Adding model 'UserLogin'
        db.create_table(u'core_userlogin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('userGame', self.gf('django.db.models.fields.related.ForeignKey')(related_name='UserGameChar', to=orm['core.UserGame'])),
            ('join', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['UserLogin'])

        # Adding model 'Friend'
        db.create_table(u'core_friend', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='UserBase', to=orm['core.UserGame'])),
            ('friend', self.gf('django.db.models.fields.related.ForeignKey')(related_name='UserFriend', to=orm['core.UserGame'])),
        ))
        db.send_create_signal(u'core', ['Friend'])

        # Adding model 'RequisitionBattle'
        db.create_table(u'core_requisitionbattle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('challenging', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'Challenging', to=orm['core.UserGame'])),
            ('challenged', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'Challenged', to=orm['core.UserGame'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('challenging_chest', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ChestItem1', null=True, to=orm['core.Item'])),
            ('challenging_leg', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='LegItem1', null=True, to=orm['core.Item'])),
            ('challenging_arm', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ArmItem1', null=True, to=orm['core.Item'])),
            ('challenging_head', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='HeadItem1', null=True, to=orm['core.Item'])),
            ('challenging_especial', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='especialItem1', null=True, to=orm['core.Item'])),
            ('challenged_chest', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ChestItem2', null=True, to=orm['core.Item'])),
            ('challenged_leg', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='LegItem2', null=True, to=orm['core.Item'])),
            ('challenged_arm', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ArmItem2', null=True, to=orm['core.Item'])),
            ('challenged_head', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='HeadItem2', null=True, to=orm['core.Item'])),
            ('challenged_especial', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='EspecialItem2', null=True, to=orm['core.Item'])),
        ))
        db.send_create_signal(u'core', ['RequisitionBattle'])

        # Adding model 'Battle'
        db.create_table(u'core_battle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('winner', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('numberOfRounds', self.gf('django.db.models.fields.FloatField')()),
            ('requisitionBattle', self.gf('django.db.models.fields.related.ForeignKey')(related_name='RequisitionBattle', to=orm['core.RequisitionBattle'])),
        ))
        db.send_create_signal(u'core', ['Battle'])

        # Adding model 'LogBattle'
        db.create_table(u'core_logbattle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.FloatField')()),
            ('player', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('typeAttack', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('hit', self.gf('django.db.models.fields.BooleanField')()),
            ('damage', self.gf('django.db.models.fields.FloatField')()),
            ('battle', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Battle', to=orm['core.Battle'])),
            ('playerLife', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'core', ['LogBattle'])

        # Adding model 'Notification'
        db.create_table(u'core_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'UserGame', to=orm['core.UserGame'])),
        ))
        db.send_create_signal(u'core', ['Notification'])


    def backwards(self, orm):
        # Deleting model 'Config'
        db.delete_table(u'core_config')

        # Deleting model 'Item'
        db.delete_table(u'core_item')

        # Deleting model 'UserGame'
        db.delete_table(u'core_usergame')

        # Removing M2M table for field items on 'UserGame'
        db.delete_table(db.shorten_name(u'core_usergame_items'))

        # Deleting model 'UserLogin'
        db.delete_table(u'core_userlogin')

        # Deleting model 'Friend'
        db.delete_table(u'core_friend')

        # Deleting model 'RequisitionBattle'
        db.delete_table(u'core_requisitionbattle')

        # Deleting model 'Battle'
        db.delete_table(u'core_battle')

        # Deleting model 'LogBattle'
        db.delete_table(u'core_logbattle')

        # Deleting model 'Notification'
        db.delete_table(u'core_notification')


    models = {
        u'core.battle': {
            'Meta': {'object_name': 'Battle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numberOfRounds': ('django.db.models.fields.FloatField', [], {}),
            'requisitionBattle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'RequisitionBattle'", 'to': u"orm['core.RequisitionBattle']"}),
            'winner': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'core.config': {
            'Meta': {'object_name': 'Config'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reputationBattleLoser': ('django.db.models.fields.FloatField', [], {}),
            'reputationBattleWinner': ('django.db.models.fields.FloatField', [], {}),
            'xpBattleLoser': ('django.db.models.fields.FloatField', [], {}),
            'xpBattleWinner': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.friend': {
            'Meta': {'object_name': 'Friend'},
            'friend': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'UserFriend'", 'to': u"orm['core.UserGame']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'UserBase'", 'to': u"orm['core.UserGame']"})
        },
        u'core.item': {
            'Meta': {'object_name': 'Item'},
            'attribute': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'element': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'type_item': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'xpRequired': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'core.logbattle': {
            'Meta': {'object_name': 'LogBattle'},
            'battle': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Battle'", 'to': u"orm['core.Battle']"}),
            'damage': ('django.db.models.fields.FloatField', [], {}),
            'hit': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.FloatField', [], {}),
            'player': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'playerLife': ('django.db.models.fields.FloatField', [], {}),
            'typeAttack': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'core.notification': {
            'Meta': {'object_name': 'Notification'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'UserGame'", 'to': u"orm['core.UserGame']"})
        },
        u'core.requisitionbattle': {
            'Meta': {'object_name': 'RequisitionBattle'},
            'challenged': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'Challenged'", 'to': u"orm['core.UserGame']"}),
            'challenged_arm': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ArmItem2'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'challenged_chest': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ChestItem2'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'challenged_especial': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'EspecialItem2'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'challenged_head': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'HeadItem2'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'challenged_leg': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'LegItem2'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'challenging': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'Challenging'", 'to': u"orm['core.UserGame']"}),
            'challenging_arm': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ArmItem1'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'challenging_chest': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ChestItem1'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'challenging_especial': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'especialItem1'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'challenging_head': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'HeadItem1'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'challenging_leg': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'LegItem1'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'core.usergame': {
            'Meta': {'object_name': 'UserGame'},
            'arm': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ArmItem'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'chest': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ChestItem'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'especial': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'EspecialItem'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'head': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'HeadItem'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'hp': ('django.db.models.fields.FloatField', [], {'default': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Item']", 'null': 'True', 'blank': 'True'}),
            'leg': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'LegItem'", 'null': 'True', 'to': u"orm['core.Item']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'reputation': ('django.db.models.fields.FloatField', [], {'default': '100'}),
            'xp': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'core.userlogin': {
            'Meta': {'object_name': 'UserLogin'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'userGame': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'UserGameChar'", 'to': u"orm['core.UserGame']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['core']