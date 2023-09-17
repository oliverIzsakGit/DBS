from django.shortcuts import render
from curses.ascii import HT
from django.shortcuts import render
from django.db import connections
from django.http import HttpResponse, JsonResponse
import json
import psycopg2 as pg
import os


# Create your views here.
def conn(request):
    connection = pg.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )
    return connection


def patches(request):
    c=conn(request)
    with c:
        with c.cursor() as cur:
            cur.execute('''select  
asd.name as patch_version,
asd.patch_start_date,
asd.patch_end_date,
m.id,
CAST(ROUND(m.duration/60.0, 2) as real) as duration
from 
(select cast(extract(epoch from pa.release_date) as integer) as patch_start_date,
cast(extract(epoch from pap.release_date) as integer) as patch_end_date,
pa.name
from
patches as pa left join patches as pap
on pap.id=pa.id+1 order by pap.id ) as asd
left join matches as m
on m.start_time between asd.patch_start_date and (asd.patch_end_date-1)
order by patch_version,m.id  ''')
            vers=cur.fetchall()
            temp=''
            i=0
            j=0
            duckt={'patches':[]}
            for row in vers:
                if(row[0]!=temp):
                    temp=row[0]
                    
                    duckt['patches'].append({'patch_version':temp,'patch_start_date': row[1], 'patch_end_date': row[2],'matches': []})
                    i=i+1 
                if(row[4]!=None): 
                    duckt['patches'][i-1]['matches'].append({'match_id': row[3], 'duration': row[4]})
                    j=j+1
                   



                
            
            
    return JsonResponse(duckt,safe=True)    

def matches(request,player_id):
    c=conn(request)
    with c:
        with c.cursor() as cur:
            cur.execute('''
SELECT p.id,coalesce(p.nick,'Unknown') as player_nick,h.localized_name as hero_localized_name,CAST(ROUND(m.duration/60.0, 2) AS real) as match_duration_minutes,sum(coalesce(mpd.xp_hero,0)+
coalesce(mpd.xp_creep,0)+coalesce(mpd.xp_other,0)+coalesce(mpd.xp_roshan,0))as experience_gained,mpd.level as level_gained, 
              CASE
                  WHEN (mpd.player_slot=0 or mpd.player_slot=1 or mpd.player_slot=2 or mpd.player_slot=3 or mpd.player_slot=4)  and m.radiant_win='true'
                     THEN true
                  when (mpd.player_slot=0 or mpd.player_slot=128 or mpd.player_slot=129 or mpd.player_slot=130 or mpd.player_slot=131  or mpd.player_slot=132 ) and m.radiant_win='false'
              		then true
					else false
			 END as winner,mpd.match_id
FROM matches_players_details as mpd
join matches as m
on m.id=mpd.match_id
join players as p
on p.id =mpd.player_id 
 join public.heroes as h
on h.id = mpd.hero_id
 where p.id=''' + str(player_id) +'''
group by p.id,mpd.match_id,m.duration,mpd.level,mpd.player_slot,m.radiant_win,hero_localized_name
order by mpd.match_id
''')
            vers=cur.fetchall()
            temp=''
            i=0
            
            
            for row in vers:
                if(temp==''):
                    duckt={'id':row[0],'player_nick':row[1],'matches':[]}
                if(row[7]!=temp):
                    temp=row[7]
                    
                    duckt['matches'].append({'match_id':row[7],'hero_localized_name':row[2],'match_duration_minutes': row[3], 'experiences_gained': row[4],'level_gained': row[5],'winner': row[6] })
                    i=i+1 
                   
            
            
    return JsonResponse(duckt,safe=True) 


