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
            self.data = []
            with open('/tmp/reflexlog.json', 'r') as f:
                response = json.load(f)
            for entry in response["ip_user_agents"]:
                self.data.append(
                    [
                        entry['page'],
                        entry['user_agent'],
                        entry['ip'],
                        entry['time']
                    ]
                )

    def same_site_redirect(self):
        # Welcome Page (Index)
        return rx.redirect('/')

    def external_site_redirect(self):
        # Welcome Page (Index)
        return rx.redirect('https://example.com')

    def ssrf_redirect_magic(self):
        return rx.redirect('http://169.254.169.254')

    def ssrf_redirect_local(self):
        return rx.redirect('http://127.0.0.1')

    def redirect_loop(self):
        return rx.redirect('/redirect-loop')


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Preview Analyzer", size="9"),
            rx.text(
                "Lorem Ipsum ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
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
app.add_page(index, on_load=State.log_access)
app.add_page(index, route="/same-site-redirect", on_load=[State.log_access, State.same_site_redirect])
app.add_page(index, route="external-redirect", on_load=[State.log_access, State.external_site_redirect])
app.add_page(index, route="/redirect-loop", on_load=[State.log_access, State.redirect_loop])
app.add_page(index, route="/ssrf-redirect-magic", on_load=[State.log_access, State.ssrf_redirect_magic])
app.add_page(index, route="/ssrf-redirect-local", on_load=[State.log_access, State.ssrf_redirect_magic])
app.add_page(dashboard, route="/dashboard", on_load=State.load_dashboard)