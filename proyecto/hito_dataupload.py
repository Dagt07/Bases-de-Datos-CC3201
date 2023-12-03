import psycopg2
import psycopg2.extras
import csv
import re

conn = psycopg2.connect(host="localhost",
    database="batos",
    user="postgres",
    password="password", port="5432")

cur = conn.cursor()

def findOrInsertPlayer(table, name):
    cur.execute("select player_id from "+table+" where name=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (name,age) values (%s,%s) returning player_id", [name,0])
        return cur.fetchone()[0]

def findOrInsertTeam(table, name, abb):
    cur.execute("select team_id from "+table+" where teamname=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (teamname,abbreviation) values (%s,%s) returning team_id", [name,abb])
        return cur.fetchone()[0]

def findOrInsertSeason(table, year, league):
    cur.execute("select season_id from "+table+" where year=%s limit 1", [year])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (year,league) values (%s,%s) returning season_id", [year,league])
        return cur.fetchone()[0]


def findTeamNameByAbb(table,abb):
    cur.execute("select team_id FROM "+table+" where abbreviation=%s", [abb])    
    r = cur.fetchone()
    if(r):
        return r[0]


def findOrInsertTeamSeason(table, season_id,team_id, x2P, x2PA, x2Pp, FTp, FG, FGA,FGp, FT, x3P, x3PA, x3Pp, assists, pf, blocks, drb, stl):
    cur.execute("select season_id, team_id from "+table+" where season_id=%s and team_id=%s limit 1", [season_id, team_id])
    r = cur.fetchone()
    if(r):
        return r[0] 

    else:
        cur.execute("insert into "+table+" (season_id,team_id,x2p,x2pa,x2pp,ftp,fg,fga,fgp,ft,x3p,x3pa,x3pp,stl,assists,pf,blocks,drb) values \
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning season_id, team_id", \
                    [season_id,team_id, x2P, x2PA, x2Pp, FTp, FG, FGA, FGp, FT, x3P, x3PA, x3Pp, stl, assists, pf, blocks, drb])
        return cur.fetchone()[0] #Deberia retornar una tupla según David



def findOrInserPlayerTeamSeason(table,p_id,ts_s_id,ts_t_id,experience,player_pos,x3P,FGA,FG,x2P,dbpm,obpm,ows,dws,x2PA,x3PA,FTp,FT,x3Pp,FGp,x2Pp,assists,pf,blocks,drb,stl,avg_dist_fga):
    cur.execute("select player_id, team_id, season_id from "+table+" where player_id=%s and season_id=%s and team_id=%s  limit 1", [p_id, ts_s_id, ts_t_id])
    r = cur.fetchone()
    if(r):
        return r[0] 
    else:
        cur.execute("insert into "+table+" (player_id,team_id,season_id,experience,player_position,x3p,fga,fg,x2p,dbpm,obpm,ows,dws,x2pa,x3pa,ftp,ft,x3pp,fgp,x2pp,assits,pf,blocks,drb,stl,avg_dist_fga) values \
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) returning id", \
                    [p_id,ts_t_id,ts_s_id,experience,player_pos,x3P,FGA,FG,x2P,dbpm,obpm,ows,dws,x2PA,x3PA,FTp,FT,x3Pp,FGp,x2Pp,assists,pf,blocks,drb,stl,avg_dist_fga])
        return cur.fetchone()[0] 
    

def findPlayerTeamSeasonByids(table,player_id,season_id,team_id):
    cur.execute("select id FROM "+table+" where player_id=%s and season_id=%s and team_id=%s", [player_id,season_id,team_id])    
    r = cur.fetchone()
    if(r):
        return r[0]


def findOrInsertawards(table,award,pts_id,pts_won):
    cur.execute("select award, pts_id from "+table+" where award=%s and pts_id=%s limit 1", [award, pts_id])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (award,pts_id,ptos_won) values (%s,%s,%s) returning award, pts_id", [award,pts_id,pts_won])
        return cur.fetchone()[0]

