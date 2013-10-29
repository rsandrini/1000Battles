from django.conf.urls import patterns, include, url
from core.views import *


urlpatterns = patterns('',
    #url(r'^/', include('src.core.urls')),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^dashboard/(?P<id>\d+)/$', DashboardView.as_view(), name="dashboard"),
    url(r'^battles/(?P<id>\d+)/$', BattleView.as_view(), name="battleView"),
    url(r'^confirm_battle/(?P<id_battle>\d+)/(?P<id>\d+)/$', ConfirmBattleView.as_view(), name="battleConfirm"),
    url(r'^show_battle/(?P<id_battle>\d+)/$', ShowBattleView.as_view(), name="battleShow"),
    url(r'^show_all_itens/$', ShowAllItensView.as_view(), name="itensShow"),
    url(r'^show_my_itens/$', ShowMyItensView.as_view(), name="itensMyShow"),
    url(r'^show_ranking/$', ShowRankingView.as_view(), name="ranking"),
    url(r'^show_friends/(?P<id>\d+)/$', FriendsView.as_view(), name="friends"),
    url(r'^show_enemy/(?P<id_enemy>\d+)/$', ShowEnemyView.as_view(), name="friends"),
)
