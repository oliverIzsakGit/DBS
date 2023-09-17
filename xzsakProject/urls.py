"""xzsakProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from AzureDjango import zadanie1
from AzureDjango import Zadanie2
from AzureDjango import zadanie4

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/health/', zadanie1.req, name='zadanie1'),
    path('v2/patches/',Zadanie2.patches,name='patches'),
    path('v2/players/<int:player_id>/game_exp/',Zadanie2.matches,name='exp'),
    path('v2/players/<int:player_id>/game_objectives/',Zadanie2.objs,name='actions'),
    path('v2/players/<int:player_id>/abilities/',Zadanie2.abilities,name='abilities'),
    path('v3/matches/<int:match_id>/top_purchases/',Zadanie2.items,name='items'),
    path('v3/abilities/<int:hero_abilities_id>/usage/',Zadanie2.hero_abilities,name='hero_abilities'),
    path('v3/statistics/tower_kills/',Zadanie2.towers,name='towers'),
    path('v4/patches/',zadanie4.patches,name='patches'),
    path('v4/players/<int:player_id>/game_exp/',zadanie4.matches,name='exp'),
    path('v4/players/<int:pl_id>/game_objectives/',zadanie4.objs,name='actions'),
    path('v4/players/<int:pl_id>/abilities/',zadanie4.abilities,name='abilities'),
    path('v4/matches/<int:match_id>/top_purchases/',zadanie4.items,name='items'),
    path('v4/abilities/<int:hero_abilities_id>/usage/',zadanie4.hero_abilities,name='hero_abilities'),
    path('v4/statistics/tower_kills/',zadanie4.towers,name='towers'),
]
