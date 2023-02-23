#Created by Helkds
#Last Modified 23-02-2023
'''
    Reads Employee CSV file exported from ERPNext / MetaGest.
    Check if Employee Active and if ATTENDANCE ID assigned
    Adds Employess to ZKTECO.
'''
import sys
from zk import ZK, const

import csv

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
            if idx >0:
                if lines[4] != 'Left':
                    #0 Number,1 NAME, 2 Full Name, 3 Attendance ID, 4 Status
                    print ('Verifica se tem o Numero do Attendance ID...')
                    if lines[3]:
                        print ('Adicionar ao Biometrico.... ', lines[1])
                        func_adicionar_bio['nome'].append(lines[2])
                        func_adicionar_bio['attid'].append(lines[3])
                    else:
                        print ('Este Funcinonario {} nao tem ID do BIOMETRICO... '.format(lines[2]))
                        func_not_added.append(lines[2])

        if func_not_added:
            print ('lista de Funcionarios nao adicionados...')
            print (*func_not_added,sep='\n')
        print (len(func_adicionar_bio))
        print (len(func_adicionar_bio['nome']))
    return func_adicionar_bio

def actualizar_zk(deviceIP,func_adicionar_bio):
    conn = None
    # create ZK instance
    zk = ZK(deviceIP, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
    try:
        # connect to device
        conn = zk.connect()
        # disable device, this method ensures no activity on the device while the process is run
        conn.disable_device()
        # Create users
        if func_adicionar_bio:
            cc = 0
            while cc < len(func_adicionar_bio['nome']):
                conn.set_user(uid=int(func_adicionar_bio['attid'][cc]), name=str(func_adicionar_bio['nome'][cc]), privilege='User', password='12345678', group_id='', user_id=func_adicionar_bio['attid'][cc], card=0)
                cc += 1

        users = conn.get_users()
        for user in users:
            privilege = 'User'
            if user.privilege == const.USER_ADMIN:
                privilege = 'Admin'
            print ('+ UID #{}'.format(user.uid))
            print ('  Name       : {}'.format(user.name))
            print ('  Privilege  : {}'.format(privilege))
            print ('  Password   : {}'.format(user.password))
            print ('  Group ID   : {}'.format(user.group_id))
            print ('  User  ID   : {}'.format(user.user_id))

        # Test Voice: Say Thank You
        conn.test_voice()
        # re-enable device after all commands already executed
        conn.enable_device()
    except Exception as e:
        print ("Process terminate : {}".format(e))
    finally:
        if conn:
            conn.disconnect()

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
        actualizar_zk(deviceIP,ler_ficheiro(ficheiro_csv))
        
