# Preview Analyzer

Ever wondered how a social media site or messenger is pulling the previews of your site? No? ok. nevermind.
I did though and I wanted to research:

- Origin (User Device or the Servers) for privacy reasons
- How are redirects handled (resolved or not)
- Are there SSRF possibilities

In order to comfortably analyze multiple pages I created a little service that would log the access and return it for me.

### Starting the server
`python3 -m venv venv`

`source venv/bin/active`

`pip install reflex`

`export DASHBOARD_TOKEN=<my-token>; export FRONTEND_PORT=80 && reflex run --env prod`

### Routes
- `/` - a simple page that a client can directly access
- `/same-site-redirect` - redirects to `/`
- `/external-redirect` - redirect to `https://example.com`
- `/ssrf-redirect-magic` - redirect to `http://169.254.169.254`
- `/ssrf-redirect-local` - redirect to `http://127.0.0.1`
- `/redirect-loop` - redirects to `/redirect-loop`

### Dashboard
The access log can be accessed under `/dashboard?token=<my-token>` and you will need to enter the password you set when starting the server.

The dashboard is a simple, searchable and sortable page.
![Alt text](dashboard.png?raw=true)

### Disclaimer
This server will log the IP of clients (server or users) and is intended for research purposes with ones own devices. Please use with privacy in mind.