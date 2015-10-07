# What is this?

PyDashery is just another dashboard. Backend runs Python (hence the name), and
frontend is a web page using JavaScript and WebSockets to stay updated.

The goal was to keep the structure simple, yet easily extensible. If it works
as planned adding a new widget requires only adding the relevant code and
template on the backend, updating settings, and then it should already be
visible on your screen.


# How to use it?

Well, the documentation is still a bit shit, but the basic idea is fairly
simple.

1. Clone this repo, download a .ZIP, or in some manner get the contents to a
computer you want to run the PyDashery backend on.

1. Edit `backend/settings.py`, the `WIDGETS` is likely the thing you want to
configure. Each entry defines the widget to be loaded, the `type` has to match
the `TYPE` attribute of the `Widget` class, the rest are passed to widgets as
settings.

1. Set up pre-requisites for the backend, in the `backend/` -directory
execute: `pip install -r requirements.txt`

1. Run the backend, in the `backend/` -directory execute: `python -m pydashery`

1. Point your favorite (modern) browser to the PyDashery server, e.g. if
running locally with default settings: `http://localhost:8080/`

1. Create your own widgets, check out examples in the `backend/widgets/` and
`backend/templates/` -directories.


# Setting it on on a Raspberry Pi with Raspbian

Configure your Raspberry Pi with the default user, and autostart to graphics
mode.

## Check out PyDashery

```
git clone https://github.com/lietu/pydashery.git
```

## Install requirements etc. tools to help setting up the service

```
sudo apt-get update
sudo apt-get install build-essential python-dev python-virtualen virtualenvwrapper supervisor
```

## Disable screen saving, auto start chromium on boot

```
echo '@xset s noblank
@xset s off
@xset -dpms
/usr/bin/chromium --kiosk --disable-restore-session-state "http://127.0.0.1:8080"
' > /home/pi/.config/openbox/autostart
```

## Set up service to run PyDashery

```
sudo ln -s /home/pi/pydashery/salt/roots/salt/pydashery/supervisor-pydashery.conf /etc/supervisor/conf.d/
```

## Reboot the device

```
sudo reboot
```

# Ok, so what's the license like?

Short answer: MIT and new BSD.

Long answer: Read the LICENSE.md -file.

