from django.conf.urls import patterns, include, url
from core.views import *


urlpatterns = patterns('',
    #url(r'^/', include('src.core.urls')),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^dashboard/(?P<id>\d+)/$', DashboardView.as_view(), name="dashboard"),
    url(r'^battles/(?P<id>\d+)/$', BattleView.as_view(), name="battleView"),
    url(r'^battles_requisition/(?P<id>\d+)/$', BattlesRequisitionView.as_view(), name="battleView"),
    url(r'^battle_requisition_confirm/(?P<id_requisition>\d+)/$', BattleRequisitionConfirmView.as_view(), name="battleView"),
    url(r'^confirm_battle/(?P<id_battle>\d+)/(?P<id>\d+)/$', ConfirmBattleView.as_view(), name="battleConfirm"),
    url(r'^battle/(?P<id_battle>\d+)/$', ShowBattleView.as_view(), name="battleShow"),
    url(r'^all_itens/$', ShowAllItensView.as_view(), name="itensShow"),
    url(r'^my_itens/(?P<id>\d+)/$', ShowMyItensView.as_view(), name="itensMyShow"),
    url(r'^ranking/$', ShowRankingView.as_view(), name="ranking"),
    url(r'^friends/(?P<id>\d+)/$', FriendsView.as_view(), name="friends"),
    url(r'^player/(?P<id>\d+)/$', ShowEnemyView.as_view(), name="friends"),
)
