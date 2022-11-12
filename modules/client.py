#made by @pyp on github // otherwise known as doozle

import httpx, toml
from datetime import datetime
from time import time

class Client():
    timestamp = lambda: str(datetime.fromtimestamp(time())).split(' ')[1]

    def get_session(self):
        session = httpx.Client()
        return session

    def send_webhook(self, timestamp: str, vanity: str):
        ses = Client.get_session(self)
        try: 
            with open('assets/config.toml') as f: self.config = toml.loads(f.read())
            webhook = self.config['webhook']['webhook_link']
            title = self.config['webhook']['title']
            message = self.config['webhook']['message']
            if '[vanity]' in message: message = message.replace('[vanity]', f'{vanity}')
            if '[time]' in message:  message = message.replace('[time]', f'{timestamp}')
            data = {
            'embeds': [{
                    'title': f'{title}',
                    'description': f'{message}', 
                    'color': 4802889,
                }]
            }
            r = ses.post(webhook, json=data)
            if r.status_code in (200, 204):
                print('\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Succesfully sent \x1b[38;2;73;73;73mwebhook\x1b[0m.' % (Client.timestamp()))
            else:
                print('\x1b[38;2;73;73;73m[\x1b[0m%s\x1b[38;2;73;73;73m]\x1b[0m Failed to send \x1b[38;2;73;73;73mwebhook\x1b[0m.' % (Client.timestamp()))
            return 'success'
        except Exception:
            return 'failed'