def objs(request,player_id):
    c=conn(request)
    with c:
        with c.cursor() as cur:
            cur.execute('''
select p.id,p.nick as player_nick,h.localized_name as hero_localized_name,mpd.match_id,
coalesce(gao.subtype, 'NO_ACTION') AS hero_action,
greatest(COUNT(gao.subtype),1) as count
FROM matches_players_details as mpd
join matches as m
on m.id=mpd.match_id
join players as p
on p.id =mpd.player_id 
join public.heroes as h
on h.id = mpd.hero_id
left join game_objectives as gao
on mpd.id = gao.match_player_detail_id_1
 where p.id=''' + str(player_id) +'''
group by p.id,mpd.match_id,m.duration,mpd.level,mpd.player_slot,m.radiant_win,hero_localized_name,gao.subtype
order by player_nick asc ''' 
)
            vers=cur.fetchall()
            temp=''
            i=0
            j=0
           
            for row in vers:
                if(temp==''):
                    duckt={'id':row[0],'player_nick':row[1],'matches':[]}
                if(row[3]!=temp):
                    temp=row[3]
                    
                    duckt['matches'].append({'match_id':row[3],'hero_localized_name': row[2], 'actions': []})
                    i=i+1 
                   
                duckt['matches'][i-1]['actions'].append({'hero_action': row[4], 'count': row[5]})
                j=j+1
                   
            
            
    return JsonResponse(duckt,safe=True) 



def abilities(request,player_id):
    c=conn(request)
    with c:
        with c.cursor() as cur:
            cur.execute('''
SELECT p.id, COALESCE(p.nick, 'unknown') AS player_nick,
h.localized_name AS hero_localized_name,
m.id AS match_id,
ab.name as ability_name,
COUNT(au.ability_id),
max(au.level) as upgrade_level
FROM players AS p
JOIN matches_players_details AS mpd
ON mpd.player_id = p.id
JOIN matches AS m
ON m.id = mpd.match_id
JOIN heroes AS h
ON h.id = mpd.hero_id
join ability_upgrades as au
on 	au.match_player_detail_id=mpd.id
join abilities as ab
on au.ability_id = ab.id
WHERE p.id = ''' + str(player_id) +'''
GROUP BY au.ability_id, m.id, p.id, h.localized_name,ab.name
ORDER BY m.id,ab.name asc''' 
)
            vers=cur.fetchall()
            temp=''
            i=0
            j=0
           
            for row in vers:
                if(temp==''):
                    duckt={'id':row[0],'player_nick':row[1],'matches':[]}
                if(row[3]!=temp):
                    temp=row[3]
                    
                    duckt['matches'].append({'match_id':row[3],'hero_localized_name': row[2], 'abilities': []})
                    i=i+1 
                   
                duckt['matches'][i-1]['abilities'].append({'ability_name': row[4], 'count': row[5], 'upgrade_level': row[6]})
                j=j+1
                   
            
            
    return JsonResponse(duckt,safe=True) 





def items(request,match_id):
    c=conn(request)
    with c:
        with c.cursor() as cur:
            cur.execute('''
select match_id, hero_id, hero_name, item_id, item_name, count
from(select match_id, hero_id, hero_name, item_id, item_name, count(item_id),
row_number() over(partition by hero_id order by count(item_id) desc, item_name)
from(
select m.id as match_id, h.id as hero_id, h.localized_name as hero_name, 
pl.item_id as item_id, i.name as item_name--, count(pl.item_id) as item_count
from matches as m 
join matches_players_details as mpd on m.id = mpd.match_id
join heroes as h on h.id = mpd.hero_id
join purchase_logs as pl on pl.match_player_detail_id = mpd.id
join items as i on i.id = pl.item_id
where m.id =  ''' + str(match_id) +'''
and ((mpd.player_slot <= 4 and m.radiant_win = true) or (mpd.player_slot >= 128 and m.radiant_win = false))
) as subq1
group by match_id, hero_id, hero_name, item_id, item_name
) as subq2
where row_number <= 5''' 
)
            vers=cur.fetchall()
            temp=''
            i=0
            j=0
           
            for row in vers:
                if(temp==''):
                    duckt={'id':row[0],'heroes':[]}
                if(row[1]!=temp):
                    temp=row[1]
                    
                    duckt['heroes'].append({'id':row[1],'name': row[2], 'top_purchases': []})
                    i=i+1 
                   
                duckt['heroes'][i-1]['top_purchases'].append({'id': row[3], 'name': row[4], 'count': row[5]})
                j=j+1
                   
            
            
    return JsonResponse(duckt,safe=True) 


