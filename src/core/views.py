# -*- coding: utf-8 -*-

from django.views.generic import View
from core.models import *
import json
from django.http import HttpResponse
import sys
from core.utils import *
from django.db.models import Q
import random
from django.core.exceptions import ObjectDoesNotExist


class IndexView(View):
    def get(self, *args, **kwargs):

        return HttpResponse(json.dumps("TESTE"), mimetype="application/json")


'''
    curl -X POST -H "Content-Type: application/json" -d '{"username":"", "password":""}' http://localhost:8000/login
'''
class LoginView(View):
    def get(self, *args, **kwargs):
        return HttpResponse(json.dumps("OK"), mimetype="application/json")

    def post(self, *args, **kwargs):
        try:
            error = []
            data = json.loads(self.request.body)
            if UserLogin.objects.filter(username=data['username'], password=data['password']).count() == 1:
                ul = UserLogin.objects.get(username=data['username'], password=data['password'])
                return HttpResponse(json.dumps('logged'), mimetype='aplication/json')
            else:
                error.append("Login ou senha incorretos")
                return HttpResponse(json.dumps(error), mimetype='aplication/json')

        except:
            pass

'''
    curl -X POST -H "Content-Type: application/json" -d '{"username":"", "password":"", "email":"", "name":""}' http://localhost:8000/registration/
'''
class RegisterView(View):
    def post(self, *args, **kwargs):
        try:
            error = []
            data=json.loads(self.request.body)
            if (data['username'] == "" or data['email'] == ""
                and data['password'] == "" and data['name'] == ""):
                error.append("Dados incompletos")
            elif UserLogin.objects.filter(Q(username=data['username']) | Q(email=data['email'])).count() == 0:
                ug = UserGame(name=data['name'])
                ug.save()

                ul = UserLogin(username=data['username'],
                    password=data['password'], email=data['email'], userGame=ug)
                ul.save()
            else:
                error.append("Usuario ou email ja registrados")
        except:
            pass
        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(json.dumps("registred"), mimetype="aplication/json")


'''
    curl -X GET -H "Content-Type: application/json" http://localhost:8000/dashboard/1/
'''
class DashboardView(View):
    def get(self, *args, **kwargs):
        idUser = self.kwargs['id']
        error = []
        try:
            user = UserGame.objects.get(pk=idUser)
            #itens = Item.objects.filter(user=user)
            friends = Friend.objects.filter(user=user)
            _user = json_repr(user)
            _friends = json.dumps([dict(friend=json_repr(pn.friend.name)) for pn in friends])
            data = json.dumps({"user":_user, "friends":_friends })

        except:
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")

'''
    curl -X GET -H "Content-Type: application/json" http://localhost:8000/battles/1/
'''
class BattleView(View):
    def get(self, *args, **kwargs):
        idUser = self.kwargs['id']
        error = []
        try:
            user = UserGame.objects.get(pk=idUser)
            reBattles = RequisitionBattle.objects.filter(Q(challenging=user) | Q(challenged=user), status="F")
            _battles = []
            for i in reBattles:
                _battles.append(dict(battle=json_repr(Battle.objects.get(requisitionBattle=i))))

            data = json.dumps({"battles":_battles })
        except:
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")


'''
  curl -X GET -H "Content-Type: application/json" http://localhost:8000/battles_requisition/1/
'''
class ShowBattlesRequisitionView(View):
    def get(self, *args, **kwargs):
        idUser = self.kwargs['id']
        error = []
        try:
            user = UserGame.objects.get(pk=idUser)
            reBattles = RequisitionBattle.objects.filter(Q(challenging=user) | Q(challenged=user), status="W")
            _battles = []
            for i in reBattles:
                _battles.append(dict(battle=json_repr(i)))

            data = json.dumps({"battles_requisition":_battles })
        except:
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")

