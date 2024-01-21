import os
import paramiko
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from io import StringIO
import shutil
from stat import S_ISDIR
import json
import sys
from pathlib import Path
import zipfile
#from tkinter.messagebox import showinfo

session = ""
name = ""
prop = ""
appl = ""
lab = ""
tech = "" 
zipPath = ""
host = ""
apparatus = ""
ssh = None
lb1 = None
lb2 = None

CURRENT_DIR = os.path.dirname(__file__) #os.getcwd()

source_path = ""
output_path = ""

def get_correct_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parents[4]#sys.executable
    else:
        base_path = os.path.abspath(CURRENT_DIR)

    return os.path.join(base_path, relative_path)

with open(get_correct_path('config/remote_paths.json'), "r") as json_file:
    data = json.load(json_file)
    source_path = data["source_path"]
    output_path = data["output_path"]

# Dropdown menu options 
hostOptions = []

with open(get_correct_path("config/hosts_list.txt"), "r") as host_file:
    hostOptions = [line.replace("\n","") for line in host_file.readlines()]

# Dropdown menu options 
apparatusOptions = []

with open(get_correct_path("config/apparatuses_list.txt"), "r") as app_file:
    apparatusOptions =  [line.replace("\n","") for line in app_file.readlines()]

def createXMLFile():
    global session
    global name
    global prop
    global appl
    global lab
    global tech
    global host
    global apparatus
    xmlText = f"<Scan><ScanID>{session}</ScanID><Name>{name}</Name><ProprietaryName>{prop}</ProprietaryName><Applicant>{appl}</Applicant><Laboratory>{lab}</Laboratory><Technician>{tech}</Technician><SelectedSpecies>{host}</SelectedSpecies><StartDateTime>1976-05-30T12:07:41.643Z</StartDateTime><SelectedMethod>{apparatus}</SelectedMethod><ScanStatus>finished</ScanStatus><CreatedAt>2023-06-06T14:49:14.9895718Z</CreatedAt></Scan>"

    if not os.path.exists(os.path.join(get_correct_path("sessions"),session)):
        os.mkdir(os.path.join(get_correct_path("sessions"),session))
    with open(os.path.join(get_correct_path("sessions"),session,f'{session}.xml'), 'w') as f:
        f.write(xmlText)

def collectDataInFolder():
    global session
    global zipPath
    if not os.path.exists(os.path.join(get_correct_path("sessions"),session)):
        os.mkdir(os.path.join(get_correct_path("sessions"),session))
    #os.rename(f"sessions/{session}/{session}.xml", os.path.join("sessions",session,f"{session}.xml"))
    shutil.copy(zipPath, os.path.join(get_correct_path("sessions"),session,f"{session}.zip"))
    #os.rename(zipPath, os.path.join("sessions",session,f"{session}.zip"))
    
    with zipfile.ZipFile(os.path.join(get_correct_path("sessions"),session,f"{session}.zip"), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(get_correct_path("sessions"),session,"images"))

