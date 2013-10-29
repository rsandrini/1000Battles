# -*- coding: utf-8 -*-

from django.views.generic import View
from core.models import *
import json
from django.http import HttpResponse


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
            itens = Item.objects.filter(user=user)
            friends = Friend.objects.filter(user=user)
        except ex:
            error.append(ex.message)

        data = []
        data.append(user)
        data.append(itens)
        data.append(friends)

        if error:
            return HttpResponse(json.dumps(error), mymetype="aplication/json")
        else:
            return HttpResponse(json.dumps(data), mymetype="aplication/json")


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