'''
    curl -X POST -H "Content-Type: application/json" -d '{"challenging":1, "challenged":2}' http://localhost:8000/battle_challenge/
    curl -X POST -H "Content-Type: application/json" -d '{"challenging":1, "challenged":0}' http://localhost:8000/battle_challenge/

'''
class BattleRequisitionView(View):
    def post(self, *args, **kwargs):
        error = []
        try:
            data=json.loads(self.request.body)
            print data
            challenging = UserGame.objects.get(pk=data['challenging'])
            if data['challenged'] != 0:
                challenged = UserGame.objects.get(pk=data['challenged'])
            else:
                challenged = 0

            challenging_chest, challenging_leg, challenging_head, challenging_arm = None, None, None, None

            try:
                if challenging.challenging_chest > 0:
                    challenging_chest = challenging.challenging_chest
                else:
                    challeging_chest = UserGame.objects.get(pk=1)

            except:
                challeging_chest = UserGame.objects.get(pk=1)

            try:
                if challenging.challenging_head > 0:
                    challenging_head = challenging.challenging_head
                else:
                    challeging_head = UserGame.objects.get(pk=1)

            except:
                challeging_head = UserGame.objects.get(pk=1)

            try:
                if challenging.challenging_arm > 0:
                    challenging_arm = challenging.challenging_arm
                else:
                    challeging_arm = UserGame.objects.get(pk=1)

            except:
                challeging_arm = UserGame.objects.get(pk=1)


            try:
                if challenging.challenging_leg > 0:
                    challenging_leg = challenging.challenging_leg
                else:
                    challeging_leg = UserGame.objects.get(pk=1)

            except:
                challeging_leg = UserGame.objects.get(pk=1)

            ok = False
            cont =0
            while not ok:
                cont += 1
                if challenged == 0:
                    #Filter other players for reputation - See method
                    challenged = randomOpponent(challenging)
                    if RequisitionBattle.objects.filter(challenged=challenged, challenging=challenging, status="W").count() == 0:
                        ok = True
                    else:
                        challenged = 0
                        # FAIL
                        if cont > 5:
                            ok = True


            if not challenged == 0:
                rb = RequisitionBattle(challenging=challenging, challenged=challenged,
                                        challenging_chest=challenging_chest,
                                        challenging_leg=challenging_leg,
                                        challenging_arm=challenging_arm,
                                        challenging_head=challenging_head,
                                        status="W")
                rb.save()
                msg = "Você foi desafiado para um combate!"
                create_notification(msg, challenged)
            else:
                error.append("Nao foi possivel encontrar um oponente - fudeu")

        except:
            raise
            error.append("Ocorreu um erro -  tente novamente")
            pass

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(json.dumps("OK") ,mimetype="aplication/json")
'''
    Accept or decline battle requisition

    curl -X POST -H "Content-Type: application/json" -d '{"accept":"True"}' http://localhost:8000/battle_requisition_confirm/3/
'''
class BattleRequisitionConfirmView(View):


    def get(self, *args, **kwargs):
        error = []
        try:
            reBattle = RequisitionBattle.objects.get(pk=self.kwargs['id_requisition'], status="W")
            data = json.dumps({"requisition": json_repr(reBattle) })
        except RequisitionBattle.DoesNotExist:
            error.append("Nao foi possivel recuperar esta requisicao pois a batalha ja foi aceita")
        except:
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")

    def post(self, *args, **kwargs):
        error = []
        try:
            data=json.loads(self.request.body)
            req = RequisitionBattle.objects.get(pk=self.kwargs['id_requisition'])
            if req.status == "W":
                if data['accept'] == 'true' or data['accept'] == 'True':
                    challenged = UserGame.objects.get(pk=req.challenged.pk)
                    try:
                        if challenged.chest:
                            challenged_chest = challengend.chest
                    except:
                        challenged_chest = Item.objects.get(pk=1)

                    try:
                        if challenged.leg:
                            challenged_leg = challenged.leg
                    except:
                        challenged_leg = Item.objects.get(pk=1)

                    try:
                        if challenged.arm:
                            challenged_arm = challenged.arm
                    except:
                        challenged_arm = Item.objects.get(pk=1)

                    try:
                        if challenged.head:
                            challenged_head = challenged.head
                    except:
                        challenged_chest = UserGame.objects.get(pk=1)

                    req.challenged_chest = challenged_chest
                    req.challenged_leg = challenged_leg
                    req.challenged_arm = challenged_arm
                    req.challenged_head = challenged_head
                    req.save()

                    print 'ACCEPT MOTHERFUCK!'
                    self.process_battle(req)

                else:
                    req.status = "C"
                    req.save()
                    msg = "O jogador %s nao aceitou sua solicitacao de batalha", req.challenged
                    create_notification(msg, req.challenging)
                data = "OK"
        except:
            error.append("Ocorreu um problema")
            pass

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")


