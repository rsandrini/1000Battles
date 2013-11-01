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


ATTACK_KICK = "K"
ATTACK_PUNCH = "P"
ATTACK_HALTER = "H"
ATTACK_CHOICES = (
    (ATTACK_KICK, "Kick"),
    (ATTACK_PUNCH, "Punch"),
    (ATTACK_HALTER, "Halter")
)


# Create your models here.
class Config(models.Model):
    xpBattleWinner = models.FloatField(u'Xp Battle Winner')
    xpBattleLoser = models.FloatField(u'Xp for Loser Battle')
    reputationBattleWinner = models.FloatField(u'Reputation Battle Winner')
    reputationBattleLoser = models.FloatField(u'Reputation Battle Loser')

    def __unicode__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(u'Name', max_length=250)
    type_item = models.CharField(u'Type Item', max_length=100)
    element = models.CharField(u'Element', max_length=1, choices=ELEMENT_CHOICES)
    attribute = models.CharField(u'Attribute', max_length=100)
    xpRequired = models.FloatField(u'Xp Required')
    #user = models.ForeignKey(UserGame, verbose_name="UserItem")

    def __unicode__(self):
        return self.name


class UserGame(models.Model):
    name = models.CharField(u'Name', max_length=200)
    reputation = models.FloatField(u'Reputation')
    hp = models.FloatField(u'HP')
    xp = models.FloatField(u'Xp')
    chest = models.ForeignKey(Item, related_name="ChestItem", blank=True, null=True)
    leg =  models.ForeignKey(Item, related_name="LegItem", blank=True, null=True)
    arm = models.ForeignKey(Item, related_name="ArmItem", blank=True, null=True)
    head =  models.ForeignKey(Item, related_name="HeadItem", blank=True, null=True)
    items = models.ManyToManyField(Item, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Friend(models.Model):
    user = models.ForeignKey(UserGame, related_name="UserBase")
    friend = models.ForeignKey(UserGame, related_name="UserFriend")

    def __unicode__(self):
        #return "'%s' amigo de '%s' " % (self.user.name, self.friend.name)
        return self.friend.name


class RequisitionBattle(models.Model):
    challenging = models.ForeignKey(UserGame, related_name=u"Challenging")
    challenged = models.ForeignKey(UserGame, related_name=u"Challenged")
    status = models.CharField(u'Status', max_length=1, choices=STATUS_CHOICES)

    def __unicode__(self):
        return "%s vs %s" % (self.challenging, self.challenged)


class Battle(models.Model):
    winner = models.CharField(u'Winner', max_length=50)
    numberOfRounds = models.FloatField(u'Rounds')
    requisitionBattle = models.ForeignKey(RequisitionBattle, related_name="RequisitionBattle")

    def __unicode__(self):
        return self.winner


class LogBattle(models.Model):
    order = models.FloatField(u'Order')
    player = models.CharField(u'Player', max_length=50)
    typeAttack = models.CharField(u'Type Attack', max_length=1, choices=ATTACK_CHOICES)
    hit = models.BooleanField(u'Hit')
    damage = models.FloatField(u'Damage')
    battle = models.ForeignKey(Battle, related_name="Battle")


    def __unicode__(self):
        return self.player


class Notification(models.Model):
    message = models.CharField(u'Message', max_length=500)
    datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserGame, related_name=u'UserGame')
