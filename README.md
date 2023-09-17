"\# zadanie-stv10-findura-oliverIzsakGit"

Zadanie 1

commit: 4761ac16ec888a2c53176cf533a68122b6a13a01

Zadanie 2

commit : a9a7c2293fe83567bb9ed0c7dc2e19603f83124c

Zadanie 3

commit : 80f3563c12d252bef5891b74c32cba49dd9a0dce

https://fiit-dbs-xizsak-app.azurewebsites.net

1.endpoint:

select\
asd.name as patch\_version, asd.patch\_start\_date,
asd.patch\_end\_date, m.id, CAST(ROUND(m.duration/60.0, 2) as real) as
duration from (select cast(extract(epoch from pa.release\_date) as
integer) as patch\_start\_date, cast(extract(epoch from
pap.release\_date) as integer) as patch\_end\_date, pa.name from patches
as pa left join patches as pap on pap.id=pa.id+1 order by pap.id ) as
asd left join matches as m on m.start\_time between
asd.patch\_start\_date and (asd.patch\_end\_date-1) order by
patch\_version,m.id

2.endpoint:

SELECT p.id,coalesce(p.nick,'Unknown') as player\_nick,h.localized\_name
as hero\_localized\_name,CAST(ROUND(m.duration/60.0, 2) AS real) as
match\_duration\_minutes,sum(coalesce(mpd.xp\_hero,0)+
coalesce(mpd.xp\_creep,0)+coalesce(mpd.xp\_other,0)+coalesce(mpd.xp\_roshan,0))as
experience\_gained,mpd.level as level\_gained, CASE WHEN
(mpd.player\_slot=0 or mpd.player\_slot=1 or mpd.player\_slot=2 or
mpd.player\_slot=3 or mpd.player\_slot=4) and m.radiant\_win='true' THEN
true when (mpd.player\_slot=0 or mpd.player\_slot=128 or
mpd.player\_slot=129 or mpd.player\_slot=130 or mpd.player\_slot=131 or
mpd.player\_slot=132 ) and m.radiant\_win='false' then true else false
END as winner,mpd.match\_id FROM matches\_players\_details as mpd join
matches as m on m.id=mpd.match\_id join players as p on p.id
=mpd.player\_id join public.heroes as h on h.id = mpd.hero\_id where
p.id=1 group by
p.id,mpd.match\_id,m.duration,mpd.level,mpd.player\_slot,m.radiant\_win,hero\_localized\_name
order by mpd.match\_id

3.endpoint:

select p.id,p.nick as player\_nick,h.localized\_name as
hero\_localized\_name,mpd.match\_id, coalesce(gao.subtype, 'NO\_ACTION')
AS hero\_action, greatest(COUNT(gao.subtype),1) as count FROM
matches\_players\_details as mpd join matches as m on m.id=mpd.match\_id
join players as p on p.id =mpd.player\_id join public.heroes as h on
h.id = mpd.hero\_id left join game\_objectives as gao on mpd.id =
gao.match\_player\_detail\_id\_1 where p.id=1 group by
p.id,mpd.match\_id,m.duration,mpd.level,mpd.player\_slot,m.radiant\_win,hero\_localized\_name,gao.subtype
order by player\_nick asc

4.endpoint:

SELECT p.id, COALESCE(p.nick, 'unknown') AS player\_nick,
h.localized\_name AS hero\_localized\_name, m.id AS match\_id, ab.name
as ability\_name, COUNT(au.ability\_id), max(au.level) as upgrade\_level
FROM players AS p JOIN matches\_players\_details AS mpd ON
mpd.player\_id = p.id JOIN matches AS m ON m.id = mpd.match\_id JOIN
heroes AS h ON h.id = mpd.hero\_id join ability\_upgrades as au on
au.match\_player\_detail\_id=mpd.id join abilities as ab on
au.ability\_id = ab.id WHERE p.id = 1 GROUP BY au.ability\_id, m.id,
p.id, h.localized\_name,ab.name ORDER BY m.id,ab.name asc