'''
    curl -X GET -H "Content-Type: application/json"  http://localhost:8000/battle/1/
'''
class ShowBattleView(View):
    def get(self, *args, **kwargs):
        error = []
        try:
            _battle = Battle.objects.get(pk=self.kwargs['id_battle'])
            _req = RequisitionBattle.objects.get(pk=_battle.requisitionBattle.pk)

            logs = LogBattle.objects.filter(battle=_battle).order_by('order')
            _itens = []
            for i in logs:
                _itens.append(dict(log=json_repr(i)))

            data = json.dumps({"battle":json_repr(_battle), "details":json_repr(_req), "log":_itens })

        except:
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")


'''
    curl -X GET -H "Content-Type: application/json"  http://localhost:8000/all_itens/
'''
class ShowAllItensView(View):
    def get(self, *args, **kwargs):
        error = []
        try:
            itens = Item.objects.all()
            _itens = []
            for i in itens:
                _itens.append(dict(item=json_repr(i)))

            data = json.dumps({"itens":_itens })

        except:
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")


'''
    curl -X GET -H "Content-Type: application/json"  http://localhost:8000/my_itens/1/
'''
class ShowMyItensView(View):
    def get(self, *args, **kwargs):
        error = []
        try:
            idUser = self.kwargs['id']
            _user = UserGame.objects.get(pk=idUser)
            _itens = []
            for i in _user.items.all():
                _itens.append(dict(item=json_repr(i)))

            data = json.dumps({"my_itens":_itens })

        except:
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")


'''
    curl -X GET -H "Content-Type: application/json"  http://localhost:8000/ranking/
'''
class ShowRankingView(View):
    def get(self, *args, **kwargs):
        error = []
        try:
            users = UserGame.objects.all().order_by('-reputation')
            _itens = []
            for index, i in enumerate(users):
                _itens.append({"player":i.name, "reputation":i.reputation, "position":index+1 })

            data = json.dumps({"ranking":_itens })

        except:
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")


class MessageView(View):

    '''
        curl -X GET -H "Content-Type: application/json"  http://localhost:8000/message/1/
    '''
    def get(self, *args, **kwargs):
        error = []
        try:
            _msg = Notification.objects.get(pk=self.kwargs['id_msg'])
        except:
            error.append("Erro ao processar solicitacao")
            pass

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
           return HttpResponse(json_repr(_msg) ,mimetype="aplication/json")


    '''
        curl -X POST -H "Content-Type: application/json" -d '{"action":"remove"}' http://localhost:8000/message/1/
    '''
    def post(self, *args, **kwargs):
        error = []
        try:
            data=json.loads(self.request.body)
            _msg = Notification.objects.get(pk=self.kwargs['id_msg'])
            action = data['action']
            if action == "remove" or action == "Remove":
                _msg.delete()
            else:
                pass
            data = json.dumps({"response":"OK" })

        except:
            error.append("Erro ao processar solicitacao")
            pass

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
           return HttpResponse(data ,mimetype="aplication/json")


