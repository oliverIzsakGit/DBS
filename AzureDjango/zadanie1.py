from django.shortcuts import render
from curses.ascii import HT
from django.shortcuts import render
from django.db import connections
from django.http import HttpResponse, JsonResponse
import json
import psycopg2 as pg
import os


# Create your views here.
def req(request):
    connection = pg.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
    )
    with connection:
        with connection.cursor() as cur:
            cur.execute("SELECT VERSION();")
            vers,=cur.fetchone()
            cur.execute("SELECT pg_database_size('dota2')/1024/1024 as dota2_db_size;")
            dbSize, = cur.fetchone()        
    temp = { "pgsql" : {"version" : '',"dota2_db_size" : ''} } 
    temp["pgsql"]["version"]=str(vers)
    temp["pgsql"]["dota2_db_size"]= str(dbSize)
    return JsonResponse((temp),safe=True)       