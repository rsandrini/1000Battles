# -*- coding: utf-8 -*-

from django.views.generic import View
from core.models import *
import json
from django.http import HttpResponse


class IndexView(View):
    def get(self, *args, **kwargs):

        return HttpResponse(json.dumps("TESTE"), mimetype="application/json")


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse(json.dumps("OK"), mimetype="application/json")


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
        data.append(itens)
        data.append(friends)

        if error:
            return HttpResponse(json.dumps(error), mymetype="aplication/json")
        else:
            return HttpResponse(json.dumps(data), mymetype="aplication/json")


class BattlesView(View):
    pass


class FriendsView(View):
    pass
