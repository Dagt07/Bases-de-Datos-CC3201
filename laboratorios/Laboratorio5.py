import psycopg2
import psycopg2.extras
import csv
import re

conn = psycopg2.connect(host="*****",
    database="*****",
    user="*****",
    password="*****", port="1234")

cur = conn.cursor()

def findOrInsertCharacter(table, name):
    cur.execute("select id from "+table+" where name=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (name) values (%s) returning id", [name])
        return cur.fetchone()[0]

def findOrInsertSuperhero(table, id, name, intelligence, strength, speed):
    cur.execute("select id from "+table+" where name=%s limit 1", [name])
    r = cur.fetchone()
    if(r):
        return r[0]
    else:
        cur.execute("insert into "+table+" (id,name,intelligence,strength,speed) values (%s,%s,%s,%s,%s) returning id", [id, name, intelligence, strength, speed])
        return cur.fetchone()[0]

with open('lab5_data_align.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i==1:
            continue
        
        #----------------------------------CREACIÓN DEL SUPERHEROE------------------------------
        # i) Selección id personaje
        name = row[8] #name = bruce wayne
        if (name == "null"):
            name = row[1]
        id = findOrInsertCharacter('character_vadg',name.strip()) #id = 70

        # ii) Selección id superheroe
        supername = row[1]
        intelligence = row[2] if row[2]!= "null" else "0"
        strength = row[3] if row[3]!= "null" else "0"
        speed = row[4] if row[4]!= "null" else "0"

        character_id = findOrInsertSuperhero('superheroe_vadg', id, supername.strip(), intelligence.strip(), strength.strip(), speed.strip())
        
        # iii) Para cada Alter Ego

        ## FORMA ENUNCIADO
        ## A formatear
        alter_ego = re.split(r'[;,]',row[9]) # Separado en lista por ',' o ';'
        alter_ego = [m.strip() for m in alter_ego] # Sin espacios en blanco al inicio y al final
        alter_ego = [re.sub("'","", m) for m in alter_ego] #eliminar comillas dobles
        ## B Buscar o insertar
        alter_ego_id = []
        for alterego in alter_ego:
            alter_ego_id.append(findOrInsertCharacter('alterego_vadg', alterego.strip()))

        # iv) Para Ocupación o oficio
        ## A formatear
        work_ocupation = re.split(r'[;,]',row[23]) # Separado en lista por ',' o ';'
        work_ocupation = [m.strip() for m in work_ocupation] # Sin espacios en blanco al inicio y al final
        work_ocupation = [re.sub("'","", m) for m in work_ocupation] #eliminar comillas dobles
        work_ocupation = [m.lower() for m in work_ocupation]
        ## B Buscar o insertar
        work_ocupation_id = []
        for work in work_ocupation:
            work_ocupation_id.append(findOrInsertCharacter('workocupation_vadg', work.strip()))
        ## C Crear relación super - ocupación
        for work_id in work_ocupation_id:
            cur.execute("select * from super_work_vadg where (superh_id, work_id) = (%s, %s) limit 1", [character_id, work_id])
            if(not cur.fetchone()):
                cur.execute("insert into super_work_vadg (superh_id, work_id) values (%s, %s)", [character_id, work_id])
            
        # EXTRA Crear relacion super - alterego
        for alter_ego in alter_ego_id:
            cur.execute("select * from super_alterego_vadg where (super_id, alterego_id) = (%s, %s) limit 1", [character_id, alter_ego])
            if(not cur.fetchone()):
                cur.execute("insert into super_alterego_vadg (super_id, alterego_id) values (%s, %s)", [character_id, alter_ego])    

#----------------------------------Parte B----------------------------------------------------------
with open('lab5_data_align.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    i = 0
    for row in reader:
        i+=1
        if i==1:
            continue

        #----------------------------------CREACIÓN DE LOS PARIENTES--------------------------------
        # i) Selección id personaje
        name = row[8] #name = bruce wayne
        if (name == "null"):
            name = row[1]
        id = findOrInsertCharacter('character_vadg',name.strip()) #id = 70

        relation = row[26] if row[26]!= "-" else None
        # ii) ignorar filas con relación vacía
        if (relation != None):
            # iii) Selección id pariente
            ## A
            relation = re.split(r'[;,]',relation) # Separado en lista por ',' o ';'
            relation = [m.strip() for m in relation] # Sin espacios en blanco al inicio y al final
            relation = [re.sub("\"","", m) for m in relation] #eliminar comillas dobles
            ## B
            valid_relation = []
            relation_type = []

            for rel in relation:
                groups = re.search(r"([^()]+)\s*(([^)]+))", rel)
                valid_relation.append(relation.group(1).strip())
                relation_type.append(relation.group(2).replace("(","").strip())

            k=0
            for m in relation_type:
                relation_type[i] = m.split(',')[0].strip()
                k +=1
            ## C Buscar o Insertar
            pariente_id = []
            for pariente in valid_relation:
                pariente_id.append(findOrInsertCharacter('relation_vadg', pariente.strip()))
            ## D Crear relación super - pariente
            for par_id in pariente_id:
                cur.execute("select * from relatedto_vadg where (relation_id, character_id) = (%s, %s) limit 1", [par_id, id])
                if(not cur.fetchone()):
                    cur.execute("insert into relatedto_vadg (relation_id, character_id) values (%s, %s)", [par_id, id])
        
    conn.commit()
conn.close()