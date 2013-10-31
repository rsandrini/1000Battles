# -*- coding: utf-8 -*-

from django.views.generic import View
from core.models import *
import json
from django.http import HttpResponse
import sys
from core.utils import *


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
    pass


'''
   Accept or decline battle requisition
'''
class ConfirmBattleView(View):
    pass


class ShowBattleView(View):
    pass


class ShowAllItensView(View):
    pass


class ShowMyItensView(View):
    pass


class ShowRankingView(View):
    pass


class FriendsView(View):
    pass


class ShowEnemyView(View):
    pass
