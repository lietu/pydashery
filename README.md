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

1. Run the backend, in the `backend/` -directory execute: `python -m pydashery`

1. Point your favorite (modern) browser to the PyDashery server, e.g. if
running locally with default settings: `http://localhost:8080/`

1. Create your own widgets, check out examples in the `backend/widgets/` and
`backend/templates/` -directories.


# Ok, so what's the license like?

Short answer: MIT and new BSD.

Long answer: Read the LICENSE.md -file.

