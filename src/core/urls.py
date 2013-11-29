from django.conf.urls import patterns, include, url
from core.views import *


urlpatterns = patterns('',
    #url(r'^/', include('src.core.urls')),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^dashboard/(?P<id>\d+)/$', DashboardView.as_view(), name="dashboard"),
    #Show all battles for user
    url(r'^battles/(?P<id>\d+)/$', BattleView.as_view(), name="battleAll"),
    # Show all requisitions for battles
    url(r'^battles_requisition/(?P<id>\d+)/$', ShowBattlesRequisitionView.as_view(), name="battleRequisition"),
    # Confirm requisition for battle
    url(r'^battle_requisition_confirm/(?P<id_requisition>\d+)/$', BattleRequisitionConfirmView.as_view(), name="battleRequisitionConfirm"),
    # send a challenge
    url(r'^battle_challenge/$', BattleRequisitionView.as_view(), name="battleRequisition"),
    # show a battle
    url(r'^battle/(?P<id_battle>\d+)/$', ShowBattleView.as_view(), name="battleShow"),
    url(r'^all_itens/$', ShowAllItensView.as_view(), name="itensShow"),
    url(r'^my_itens/(?P<id>\d+)/$', ShowMyItensView.as_view(), name="itensMyShow"),
    url(r'^ranking/$', ShowRankingView.as_view(), name="ranking"),
    url(r'^setitem/(?P<id>\d+)/$', SetItemView.as_view(), name="set_item"),
    url(r'^friends/(?P<id>\d+)/$', FriendsView.as_view(), name="friends"),
    url(r'^player/(?P<id>\d+)/$', ShowEnemyView.as_view(), name="friends"),
    url(r'^messages/(?P<id>\d+)/$', MessageView.as_view(), name="messages"),
)