def hero_abilities(request,hero_abilities_id):
    c=conn(request)
    with c:
        with c.cursor() as cur:
            cur.execute('''
select ability_id, ability_name, hero_id, hero_name, winner, bucket, count
from (
select *, count(bucket) as count,
row_number() over(partition by hero_name, winner order by count(bucket) desc) as rank
from (
select ability_id, ability_name, hero_id, hero_name, winner,case 
when floor(time) between 0 and 9 then '0-9'
when floor(time) between 10 and 19 then '10-19'
when floor(time) between 20 and 29 then '20-29'
when floor(time) between 30 and 39 then '30-39'
when floor(time) between 40 and 49 then '40-49'
when floor(time) between 50 and 59 then '50-59'
when floor(time) between 60 and 69 then '60-69'
when floor(time) between 70 and 79 then '70-79'
when floor(time) between 80 and 89 then '80-89'
when floor(time) between 90 and 99 then '90-99'
when floor(time) >= 100 then '100-109' 
end as bucket
from (
select a.id AS ability_id, a.name AS ability_name, 
100.0*au.time/m.duration as time, h.id as hero_id,
h.localized_name as hero_name,
case when (mpd.player_slot < 5 and m.radiant_win = true) or
(mpd.player_slot > 127 and m.radiant_win = false) then 'win'
else 'lose' end AS winner
from abilities as a
join ability_upgrades as au
on a.id = au.ability_id
join matches_players_details as mpd
on mpd.id = au.match_player_detail_id
join matches as m
on mpd.match_id = m.id
join heroes as h
on h.id = mpd.hero_id
where a.id =''' + str(hero_abilities_id) +'''
) as subq1
) as subq2
group by bucket, ability_id, ability_name, hero_id, hero_name, winner
) as subq3
where rank = 1''' 
)
            vers=cur.fetchall()
            temp=''
            i=0
            j=0
           
            for row in vers:
                if(temp==''):
                    duckt={'id':row[0],'name':row[1],'heroes':[]}
                if(row[2]!=temp):
                    temp=row[2]
                    
                    duckt['heroes'].append({'id':row[2],'name': row[3] })
                    i=i+1 

                if(row[4]=='win'):
                    duckt['heroes'][i-1]['usage_winners']={'bucket': row[5], 'count': row[6]}
                else:
                    duckt['heroes'][i-1]['usage_loosers']={'bucket': row[5], 'count': row[6]}
                j=j+1
                   
            
            
    return JsonResponse(duckt,safe=True) 



def towers(request):
    c=conn(request)
    with c:
        with c.cursor() as cur:
            cur.execute('''
select hid as hero_id,hn as hero_name, max(count) as tower_kills
from (select hid, hn, count(*)from (
select h.id as hid, 
h.localized_name as hn,
(row_number() over(order by mpd.match_id, go.time) -
row_number() over(partition by mpd.match_id, h.id order by mpd.match_id, go.time)) as part
from matches_players_details as mpd
join game_objectives as go
on go.match_player_detail_id_1 = mpd.id
join heroes as h
on h.id = mpd.hero_id
where subtype = 'CHAT_MESSAGE_TOWER_KILL' and match_player_detail_id_1 is not null
order by mpd.match_id, go.time) as subq1
group by part, hid,hn
order by count desc) as subq2
group by hero_id, hero_name
order by max(count) desc, hero_name''' 
)
            vers=cur.fetchall()
            temp=''
            i=0
            j=0
           
            for row in vers:
                if(temp==''):
                    duckt={'heroes':[]}
                if(row[0]!=temp):
                    temp=row[0]
                    
                    duckt['heroes'].append({'id':row[0],'name': row[1],'tower_kills':row[2]})
                    i=i+1 

            
                   
            
            
    return JsonResponse(duckt,safe=True) 