def samples_scanner():
    global ssh, lb1, lb2, lb3
    root = tk.Tk()
    user = "azureuser"
    #keyCertPath = "AI-KFM_key.pem"
    server = "40.114.205.185"
    #k = paramiko.RSAKey.from_private_key_file(keyCertPath)
    k_s = StringIO("-----BEGIN RSA PRIVATE KEY-----\n\
    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\n\
    -----END RSA PRIVATE KEY-----")
    k = paramiko.RSAKey.from_private_key(k_s)

    #localpath = "svm.png"
    #remotepath = "/datadrive/home/Antonio/scan_data/svm.png"

    ssh = paramiko.SSHClient()
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(server, username=user, pkey = k )

    root.title("Samples Scanner")

    def sendFolder():
        global ssh
        sftp = ssh.open_sftp()
        stdin, stdout, stderr = ssh.exec_command(f'mkdir {source_path}/{session}')
        sftp.put(os.path.join(get_correct_path("sessions"),session,f"{session}.zip"), f"{source_path}/{session}/{session}.zip")
        sftp.put(os.path.join(get_correct_path("sessions"),session,f"{session}.xml"), f"{source_path}/{session}/{session}.xml")
        sftp.close()

    def select_file():
        global zipPath
        filetypes = (
            ('Zip files', '*.zip'),#,
            #('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Load a .zip file',
            initialdir='.',
            filetypes=filetypes)
        zipPath = filename
        #zipPath.set(filename)
        l8.config(text=f"Zip File Path: {filename}")
        
        #showinfo(
        #    title='Selected File',
        #    message=filename
        #)

    def take_inputs():
        global session
        global name
        global prop
        global appl
        global lab
        global tech
        global host
        global apparatus
        global zipPath
        global ssh
        global lb1
        session = t0.get("1.0", "end-1c")
        print(session)
        name = t1.get("1.0", "end-1c")
        print(name)
        prop = t2.get("1.0", "end-1c")
        print(prop)
        appl = t3.get("1.0", "end-1c")
        print(appl)
        lab = t4.get("1.0", "end-1c")
        print(lab)
        tech = t5.get("1.0", "end-1c")
        print(tech)
        host = selectedHost.get()
        apparatus = selectedApparatus.get()
        print(host)
        print(apparatus)
        print(zipPath)
        lb1.config(text="Loading...")
        try:
            createXMLFile()
            collectDataInFolder()
            sendFolder()
            lb1.config(text="Folder sent successfully")
            print("Folder sent successfully")
        except Exception as e:
            lb1.config(text=e)
            print(e)

    def sftp_walk(sftp,remotepath):
        path=remotepath
        files=[]
        folders=[]
        for f in sftp.listdir_attr(remotepath):
            if S_ISDIR(f.st_mode):
                folders.append(f.filename)
            else:
                files.append(f.filename)
        if files:
            yield path, files
        for folder in folders:
            new_path=os.path.join(remotepath,folder)
            for x in sftp_walk(new_path):
                yield x

    def retrieve_report():
        global session
        global ssh
        global lb3
        session = t0.get("1.0", "end-1c")
        print(session)
        try:
            lb3.config(text="Loading...")
            sftp = ssh.open_sftp()
            sftp.get(f"{output_path}/{session}/{session}_report.pdf", os.path.join(get_correct_path("sessions"),session,f"{session}_report.pdf"))
            sftp.get(f"{output_path}/{session}/{session}_inference.json", os.path.join(get_correct_path("sessions"),session,f"{session}_inference.json"))
            if not os.path.exists(os.path.join(get_correct_path("sessions"),session,"labels")):
                os.mkdir(os.path.join(get_correct_path("sessions"),session,"labels"))
            for path, files in sftp_walk(sftp,f"{output_path}/{session}/{session}_DetectionOutput/labels"):
                for file in files:
                    sftp.get(os.path.join(path,file), os.path.join(get_correct_path("sessions"),session,"labels",file))
            lb3.config(text="Report downloaded successfully")
        except Exception as e:
            lb3.config(text=e)
            print(e)

    def generate_report():
        global session
        global ssh
        global lb2
        session = t0.get("1.0", "end-1c")
        print(session)
        try:
            lb2.config(text="Loading...")
            stdin, stdout, stderr = ssh.exec_command(f'./runFlow_PYTHON.sh {session}')
            exit_status = stdout.channel.recv_exit_status()
            if exit_status == 0:
                print ("RunFlow Script Launched and Completed")
            else:
                print("Error", exit_status)
            sftp = ssh.open_sftp()
            sftp.get(f"{output_path}/{session}/{session}_report.pdf", os.path.join(get_correct_path("sessions"),session,f"{session}_report.pdf"))
            sftp.get(f"{output_path}/{session}/{session}_inference.json", os.path.join(get_correct_path("sessions"),session,f"{session}_inference.json"))
            if not os.path.exists(os.path.join(get_correct_path("sessions"),session,"labels")):
                os.mkdir(os.path.join(get_correct_path("sessions"),session,"labels"))
            for path, files in sftp_walk(sftp,f"{output_path}/{session}/{session}_DetectionOutput/labels"):
                for file in files:
                    sftp.get(os.path.join(path,file), os.path.join(get_correct_path("sessions"),session,"labels",file))
            lb2.config(text="Report downloaded successfully")
        except Exception as e:
            lb2.config(text=e)
            print(e)

    # specify size of window.
    root.geometry("800x800")

    # datatype of menu text 
    selectedHost = tk.StringVar(root) 

    # datatype of menu text 
    selectedApparatus = tk.StringVar(root) 

    # initial menu text 
    selectedHost.set( hostOptions[0] ) 

    # initial menu text 
    selectedApparatus.set( apparatusOptions[0] ) 

    # Create label
    l0 = tk.Label(root, text = "Scan Session Name")
    l0.config(font =("Courier", 14))

    # Create text widget and specify size.
    t0 = tk.Text(root, height = 4, width = 52)
    
    # Create label
    l1 = tk.Label(root, text = "Name")
    l1.config(font =("Courier", 14))

    # Create text widget and specify size.
    t1 = tk.Text(root, height = 4, width = 52)

    # Create label
    l2 = tk.Label(root, text = "Proprietary")
    l2.config(font =("Courier", 14))

    # Create text widget and specify size.
    t2 = tk.Text(root, height = 4, width = 52)

    # Create label
    l3 = tk.Label(root, text = "Applicant")
    l3.config(font =("Courier", 14))

    # Create text widget and specify size.
    t3 = tk.Text(root, height = 4, width = 52)

    # Create label
    l4 = tk.Label(root, text = "Laboratory")
    l4.config(font =("Courier", 14))

    # Create text widget and specify size.
    t4 = tk.Text(root, height = 4, width = 52)

    # Create label
    l5 = tk.Label(root, text = "Technician")
    l5.config(font =("Courier", 14))

    # Create text widget and specify size.
    t5 = tk.Text(root, height = 4, width = 52)

    # Create label
    l6 = tk.Label(root, text = "Host")

    # Create Dropdown menu 
    drop1 = tk.OptionMenu( root , selectedHost , *hostOptions ) 

    # Create label
    l7 = tk.Label(root, text = "Apparatus")

    # Create Dropdown menu 
    drop2 = tk.OptionMenu( root , selectedApparatus , *apparatusOptions ) 

    # Create label
    l8 = tk.Label(root, text = "Zip File Path: ")

    open_button = ttk.Button(
        root,
        text='Load Scan Zip File',
        command=select_file
    )
    
    # Create button for next text.
    b1 = tk.Button(root, text = "Send", command = lambda: take_inputs())
    lb1 = tk.Label(root, text = "")

    # Create button for next text.
    b2 = tk.Button(root, text = "Generate", command = lambda: generate_report())
    lb2 = tk.Label(root, text = "") 

     # Create button for next text.
    b3 = tk.Button(root, text = "Retrieve only", command = lambda: retrieve_report())
    lb3 = tk.Label(root, text = "") 

    # Create an Exit button.
    #b3 = tk.Button(root, text = "Exit",
    #            command = root.destroy) 
    
    l0.pack()
    t0.pack()
    l1.pack()
    t1.pack()
    l2.pack()
    t2.pack()
    l3.pack()
    t3.pack()
    l4.pack()
    t4.pack()
    l5.pack()
    t5.pack()
    l6.pack()
    drop1.pack() 
    l7.pack()
    drop2.pack() 
    l8.pack()
    open_button.pack()
    b1.pack()
    lb1.pack()
    b2.pack()
    lb2.pack()
    b3.pack()
    lb3.pack()
    #b3.pack()
    
    # Insert The Fact.
    #T1.insert(tk.END, Fact)
    
    tk.mainloop()

    ssh.close()

#samples_scanner()