'''
    curl -X GET -H "Content-Type: application/json"  http://localhost:8000/friends/1/
'''
class FriendsView(View):
    def get(self, *args, **kwargs):
        idUser = self.kwargs['id']
        error = []
        try:
            user = UserGame.objects.get(pk=idUser)
            #itens = Item.objects.filter(user=user)
            friends = Friend.objects.filter(user=user)
            _friends = json.dumps([dict(friend=json_repr(pn.friend.name)) for pn in friends])
            data = json.dumps({"friends":_friends })
        except:
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")

    '''
        curl -X POST -H "Content-Type: application/json" -d '{"friend":3, "action:"True""}' http://localhost:8000/friends/1/

        { "friend":"ID", "action":"True" } / { "friend":"ID", "action":"False" }
    '''
    def post(self, *args, **kwargs):
        error = []
        try:
            data=json.loads(self.request.body)
            _friend = UserGame.objects.get(pk=data['friend'])
            _user = UserGame.objects.get(pk=self.kwargs['id'])
            add = data['action']
            if add == "True" or add == "true":
                if Friend.objects.filter(user=_user, friend=_friend).count() == 1:
                    friend = Friend(user=_user, friend=_friend)
                    friend.save()
                else:
                    error.append("Amigo ja existe")
            else:
                if Friend.objects.filter(user=_user, friend=_friend).count() == 1:
                    friend_get = Friend.objects.get(friend=_friend.pk, user=_user.pk)
                    friend_get.delete()
                else:
                    error.append("Amigo nao existe")

            data = json.dumps({"response":"OK" })

        except:
            error.append("Erro ao processar solicitacao")
            pass

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")


'''
    curl -X GET -H "Content-Type: application/json"  http://localhost:8000/player/2/
'''
class ShowEnemyView(View):
    def get(self, *args, **kwargs):
        idUser = self.kwargs['id']
        error = []
        try:
            user = UserGame.objects.get(pk=idUser)
            #itens = Item.objects.filter(user=user)
            _user = json_repr(user)
            data = json.dumps({"user":_user })

        except:
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")


class SetItemView(View):

    '''
        curl -X POST -H "Content-Type: application/json" -d '{"item":1, "action:"True""}' http://localhost:8000/setitem/1/
    '''
    def post(self, *args, **kwargs):
        error = []
        try:
            data=json.loads(self.request.body)
            _item = Item.objects.get(pk=data['item'])
            _user = UserGame.objects.get(pk=self.kwargs['id'])
            add = data['action']
            if add == "True" or add == "true":
                try:
                    u= UserGame.objects.get(pk=_user.pk, items=_item.pk)
                    _user_item = u.items.get(pk=_item.pk)
                    if _user_item.type_item == "A":
                        u.arm = _user_item
                        u.save()
                    elif  _user_item.type_item == "L":
                        u.leg = _user_item
                        u.save()
                    elif _user_item.type_item == "H":
                        u.head = _user_item
                        u.save()
                    elif _user_item.type_item == "C":
                        u.chest = _user_item
                        u.save()
                    elif _user_item.type_item == "E":
                        u.especial = _user_item
                        u.save()
                    else:
                        error.append("Tipo do item incorreto")

                #except DoesNotExit:
                #    error.append("Item nao existe para este usuario")
                except:
                    pass
            else:
                try:
                    u= UserGame.objects.get(pk=_user.pk, items=_item.pk)
                    _user_item = u.items.get(pk=_item.pk)
                    if _user_item.type_item == "A":
                        u.arm = None
                        u.save()
                    elif  _user_item.type_item == "L":
                        u.leg = None
                        u.save()
                    elif _user_item.type_item == "H":
                        u.head = None
                        u.save()
                    elif _user_item.type_item == "C":
                        u.chest = None
                        u.save()
                    elif _user_item.type_item == "E":
                        u.especial = None
                        u.save()
                    else:
                        error.append("Tipo do item incorreto")

                #except DoesNotExit:
                #    error.append("Item nao existe para este usuario")
                except:
                    pass
            data = json.dumps({"response":"OK" })

        except:
            error.append("Erro ao processar solicitacao")
            pass

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
           return HttpResponse(data ,mimetype="aplication/json")


