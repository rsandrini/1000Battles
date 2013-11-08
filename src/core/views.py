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
            raise


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
            raise
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
            raise
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
            raise
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
            raise
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")

'''
    curl -X POST -H "Content-Type: application/json" -d '{"challenging":1, "challenged":2}' http://localhost:8000/battle_challenge/
'''
class BattleRequisitionView(View):
    def post(self, *args, **kwargs):
        try:
            data=json.loads(self.request.body)
            print data
            challenging = UserGame.objects.get(pk=data['challenging'])
            challenged = UserGame.objects.get(pk=data['challenged'])

            challenging_chest, challenging_leg, challenging_head, challenging_arm = None, None, None, None

            try:
                if data['challenging_chest']:
                    challenging_chest = UserGame.objects.get(
                                            pk=data['challenging_chest'])
            except KeyError:
                pass

            try:
                if data['challenging_leg']:
                    challenging_leg = UserGame.objects.get(
                                        pk=data['challenging_leg'])
            except KeyError:
                pass

            try:
                if data['challenging_arm']:
                    challenging_arm = UserGame.objects.get(
                                        pk=data['challenging_arm'])
            except KeyError:
                pass

            try:
                if data['challenging_head']:
                    challenging_head = UserGame.objects.get(
                                        pk=data['challenging_head'])
            except KeyError:
                pass

            rb = RequisitionBattle(challenging=challenging, challenged=challenged,
                                    challenging_chest=challenging_chest,
                                    challenging_leg=challenging_leg,
                                    challenging_arm=challenging_arm,
                                    challenging_head=challenging_head,
                                    status="W")
            rb.save()
            msg = "Você foi desafiado para um combate!"
            create_notification(msg, challenged)

        except:
            raise
        return HttpResponse('Challenged')

'''
    Accept or decline battle requisition

    curl -X POST -H "Content-Type: application/json" -d '{"accept":"True"}' http://localhost:8000/battle_requisition_confirm/3/
'''
class BattleRequisitionConfirmView(View):

    def process_battle(self, req):
        print req
        if not req.status == 'W':
            return ""
        else:
            req.status = "F"
            req.save()
        '''
            Randomiza quem comeca
            Cria uma lista da ordem dos 3 ataques que fará no inicio (TODO)
            Comeca atacando com primeiro da lista e guarda o resultado (TODO)
            - Mesma coisa o inimigo
            Ao final dos três ataques usa o mais efetivo (TODO)
            Se hp <=0 fim da batalha
        '''

        # Create a battle
        _battle = Battle(numberOfRounds=0, requisitionBattle=req, winner="")
        _battle.save()

        _round =0
        _cont = True
        _attacker = None
        _defender = None
        _challenging_attackers = []
        _challenged_attackes = []
        _winner = ""


        if random.choice('ab') == 'a':
            _attacker = req.challenging
            _defender = req.challenged
        else:
            _attacker = req.challenged
            _defender = req.challenging

        while (_cont):
            _round += 1
            _att = random.randint(0, 6)
            _def = random.randint(0, 6)
            _hit = False
            _damage = 0

            if _att > _def:
                _damage = random.randint(0,6)
                _defender.hp -= _damage
                _hit = True

            log_battle = LogBattle(order=_round, player=_attacker,
                                    typeAttack="K", hit=_hit,
                                    damage=_damage, battle=_battle)
            log_battle.save()
            config = Config.objects.get(pk=1)

            if _defender.hp <= 0:
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

        _battle.winner = _winner
        _battle.numberOfRounds = _round
        _battle.save()

        print "End battle"
        msg = "Uma batalha aconteceu, veja o resultado!"
        create_notification(msg, req.challenging)
        create_notification(msg, req.challenged)

    def get(self, *args, **kwargs):
        error = []
        try:
            reBattle = RequisitionBattle.objects.get(pk=self.kwargs['id_requisition'], status="W")
            data = json.dumps({"requisition": json_repr(reBattle) })
        except RequisitionBattle.DoesNotExist:
            error.append("Nao foi possivel recuperar esta requisição pois a batalha já foi aceita")
        except:
            raise
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")

    def post(self, *args, **kwargs):
        try:
            data=json.loads(self.request.body)
            req = RequisitionBattle.objects.get(pk=self.kwargs['id_requisition'])
            if req.status == "W":

                if data['accept'] == 'true' or data['accept'] == 'True':
                    print 'ACCEPT MOTHERFUCK!'
                    self.process_battle(req)

                else:
                    req.status = "C"
                    # Vai remover reputação ?
                    req.save()
                    msg = "O jogador %s nao aceitou sua solicitação de batalha", req.challenged
                    create_notification(msg, req.challenging)
        except:
            raise
        return HttpResponse('OK')


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
            raise
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
            raise
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
            raise
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
            raise
            error.append(sys.exc_info()[0])

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
            raise
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
            raise
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
            raise
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
                    raise
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
                    raise

            data = json.dumps({"response":"OK" })

        except:
            raise
            error.append("Erro ao processar solicitacao")
            pass

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
           return HttpResponse(data ,mimetype="aplication/json")


def create_notification(_message, _to):
    user = UserGame.objects.get(pk=_to.pk)
    msg = Notification(message=_message, user=user)
    msg.save()
