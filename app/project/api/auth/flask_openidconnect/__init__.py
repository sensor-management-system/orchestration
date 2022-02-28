"""
Package for the flask_openidconnect extension.

Also contains one instance of the openidconnect extension.
"""

from .extension import OpenIDConnect

open_id_connect = OpenIDConnect()
