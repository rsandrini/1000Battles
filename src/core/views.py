# -*- coding: utf-8 -*-

from django.views.generic import View
from core.models import *
import json
from django.http import HttpResponse
import sys
from core.utils import *
from django.db.models import Q

class IndexView(View):
    def get(self, *args, **kwargs):

        return HttpResponse(json.dumps("TESTE"), mimetype="application/json")


class LoginView(View):
    def get(self, *args, **kwargs):
        return HttpResponse(json.dumps("OK"), mimetype="application/json")


class RegisterView(View):
    pass


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
{"friends": "[{\"friend\": \"\\\"XxXAssassinoXxX\\\"\"}, {\"friend\": \"\\\"HueHueHue\\\"\"}, {\"friend\": \"\\\"PowerDieMotherFuck\\\"\"}]", "user": "{\"name\": \"Matador\", \"head_id\": \"None\", \"hp\": 10.0, \"_state\": {\"adding\": false, \"db\": \"default\"}, \"arm_id\": \"None\", \"leg_id\": \"None\", \"reputation\": 0.0, \"chest_id\": \"None\", \"xp\": 0.0, \"id\": 1}"}
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


class BattlesRequisitionView(View):
    def get(self, *args, **kwargs):
        idUser = self.kwargs['id']
        error = []
        try:
            user = UserGame.objects.get(pk=idUser)
            reBattles = RequisitionBattle.objects.filter(Q(challenging=user) | Q(challenged=user))
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


class BattleRequisitionConfirmView(View):
    def get(self, *args, **kwargs):
        error = []
        try:
            reBattle = RequisitionBattle.objects.get(pk=self.kwargs['id_requisition'], status="W")
            data = json.dumps({"requisition": json_repr(reBattle) })
        except:
            raise
            error.append(sys.exc_info()[0])

        if error:
            return HttpResponse(json.dumps(error), mimetype="aplication/json")
        else:
            return HttpResponse(data ,mimetype="aplication/json")

    '''
    curl -X POST -H "Content-Type: application/json" -d '{"username":"xyz","password":"xyz"}' http://localhost:8000/battle_requisition_confirm/3/

    {"accept":"True"}
    '''

    def post(self, *args, **kwargs):
        try:
            data=json.loads(self.request.body)

            print data
        except:
            raise
        return HttpResponse('')
'''
   Accept or decline battle requisition
'''
class ConfirmBattleView(View):
    pass


class ShowBattleView(View):
    pass


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


