#Created by Helkds
#Last Modified 18-08-2025
'''
    Reads Employee CSV file exported from ERPNext / MetaGest.
    Check if Employee Active and if ATTENDANCE ID assigned
    Adds Employess to ZKTECO.
'''
import sys
import csv

import os
import json

from dotenv import load_dotenv

load_dotenv()


import importlib.util

spec = importlib.util.spec_from_file_location("hikvision_isapi", "./hikvision_isapi/client.py")
hikvision_C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hikvision_C)

hikvision_client = hikvision_C.HikvisionClient(
    base_url=os.getenv("HIK_URL", "http://192.168.8.25"),
    username=os.getenv("HIK_USERNAME", "admin"),
    password=os.getenv("HIK_PASSWORD", "admin2025"),
)

def ler_ficheiro(ficheiro):
        
    func_not_added = []
    func_adicionar_bio = {'nome':[],'attid':[]}
    # opening the CSV file
    if ficheiro:
        ficheiro_csv = ficheiro
    else:
        #Tem que estar no mesmo directorio que a Script.
        ficheiro_csv = 'lista_funcionarios.csv'
    with open(ficheiro_csv, mode ='r')as file:
        # reading the CSV file
        csvFile = csv.reader(file)
        # displaying the contents of the CSV file
        for idx,lines in enumerate(csvFile):
            print ("lines ")
            print ('idx ', idx)
            print (lines)
            if idx >0:
                print ('lines 3 (Status) ', lines[3])
                print ('lines 4 (NOME) ', lines[4])
                if lines[3] != 'Left':
                    #0 Number,1 NAME, 2 Full Name, 3 Attendance ID, 4 Status
                    print ('Verifica se tem o Numero do Attendance ID...')
                    if lines[5]:
                        print ('Adicionar ao Biometrico.... ', lines[1])
                        func_adicionar_bio['nome'].append(lines[4])
                        func_adicionar_bio['attid'].append(lines[5])
                    else:
                        print ('Este Funcinonario {} nao tem ID do BIOMETRICO... '.format(lines[1]))
                        func_not_added.append(lines[1])

        if func_not_added:
            print ('lista de Funcionarios nao adicionados...')
            print (*func_not_added,sep='\n')
        print (len(func_adicionar_bio))
        print (len(func_adicionar_bio['nome']))
    return func_adicionar_bio

def actualizar_hikvision(deviceIP,func_adicionar_bio):
    conn = None
    # create ZK instance
    #zk = ZK(deviceIP, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    

    try:
        # connect to device
        #conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        #conn.disable_device()
        # Create users
        if func_adicionar_bio:
            cc = 0
            while cc < len(func_adicionar_bio['nome']):
                #conn.set_user(uid=int(func_adicionar_bio['attid'][cc]), name=str(func_adicionar_bio['nome'][cc]), privilege='User', password='12345678', group_id='', user_id=func_adicionar_bio['attid'][cc], card=0)
                novoUser = hikvision_client.create_user(empNo=func_adicionar_bio['attid'][cc],empName=str(func_adicionar_bio['nome'][cc]))
                print ('********Creating... NEW USER')
                print (novoUser.status_code)
                print (novoUser.text)

                cc += 1

        #users = conn.get_users()
        lista_users = hikvision_client.search_all_emps()
        listausers = json.loads(lista_users.text)['UserInfoSearch']['UserInfo']
        for user in listausers:
            privilege = 'User'
            #if user.privilege == const.USER_ADMIN:
            #    privilege = 'Admin'
            '''
            print ('+ UID #{}'.format(user.uid))
            print ('  Name       : {}'.format(user.name))
            print ('  Privilege  : {}'.format(privilege))
            print ('  Password   : {}'.format(user.password))
            print ('  Group ID   : {}'.format(user.group_id))
            print ('  User  ID   : {}'.format(user.user_id))
            '''

            print ('=============')
            print (user)
            print ('emp ', user['employeeNo'])

            print ('+ EmployeeNo #{}'.format(user['employeeNo']))
            print ('  Name       : {}'.format(user['name']))
            print ('  User Type   : {}'.format(user['userType']))            

        # Test Voice: Say Thank You
        #conn.test_voice()
        # re-enable device after all commands already executed
        #conn.enable_device()
    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        print ('TERMINOU de Adicionar....')
        #if conn:
        #    conn.disconnect()

def valid_ip(address):
    try:
        host_bytes = address.split('.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b<=255]
        return len(host_bytes) == 4 and len(valid) == 4
    except:
        return False
    
file_csv = False
IPvalid = False

deviceIP = 0
ficheiro_csv = ''

if __name__ == "__main__":
    print(f"Conta Argumentos: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argumento {i:>6}: {arg}")
        if '.csv' in arg and i == 1:
            print ('Ficheiro CSV encontrado')
            file_csv = True
            ficheiro_csv = arg
        if i == 2:
            #Check if Valid IP
            IPvalid = valid_ip(arg)
            if IPvalid: deviceIP = arg
            print (IPvalid)
    if IPvalid and file_csv:
        actualizar_hikvision(deviceIP,ler_ficheiro(ficheiro_csv))
    else:
        print ('Leitura do ficheiro CSV somente...')
        ler_ficheiro(ficheiro_csv)
        