#----------------------- Insertar Team y Season -----------------------
with open('archivos/TeamTotals.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i==1:
            continue      
        #----------------------- Insertar Team -----------------------
        team_name=row[2]
        abb= row[3].strip()
        team_id=findOrInsertTeam("batos.team",team_name,abb)
        #----------------------- Insertar Season -----------------------
        year = row[0]
        league = row[1]
        season_id = findOrInsertSeason("batos.season", year, league)
        #--------------------- Insertar TeamSeason -------------------
        expresion_regular = r'\bNA\w*\b'

        x2P = row[13]   if not re.findall(expresion_regular,row[13]) else 0
        x2PA = row[14]  if not re.findall(expresion_regular,row[14]) else 0
        x2Pp = row[15]  if not re.findall(expresion_regular,row[15]) else 0.0
        x3P = row[10]   if not re.findall(expresion_regular,row[10]) else 0
        x3PA = row[11]  if not re.findall(expresion_regular,row[11]) else 0
        x3Pp = row[12]  if not re.findall(expresion_regular,row[12]) else 0.0
        FT = row[16]    if not re.findall(expresion_regular,row[16]) else 0
        FTp = row[17]   if not re.findall(expresion_regular,row[17]) else 0.0
        FG = row[7]     if not re.findall(expresion_regular,row[7]) else 0
        FGA = row[8]    if not re.findall(expresion_regular,row[8]) else 0
        FGp = row[9]    if not re.findall(expresion_regular,row[9]) else 0.0
        assists=row[22] if not re.findall(expresion_regular,row[22]) else 0
        pf = row[26]    if not re.findall(expresion_regular,row[26]) else 0
        blocks =row[24] if not re.findall(expresion_regular,row[24]) else 0
        drb = row[20]   if not re.findall(expresion_regular,row[20]) else 0
        stl = row[23]   if not re.findall(expresion_regular,row[23]) else 0
        team_season_id = findOrInsertTeamSeason("batos.team_season",season_id,team_id,x2P,x2PA,x2Pp,FTp,FG,FGA,FGp,FT,x3P,x3PA,x3Pp,assists,pf,blocks,drb,stl)

#----------------------- Insertar Player y PlayerTeamSeason -----------------------
with open('archivos/PlayerTotals.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i==1:
            continue
    #------------Insertar Player----------------------------------#
        #findorinsertTEAM = team_id
        abb= row [9].strip()
        team_id=findTeamNameByAbb("batos.team",abb)
        year=row[1]
        season_id=findOrInsertSeason("batos.season",year,"error")
        
        name = row[3]
        #age = row[4]
        player_id = findOrInsertPlayer("batos.player", name)
    #-----------------Insertar PlayerTeamSeason-----------#
        expresion_regular = r'(^$|\bNA\w*\b|\s+)'

        experience= row[7]  if not re.findall(expresion_regular,row[7]) else 0
        player_pos=row[5]  
        x3P=row[16]         if not re.findall(expresion_regular,row[16]) else 0
        FGA= row[14]        if not re.findall(expresion_regular,row[14]) else 0
        FG=row[13]          if not re.findall(expresion_regular,row[13]) else 0
        x2P=row[19]         if not re.findall(expresion_regular,row[19]) else 0
        dbpm=row[36]        if not re.findall(expresion_regular,row[36]) else 0.0
        obpm=row[35]        if not re.findall(expresion_regular,row[35]) else 0.0
        ows=row[37]         if not re.findall(expresion_regular,row[37]) else 0.0
        dws=row[38]         if not re.findall(expresion_regular,row[38]) else 0.0
        x2PA=row[20]        if not re.findall(expresion_regular,row[20]) else 0
        x3PA=row[17]        if not re.findall(expresion_regular,row[17]) else 0 
        FTp=row[25]         if not re.findall(expresion_regular,row[25]) else 0.0
        FT=row[23]          if not re.findall(expresion_regular,row[23]) else 0
        x3Pp=row[18]        if not re.findall(expresion_regular,row[18]) else 0.0
        FGp=row[15]         if not re.findall(expresion_regular,row[15]) else 0.0
        x2Pp=row[21]        if not re.findall(expresion_regular,row[21]) else 0.0
        assists=row[29]     if not re.findall(expresion_regular,row[29]) else 0
        pf=row[33]          if not re.findall(expresion_regular,row[33]) else 0
        blocks=row[31]      if not re.findall(expresion_regular,row[31]) else 0
        drb=row[27]         if not re.findall(expresion_regular,row[27]) else 0
        stl=row[30]         if not re.findall(expresion_regular,row[30]) else 0
        avg_dist_fga=row[39]    if not re.findall(expresion_regular,row[39]) else 0.0
        Player_Team_Season_id=findOrInserPlayerTeamSeason("batos.player_team_season",player_id,season_id,team_id,experience,player_pos,x3P
                                                          ,FGA,FG,x2P,dbpm,obpm,ows,dws,x2PA,x3PA,FTp,FT,x3Pp,FGp,x2Pp,assists,pf,blocks,drb,stl,avg_dist_fga)
        
#---------------------------- Insertar awards ------------------------------#
with open('archivos/PlayerAwardShares.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    expresion_regular = r'\bNA\w*\b'
    i = 0
    for row in reader:
        i+=1
        if i==1:
            continue 
        
        name=row[2]
        year=row[0]
        abb=row[4].strip()
        player_id = findOrInsertPlayer("batos.player", name)
        season_id=findOrInsertSeason("batos.season",year,"error")
        team_id=findTeamNameByAbb("batos.team",abb)
        Player_Team_Season_id = findPlayerTeamSeasonByids("batos.player_team_season", player_id, season_id, team_id)

        if Player_Team_Season_id is None:
            continue
        else:
            award=row[1]
            pts_won=row[6]  if not re.findall(expresion_regular,row[6]) else 0
            player_award_shares=findOrInsertawards("batos.awards", award, Player_Team_Season_id, pts_won)

#---------------------------- Commit & Close ------------------------------# 
    conn.commit()
conn.close()