Zadanie 5

commit : 5997e783095fd9b38cdfe707c9157aa53466f0fc

https://fiit-dbs-xizsak-app.azurewebsites.net

1.  endpoint:

select match\_id, hero\_id, hero\_name, item\_id, item\_name, count
from(select match\_id, hero\_id, hero\_name, item\_id, item\_name,
count(item\_id), row\_number() over(partition by hero\_id order by
count(item\_id) desc, item\_name) from( select m.id as match\_id, h.id
as hero\_id, h.localized\_name as hero\_name, pl.item\_id as item\_id,
i.name as item\_name--, count(pl.item\_id) as item\_count from matches
as m join matches\_players\_details as mpd on m.id = mpd.match\_id join
heroes as h on h.id = mpd.hero\_id join purchase\_logs as pl on
pl.match\_player\_detail\_id = mpd.id join items as i on i.id =
pl.item\_id where m.id = ''' + str(match\_id) +''' and
((mpd.player\_slot \<= 4 and m.radiant\_win = true) or (mpd.player\_slot
\>= 128 and m.radiant\_win = false)) ) as subq1 group by match\_id,
hero\_id, hero\_name, item\_id, item\_name ) as subq2 where row\_number
\<= 5

2.  endpoint:

select ability\_id, ability\_name, hero\_id, hero\_name, winner, bucket,
count from ( select *, count(bucket) as count, row\_number()
over(partition by hero\_name, winner order by count(bucket) desc) as
rank from ( select ability\_id, ability\_name, hero\_id, hero\_name,
winner,case when floor(time) between 0 and 9 then '0-9' when floor(time)
between 10 and 19 then '10-19' when floor(time) between 20 and 29 then
'20-29' when floor(time) between 30 and 39 then '30-39' when floor(time)
between 40 and 49 then '40-49' when floor(time) between 50 and 59 then
'50-59' when floor(time) between 60 and 69 then '60-69' when floor(time)
between 70 and 79 then '70-79' when floor(time) between 80 and 89 then
'80-89' when floor(time) between 90 and 99 then '90-99' when floor(time)
\>= 100 then '100-109' end as bucket from ( select a.id AS ability\_id,
a.name AS ability\_name, 100.0*au.time/m.duration as time, h.id as
hero\_id, h.localized\_name as hero\_name, case whne (mpd.player\_slot
\< 5 AND m.radiant\_win = true) or (mpd.player\_slot \> 127 and
m.radiant\_win = false) then 'win' else 'lose' end AS winner from
abilities as a join ability\_upgrades as au on a.id = au.ability\_id
join matches\_players\_details as mpd on mpd.id =
au.match\_player\_detail\_id join matches as m on mpd.match\_id = m.id
join heroes as h on h.id = mpd.hero\_id where a.id =''' +
str(hero\_abilities\_id) +''' ) as subq1 ) as subq2 group by bucket,
ability\_id, ability\_name, hero\_id, hero\_name, winner ) as subq3
where rank = 1

3.  endpoint:

select hid as hero\_id,hn as hero\_name, max(count) as tower\_kills from
(select hid, hn, count(\*)from ( select h.id as hid, h.localized\_name
as hn, (row\_number() over(order by mpd.match\_id, go.time) -
row\_number() over(partition by mpd.match\_id, h.id order by
mpd.match\_id, go.time)) as part from matches\_players\_details as mpd
join game\_objectives as go on go.match\_player\_detail\_id\_1 = mpd.id
join heroes as h on h.id = mpd.hero\_id where subtype =
'CHAT\_MESSAGE\_TOWER\_KILL' and match\_player\_detail\_id\_1 is not
null order by mpd.match\_id, go.time) as subq1 group by part, hid,hn
order by count desc) as subq2 group by hero\_id, hero\_name order by
max(count) desc, hero\_name

Zadanie 6
Commit: d053f9ae278b21bc55726d704f38b0eb70a914cc
