from django.db import models

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


TYPE_ARM = "A"
TYPE_LEG = "L"
TYPE_HEAD = "H"
TYPE_CHEST = "C"
TYPE_ESP = "E"
TYPE_CHOICES = (
    (TYPE_ARM, "Arm"),
    (TYPE_LEG, "Leg"),
    (TYPE_HEAD, "Head"),
    (TYPE_CHEST, "Chest"),
    (TYPE_ESP, "Especial")
)

ELEM_FIRE = "F"
ELEM_AIR = "A"
ELEM_WATER = "W"
ELEM_EARTH = "E"
ELEM_CHOICES = (
    (ELEM_FIRE, "Fire"),
    (ELEM_AIR, "Air"),
    (ELEM_WATER, "Water"),
    (ELEM_EARTH, "Earth")
)

# Create your models here.
class Config(models.Model):
    xpBattleWinner = models.FloatField(u'Xp Battle Winner')
    xpBattleLoser = models.FloatField(u'Xp for Loser Battle')
    reputationBattleWinner = models.FloatField(u'Reputation Battle Winner')
    reputationBattleLoser = models.FloatField(u'Reputation Battle Loser')


class Item(models.Model):
    name = models.CharField(u'Name', max_length=250)
    type_item = models.CharField(u'Type Item', max_length=1, choices=TYPE_CHOICES)
    element = models.CharField(u'Element', max_length=1, choices=ELEM_CHOICES)
    attribute = models.CharField(u'Attribute', max_length=100)
    xpRequired = models.FloatField(u'Xp Required')
    #user = models.ForeignKey(UserGame, verbose_name="UserItem")

    def __unicode__(self):
        return self.name


class UserGame(models.Model):
    name = models.CharField(u'Name', max_length=200)
    reputation = models.FloatField(u'Reputation', default=100)
    hp = models.FloatField(u'HP', default=10)
    xp = models.FloatField(u'XP', default=0)
    chest = models.ForeignKey(Item, related_name="ChestItem", blank=True, null=True)
    leg =  models.ForeignKey(Item, related_name="LegItem", blank=True, null=True)
    arm = models.ForeignKey(Item, related_name="ArmItem", blank=True, null=True)
    head =  models.ForeignKey(Item, related_name="HeadItem", blank=True, null=True)
    especial = models.ForeignKey(Item, related_name="EspecialItem", blank=True, null=True)
    items = models.ManyToManyField(Item, blank=True, null=True)

    def __unicode__(self):
        return self.name


class UserLogin(models.Model):
    username = models.CharField(u'UserName', max_length=50)
    password = models.CharField(u'Password', max_length=100)
    email = models.EmailField(u'Email', max_length=75)
    userGame = models.ForeignKey(UserGame, related_name='UserGameChar')
    join = models.DateTimeField(auto_now=True)


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
    datetime = models.DateTimeField(auto_now=True)

    challenging_chest = models.ForeignKey(Item, related_name="ChestItem1", blank=True, null=True)
    challenging_leg =  models.ForeignKey(Item, related_name="LegItem1", blank=True, null=True)
    challenging_arm = models.ForeignKey(Item, related_name="ArmItem1", blank=True, null=True)
    challenging_head =  models.ForeignKey(Item, related_name="HeadItem1", blank=True, null=True)
    challenging_especial =  models.ForeignKey(Item, related_name="especialItem1", blank=True, null=True)


    challenged_chest = models.ForeignKey(Item, related_name="ChestItem2", blank=True, null=True)
    challenged_leg =  models.ForeignKey(Item, related_name="LegItem2", blank=True, null=True)
    challenged_arm = models.ForeignKey(Item, related_name="ArmItem2", blank=True, null=True)
    challenged_head =  models.ForeignKey(Item, related_name="HeadItem2", blank=True, null=True)
    challenged_especial =  models.ForeignKey(Item, related_name="EspecialItem2", blank=True, null=True)

    def __unicode__(self):
        return "%s vs %s" % (self.challenging, self.challenged)


class Battle(models.Model):
    winner = models.CharField(u'Winner', max_length=50, null=True, blank=True)
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

    def __unicode__(self):
        return self.message
