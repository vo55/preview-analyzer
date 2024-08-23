"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import json
import datetime
from rxconfig import config
import os

def store_info(ip, user_agent, page):
    try:
        with open('/tmp/reflexlog.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        # If the file doesn't exist, initialize an empty data structure
        data = {'ip_user_agents': []}
    data['ip_user_agents'].append({'page': page, 'ip': ip, 'user_agent': user_agent, 'time': str(datetime.datetime.now())})
    with open('/tmp/reflexlog.json', 'w') as f:
        json.dump(data, f, indent=4)


class State(rx.State):
    """The app state."""
    columns = ["Route", "User-Agent", "IP", "Time"]
    data = []
    token_hint = True


    def log_access(self):
        ip_adress = self.router.session.client_ip
        route = self.router.page.path
        user_agent = self.router.headers.user_agent
        store_info(ip_adress, user_agent, route)

    def load_dashboard(self):
        if self.router.page.params['token'] == os.environ.get('DASHBOARD_TOKEN'):
            response = []
            self.data = []
            with open('/tmp/nginx.json', 'r') as f:
                for json_line in f.readlines():
                    line = json.loads(json_line)
                    response.append(line)
            for entry in response:
                self.data.append(
                    [
                        entry['request'],
                        entry['http_user_agent'],
                        entry['remote_addr'],
                        entry['time_local']
                    ]
                )


def dashboard() -> rx.Component:
    return rx.vstack(
        rx.data_table(
            data=State.data,
            columns=State.columns,
            pagination=True,
            search=True,
            sort=True,
        ),
    )

app = rx.App()
app.add_page(dashboard, route="/dashboard", on_load=State.load_dashboard)