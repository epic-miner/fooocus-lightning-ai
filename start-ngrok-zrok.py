import argparse
import json
from pyngrok import ngrok, conf
import os
import pip
import psutil
from requests import get
import signal
import socket
import sys
import subprocess
from multiprocessing import Process
import time

def get_saved_data():
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)
    
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0
    
def find_and_terminate_process(port):
    for process in psutil.process_iter(['pid', 'name', 'connections']):
        for conn in process.info.get('connections', []):
            if conn.laddr.port == port:
                print(f"Port {port} is in use by process {process.info['name']} (PID {process.info['pid']})")
                try:
                    process.terminate()
                    print(f"Terminated process with PID {process.info['pid']}")
                except psutil.NoSuchProcess:
                    print(f"Process with PID {process.info['pid']} not found")
        
def run_app(env):
    #-+subprocess.run("pwd", shell=False, env=env)
    cmd = 'python Fooocus/entry_with_update.py --always-high-vram > log.txt & ssh -o StrictHostKeyChecking=no -p 80 -R0:localhost:7865 a.pinggy.io > log.txt'
    subprocess.run(cmd, shell=True, env=env)

def print_url():
    print("waiting for output")
    time.sleep(2)
    sys.stdout.flush()
    
    found = False
    with open('log.txt', 'r') as file:
        end_word = '.pinggy.link'
        for line in file:
            #print(line)
            start_index = line.find("http:")
            if start_index != -1:
                end_index = line.find(end_word, start_index)
                if end_index != -1:
                    print("😁 😁 😁")
                    print("URL: " + line[start_index:end_index + len(end_word)])
                    print("😁 😁 😁")
                    found = True
    if not found:
        print_url()
    else:
        with open('log.txt', 'r') as file:
            for line in file:
                print(line)
                
def get_zrok_token(args, saved_data):
    if args.token_zrok is None:
            if saved_data and saved_data['token_zrok']:
                args.token_zrok = saved_data['token_zrok']
            else:
                # If there is no session token, run the create account step
                args.token_zrok = input('Enter the Zrok session token: ')
                if args.token_zrok == '':
                    args.token_zrok = input('Enter the Zrok session token: ')
                saved_data['token_zrok'] = args.token_zrok
                save_data(saved_data)

