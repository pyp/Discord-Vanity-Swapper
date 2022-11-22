#made by @pyp on github // otherwise known as doozle

from threading import Thread
import os, toml, httpx, sys

from concurrent.futures import ThreadPoolExecutor
from modules import Client
from urllib.parse import urlencode
from modules import Client

class sniper:
    def __init__(self):
        self.sniped = True
        
        with open('assets/config.toml') as f: self.config = toml.loads(f.read())
        self.token = self.config['sniper']['discord_token']
        self.session = httpx.Client()
        
        try: 
            self.current_guild = sys.argv[1]
            self.target_guild = sys.argv[2]
            self.vanity = sys.argv[3]
            self.run()
        except Exception:   
            print('\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Incorrect Usage\x1b[38;2;73;73;73m\x1b[0m! python3 main.py \x1b[38;2;73;73;73m[\x1b[0mcurrent_guild\x1b[38;2;73;73;73m] \x1b[38;2;73;73;73m[\x1b[0mtarget_guild\x1b[38;2;73;73;73m]\x1b[0m \x1b[38;2;73;73;73m[\x1b[0mvanity\x1b[38;2;73;73;73m]\x1b[0m' % (Client.timestamp()))
            sys.exit()
        
    def change(self, guild):
        r = self.session.patch('https://ptb.discord.com/api/v9/guilds/%s/vanity-url' % guild, headers={'accept': '*/*', 'authorization': self.token}, json={'code': os.urandom(5).hex()})
        if r.status_code == 200:
            self.changed = Client.timestamp()
            print('\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Succesfully changed vanity on \x1b[38;2;73;73;73m%s\x1b[0m.' % (Client.timestamp(), self.current_guild))
        elif r.status_code == 429:
            times = r.text.split('after": ')[1].split('\n}\n')[0]
            print('\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Ratelimited | %s' % (Client.timestamp(), times))
            sys.exit() 
        else:
            print('\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Failed to change \x1b[38;2;73;73;73m%s\x1b[0m.' % (Client.timestamp(), self.vanity))
            sys.exit()
         
    def swap(self, guild):
        r = self.session.patch('https://ptb.discord.com/api/v9/guilds/%s/vanity-url' % guild, headers={'accept': '*/*', 'authorization': self.token}, json={'code': self.vanity})
        if r.status_code == 200:
            self.claimed = Client.timestamp()
            print('\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Succesfully swapped vanity on \x1b[38;2;73;73;73m%s\x1b[0m.' % (Client.timestamp(), self.target_guild))
            Client.send_webhook(self, timestamp=float(self.claimed[-7:])-float(self.changed[-7:]), vanity=self.vanity)
            sys.exit()
        elif r.status_code == 429:
            times = r.text.split('after": ')[1].split('\n}\n')[0]
            print('\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Ratelimited | %s' % (Client.timestamp(), times))
            sys.exit() 
        else:
            print('\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Failed to swap \x1b[38;2;73;73;73m%s\x1b[0m.' % (Client.timestamp(), self.vanity))
            sys.exit()
            
    def run(self):
        Thread(target=self.change(self.current_guild)).start()
        Thread(target=self.swap(self.target_guild)).start()
        
os.system('cls || clear')
sniper()