def verifyEffect(_elem_attacker, _elem_defense):
    # ELEMENTS - W >  F > A > E >
    if _elem_attacker == "W":
        if _elem_defense == "F":
            return 2
        elif _elem_defense == "A":
            return 1
        elif _elem_defense == "E":
            return 0
        else:
            return 1

    if _elem_attacker == "F":
        if _elem_defense == "A":
            return 2
        elif _elem_defense == "E":
            return 1
        elif _elem_defense == "W":
            return 0
        else:
            return 1

    if _elem_attacker == "A":
        if _elem_defense == "E":
            return 2
        elif _elem_defense == "W":
            return 1
        elif _elem_defense == "F":
            return 0
        else:
            return 1

    if _elem_attacker == "E":
        if _elem_defense == "W":
            return 2
        elif _elem_defense == "F":
            return 1
        elif _elem_defense == "A":
            return 0
        else:
            return 1


def setPercentForAttack(effect, perc, type_att):
    # HALTER, PUNCH, KICK
    if type_att == "H":
        if effect == 2:
            perc["halter"] += 20
            perc["punch"] -= 10
            perc["kick"] -= 10
        elif effect == 1:
            perc["halter"] += 10
            perc["punch"] -= 5
            perc["kick"] -= 5
        else:
            perc["halter"] -= 10
            perc["punch"] += 5
            perc["kick"] += 5
    elif type_att == "P":
        if effect == 2:
            perc["halter"] -= 10
            perc["punch"] += 20
            perc["kick"] -= 10
        elif effect == 1:
            perc["halter"] -= 5
            perc["punch"] += 10
            perc["kick"] -= 5
        else:
            perc["halter"] += 5
            perc["punch"] -= 10
            perc["kick"] += 5
    elif type_att == "K":
        if effect == 2:
            perc["halter"] -= 10
            perc["punch"] -= 10
            perc["kick"] += 20
        elif effect == 1:
            perc["halter"] -= 5
            perc["punch"] -= 5
            perc["kick"] += 10
        else:
            perc["halter"] += 5
            perc["punch"] += 5
            perc["kick"] -= 10

    #VALID
    valid = False
    while not valid:
        print "Fix Table percents"
        if perc["halter"] <=0:
            perc["halter"] += 2
            perc["punch"] -= 1
            perc["kick"] -= 1

        if perc["punch"] <=0:
            perc["halter"] -= 1
            perc["punch"] += 2
            perc["kick"] -= 1

        if perc["kick"] <=0:
            perc["halter"] -= 1
            perc["punch"] -= 1
            perc["kick"] += 2

        if perc["halter"] > 0 and perc["punch"] > 0 and perc["kick"] > 0:
            if perc["halter"] + perc["punch"] + perc["kick"] == 99:
                valid = True

    return perc


def create_notification(_message, _to):
    user = UserGame.objects.get(pk=_to.pk)
    msg = Notification(message=_message, user=user)
    msg.save()


def randomOpponent(req):
    select = 0
    _range = 50
    _notInfiniteLoop = 0
    while _notInfiniteLoop < 20:
        _notInfiniteLoop += 1
        ugs = UserGame.objects.filter(reputation__range=[req.reputation-_range, req.reputation+_range]).exclude(pk=req.pk)
        if ugs.count() <= 0 :
            _range += 25
        else:
            select = ugs[random.randint(0,ugs.count()-1)]
            break

    return select


