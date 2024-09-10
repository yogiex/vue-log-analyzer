import subprocess                                                                                                                                                    
import mysql.connector                                                                                                                                               
                                                                                                                                                                     
db_config = {                                                                                                                                                        
    'host': '180.250.135.11',                                                                                                                                        
    'user': 'vm-b',                                                                                                                                                  
    'password': 'admin@123',                                                                                                                                         
    'database': 'moodle',                                                                                                                                            
}                                                                                                                                                                    
                                                                                                                                                                     
class peserta:                                                                                                                                                       
    def __init__(self, state, sid, timecreated, timemodified, first_IP, last_IP, unix_timecreated):                                                                  
        self.state = state                                                                                                                                           
        self.sid = sid                                                                                                                                               
        self.timecreated = timecreated                                                                                                                               
        self.timemodified = timemodified                                                                                                                             
        self.first_IP = first_IP                                                                                                                                     
        self.last_IP = last_IP                                                                                                                                       
        self.unix_timecreated = unix_timecreated                                                                                                                     
                                                                                                                                                                     
data = {}                                                                                                                                                            
                                                                                                                                                                     
def load_data():                                                                                                                                                     
    global data                                                                                                                                                      
                                                                                                                                                                     
    conn = mysql.connector.connect(**db_config)                                                                                                                      
                                                                                                                                                                     
    # Create a cursor object to interact with the database                                                                                                           
    cursor = conn.cursor()                                                                                                                                           
                                                                                                                                                                     
    # Example query                                                                                                                                                  
    cursor.execute(                                                                                                                                                  
        """                                                                                                                                                          
        select *, DATE_FORMAT(FROM_UNIXTIME(timecreated), '%d/%b/%Y:%H:%i:%s')                                                                                       
        from mdl_sessions ms
        """)
    rows = cursor.fetchall()

    for row in rows:                                                                                                                                                 
        if data:                                                                                                                                                     
            if row[2] in data:                                                                                                                                       
                if data[row[2]].state != row[1]:                                                                                                                     
                    data[row[2]].state = row[1]                                                                                                                      
                if data[row[2]].sid != row[2]:                                                                                                                       
                    data[row[2]].sid = row[2]                                                                                                                        
                if data[row[2]].timecreated != row[5]:                                                                                                               
                    data[row[2]].timecreated = row[5]                                                                                                                
                if data[row[2]].timemodified != row[6]:                                                                                                              
                    data[row[2]].timemodified = row[6]                                                                                                               
                if data[row[2]].first_IP != row[7]:                                                                                                                  
                    data[row[2]].first_IP = row[7]                                                                                                                   
                if data[row[2]].last_IP != row[8]:                                                                                                                   
                    data[row[2]].last_IP = row[8]                                                                                                                    
                if data[row[2]].unix_timecreated != row[9]:                                                                                                          
                    data[row[2]].unix_timecreated = row[9]                                                                                                           
            else:                                                                                                                                                    
                data[row[2]] = peserta(row[1], row[2], row[5], row[6], row[7], row[8], row[9])                                                                       
        else:                                                                                                                                                        
            data[row[2]] = peserta(row[1], row[2], row[5], row[6], row[7], row[8], row[9])                                                                           
                                                                                                                                                                     
    return data                                                                                                                                                      
                                                                                                                                                                     
def main_menu():                                                                                                                                                     
    i = 1                                                                                                                                                            
    sid_data = []                                                                                                                                                    
    if len(data) == 0:                                                                                                                                               
        load_data()                                                                                                                                                  
                                                                                                                                                                     
    print("Pick user by num in list:")                                                                                                                               
    for sid, peserta in data.items():                                                                                                                                
        sid_data.append(sid)
        print("sid " + str(i) + " : " + str(peserta.sid) + " ," + str(peserta.last_IP) + " ," + str(peserta.unix_timecreated))                                       
        i += 1                                                                                                                                                       
                                                                                                                                                                     
    user_input = int(input("pick user num: "))                                                                                                                       
                                                                                                                                                                     
    ip,unix_time = data[sid_data[user_input - 1]].last_IP, data[sid_data[user_input - 1]].unix_timecreated                                                           
                                                                                                                                                                     
    command =  f"cd .. && sudo cat /var/log/rsync-apache2/access.log | grep -E {ip}.*{unix_time}"                                                                    
                                                                                                                                                                     
    try:                                                                                                                                                             
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)                                                     
        print(result.stdout.decode('utf-8'))                                                                                                                        
        print("\n\n")                                                                                                                                                
    except subprocess.CalledProcessError as e:                                                                                                                       
        print("Error :", e.stderr.decode("utf-8"))                                                                                                                   
                                                                                                                                                                     
                                                                                                                                                                     
while True:
    main_menu()