def main():
    target_port = 7865
    
    env = os.environ.copy()
    
    if is_port_in_use(target_port):
        find_and_terminate_process(target_port)
    else:
        print(f"Port {target_port} is free.")
    
    parser = argparse.ArgumentParser(description='Console app with token and domain arguments')
    parser.add_argument('--token', help='Specify the ngrok token')
    parser.add_argument('--domain', help='Specify the ngrok domain')
    parser.add_argument('--tunnel', help='Select the tunnel [1, 2, 3]')
    parser.add_argument('--token_zrok', help='Specify the Zrok token')
    parser.add_argument('--reset', action='store_true', help='Reset saved data')

    args = parser.parse_args()

    saved_data = get_saved_data()

    if args.reset:
        if saved_data is not None:
            saved_data = { 'token': '', 'domain': '', 'tunnel': '', 'token_zrok':'', 'zrok_activated':''}
    else:
        if saved_data is not None:
            if args.token:
                saved_data['token'] = args.token
            if args.domain:
                saved_data['domain'] = args.domain
            if args.tunnel:
                saved_data['tunnel'] = args.tunnel 
            try: 
                print("Tunnel in the json file is: " + saved_data['tunnel'])
            except:
                saved_data['tunnel'] = ''
            try: 
                print("Ngrok token in the json file is: " + saved_data['token'])
            except:
                saved_data['token'] = ''
            try: 
                print("Ngrok domain in the json file is: " + saved_data['domain'])
            except:
                saved_data['domain'] = ''
            try: 
                print("Zrok token in the json file is: " + saved_data['token_zrok'])
            except:
                saved_data['token_zrok'] = ''
            try: 
                print("Zrok activated in the json file is: " + saved_data['zrok_activated'])
            except:
                saved_data['zrok_activated'] = ''            
        else:
            saved_data = { 'token': '', 'domain': '', 'tunnel': '', 'token_zrok':'', 'zrok_activated':''}
                
    if args.tunnel is None:
        if saved_data and saved_data['tunnel']: 
            args.tunnel = saved_data['tunnel']
        else: 
            args.tunnel = input('Enter a tunnel: pinggy [1], zrok [2], ngrok [3] (1/2/3): ')
            if args.tunnel == '':
                args.tunnel = 1
            saved_data['tunnel'] = args.tunnel
            
    save_data(saved_data)
    
    cmd = 'python Fooocus/entry_with_update.py --always-high-vram'
    
    print("Tunnel: " + args.tunnel)
    if args.tunnel == '3':
        if args.token is None:
            if saved_data and saved_data['token']:
                args.token = saved_data['token']
            else:
                args.token = input('Enter the token: ')
                if args.token == '':
                    args.token = input('Enter the token: ')
                saved_data['token'] = args.token

        if args.domain is None:
            args.domain = ''
            if saved_data and saved_data['domain']:
                args.domain = saved_data['domain']
            else:
                args.domain = input('Enter the domain: ')
                saved_data['domain'] = args.domain
        save_data(saved_data)                        
        print(f'Token: {args.token}')
        print(f'Domain: {args.domain}')
        print('Using ngrok')
        print('token: ' + args.token)
        if args.token != '':
            ngrok.kill()
            srv = ngrok.connect(target_port, pyngrok_config=conf.PyngrokConfig(auth_token=args.token),
                    bind_tls=True, domain=args.domain).public_url
            print(srv)
            signal.signal(signal.SIGINT, signal_handler)
            print('Press Ctrl+C to exit')   
            subprocess.run(cmd, shell=True, env=env)
            signal.pause()
        else:
            print('An ngrok token is required. You can get one on https://ngrok.com')
            
    elif args.tunnel == '2':
        print('Using Zrok')
        # Check zrok is installed
        if not os.path.exists('/home/studio-lab-user/zrok/zrok'):
            cmd_zrok = 'mkdir /home/studio-lab-user/zrok'
            subprocess.run(cmd_zrok, shell=True, env=env)
            cmd_zrok = 'wget https://github.com/openziti/zrok/releases/download/v0.4.23/zrok_0.4.23_linux_amd64.tar.gz -O /home/studio-lab-user/zrok/zrok.tar.gz'
            subprocess.run(cmd_zrok, shell=True, env=env)
            cmd_zrok = 'tar -xvf /home/studio-lab-user/zrok/zrok.tar.gz -C /home/studio-lab-user/zrok'
            subprocess.run(cmd_zrok, shell=True, env=env)
            cmd_zrok = 'chmod a+x /home/studio-lab-user/zrok/zrok'
            subprocess.run(cmd_zrok, shell=True, env=env)
        # Add zrok to the environment variable
        if not 'zrok' in os.environ['PATH']:
            os.environ['PATH'] += ":/home/studio-lab-user/zrok"
        # Activate the environment using the zrok token
        if not saved_data['zrok_activated'] == '1':    
            print("Would you like to create a Zrok account?")
            create_zrok = input("Y/n: ")
            if not (create_zrok.upper() == 'N'):
                cmd_zrok = '/home/studio-lab-user/zrok/zrok invite'
                subprocess.run(cmd_zrok, shell=True, env=env)
            print('Would you like to enable the environment for Zrok?')
            create_zrok = input("Y/n: ")
            if not (create_zrok.upper() == 'N'):
                cmd_zrok = f"/home/studio-lab-user/zrok/zrok disable > /dev/null"
                subprocess.run(cmd_zrok, shell=True, env=env)
                get_zrok_token(args, saved_data)
                cmd_zrok = f"/home/studio-lab-user/zrok/zrok enable {args.token_zrok}"
                subprocess.run(cmd_zrok, shell=True, env=env)
            saved_data['zrok_activated'] = '1'
            save_data(saved_data)
            
        # Start the WebUI with Zrok
        cmd_zrok = f"{cmd} & /home/studio-lab-user/zrok/zrok share public http://localhost:{target_port} --headless"
        subprocess.run(cmd_zrok, shell=True, env=env)
        
    else:
        # Check openssh is installed
        try:
            subprocess.check_output(['ssh', '-V'])
        except:
            cmd = 'conda activate fooocus'
            subprocess.run(cmd, shell=True, env=env)
            cmd = 'conda config --add channels conda-forge'
            subprocess.run(cmd, shell=True, env=env)
            cmd = 'conda config --set channel_priority strict'
            subprocess.run(cmd, shell=True, env=env)
            cmd = 'conda install openssh -y'
            subprocess.run(cmd, shell=True, env=env)
        
        print('Using Pinggy')
        cmd = 'touch log.txt'
        subprocess.run(cmd, shell=True, env=env)
        open('log.txt', 'w').close()
        p_app = Process(target=run_app, args=(env,))
        p_url = Process(target=print_url)
        p_app.start()
        p_url.start()
        p_app.join()
        p_url.join()

    
if __name__ == '__main__':
    main()
