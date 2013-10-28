from django.db import models

ELEMENT_WOOD = 'W'
ELEMENT_IRON = 'I'
ELEMENT_CHOICES = (
    (ELEMENT_WOOD, 'Wood'),
    (ELEMENT_IRON, 'Iron')
)


STATUS_WAITING = 'W'
STATUS_FINISHED = 'F'
STATUS_CANCELED = 'C'
STATUS_CHOICES = (
    (STATUS_WAITING, "Waiting"),
    (STATUS_FINISHED, "Finished"),
    (STATUS_CANCELED, "Canceled")
)

# Create your models here.
class Config(models.Model):
    xpBattleWinner = models.FloatField(u'Xp Battle Winner')
    xpBattleLoser = models.FloatField(u'Xp for Loser Battle')
    reputationBattleWinner = models.FloatField(u'Reputation Battle Winner')
    reputationBattleLoser = models.FloatField(u'Reputation Battle Loser')


class Item(models.Model):
    name = models.CharField(u'Name', max_length=250)
    type_item = models.CharField(u'Type Item', max_length=100)
    element = models.CharField(u'Element', max_length=1, choices=ELEMENT_CHOICES)
    attribute = models.CharField(u'Attribute', max_length=100)
    xpRequired = models.FloatField(u'Xp Attribute')


class UserGame(models.Model):
    name = models.CharField(u'Name', max_length=200)
    reputation = models.FloatField(u'Reputation')
    hp = models.FloatField(u'HP')
    xp = models.FloatField(u'Xp')


class Friend(models.Model):
    user = models.ForeignKey(UserGame, verbose_name="User"),
    friend = models.ForeignKey(UserGame, verbose_name="Friend")


class RequisitionBattle(models.Model):
    challenging = models.ForeignKey(UserGame, related_name=u"Challenging")
    challenged = models.ForeignKey(UserGame, related_name=u"Challenged")
    status = models.CharField(u'Status', max_length=1, choices=STATUS_CHOICES)


class Battle(models.Model):
    winner = models.ForeignKey(UserGame, verbose_name="Winner")
    numberOfRounds = models.FloatField(u'Rounds')


class LogBattle(models.Model):
    order = models.FloatField(u'Order')
    player = models.ForeignKey(UserGame, verbose_name="Player")
    typeAttack = models.CharField(u'Type Attack', max_length=50)
    hit = models.BooleanField(u'Hit')
    damage = models.FloatField(u'Damage')