def process_battle(self, req):
    print req
    if not req.status == 'W':
        return ""
    else:
        req.status = "F"
        req.save()
    '''
        Randomiza quem comeca
        A cada ataque verifica se foi efetivo, super efetivo ou nulo.
        Aumenta ou reduz a porcetagem de uso
        - Mesma coisa o inimigo
        Se hp <=0 fim da batalha
    '''

    # Create a battle
    _battle = Battle(numberOfRounds=0, requisitionBattle=req, winner="")
    _battle.save()

    _round =0
    _cont = True
    _attacker = None
    _defender = None
    _challenging_attackers, _challenged_attackes = [], []
    _perc = { "halter":33, "punch":33, "kick":33 }, { "halter":33, "punch":33, "kick":33 }
    _winner = ""
    _elem_attacker = ""
    _elem_defense = ""

    if random.choice('ab') == 'a':
        _attacker = req.challenging
        _defender = req.challenged
        _current = 1
    else:
        _attacker = req.challenged
        _defender = req.challenging
        _current = 2

    while (_cont):
        #choice type attack
        tr = random.randint(0, 99)
        if tr in range(0, halter):
            _type_attack = "H"
            if _current == 1:
                _elem_attacker = req.challeging_head.element
                _elem_defense = req.challeged_chest.element
                _att = random.randint(0, 6+req.challeging_head.attribute)
                _damage = random.randint(1,6+req.challeging_head.attribute)
            else:
                _elem_attacker = req.challeged_head.element
                _elem_defense = req.challeging_chest.element
                _att = random.randint(0, 6+req.challenged_head.attribute)
                _damage = random.randint(1,6+req.challenged_head.attribute)

        elif tr in range(halter+1, halter+punch):
            _type_Attack = "P"
            if _current == 1:
                _elem_attacker = req.challeging_head.element
                _elem_defense = req.challeged_chest.element
                _att = random.randint(0, 6+req.challeging_arm.attribute)
                _damage = random.randint(1,6+req.challeging_arm.attribute)
            else:
                _elem_attacker = req.challeged_head.element
                _elem_defense = req.challeging_chest.element
                _att = random.randint(0, 6+req.challenged_arm.attribute)
                _damage = random.randint(1,6+req.challenged_arm.attribute)

        elif tr in range(halter+punch+1, halter+punch+kick):
            _type_attack = "K"
            if _current == 1:
                _elem_attacker = req.challeging_head.element
                _elem_defense = req.challeged_chest.element
                _att = random.randint(0, 6+req.challeging_leg.attribute)
                _damage = random.randint(1,6+req.challeging_leg.attribute)
            else:
                _elem_attacker = req.challeged_head.element
                _elem_defense = req.challeging_chest.element
                _att = random.randint(0, 6+req.challenged_leg.attribute)
                _damage = random.randint(1,6+req.challenged_leg.attribute)

        _round += 1
        if _current == 1:
            _def = random.randint(0, 6+req.challenging_chest.attribute)
        else:
            _def = random.randint(0, 6+req.challenged_chest.attribute)
        _hit = False

        _effect = verifyEffect(_elem_attacker, _elem_defense)
        if _effect == 1:
            #Effective
            if _att > _def:
                _defender.hp -= _damage
                _hit = True
        elif _effect == 2:
            #SuperEffective
            if _att*2 > _def:
                _defender.hp -= _damage*2
        else:
            #Not Effect
            if _att > _def*2:
                _defender.hp -= _damage/2

        if _hit:
            if _current == 1:
                _perc[0] = setPercentForAttack(_effect, _perc[0], _type_attack)
            else:
                _perc[1] = setPercentForAttack(_effect, _perc[1], _type_attack)


        log_battle = LogBattle(order=_round, player=_attacker,
                                typeAttack=_type_attack, hit=_hit,
                                damage=_damage, battle=_battle)
        log_battle.save()

        if _defender.hp <= 0:
            config = Config.objects.get(pk=1)
            _cont = False
            _winner = _attacker.name

            winner = UserGame.objects.get(pk=_attacker.pk)
            winner.reputation += config.reputationBattleWinner
            winner.xp += config.xpBattleWinner
            winner.save()

            loser = UserGame.objects.get(pk=_defender.pk)
            loser.reputation -= config.reputationBattleLoser
            loser.xp += config.xpBattleLoser
            loser.save()

        else:
            _attacker, _defender = _defender, _attacker # :D
            if _current == 1:
                _current = 2
            else:
                _current = 1

    _battle.winner = _winner
    _battle.numberOfRounds = _round
    _battle.save()

    print "End battle"
    msg = "Uma batalha aconteceu, veja o resultado!"
    create_notification(msg, req.challenging)
    create_notification(msg, req.challenged)

