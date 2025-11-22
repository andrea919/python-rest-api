"""
blocklist.py

This file just contains the blocklist of the JWT tokens. It will be omported by the app and 
the logout resource soo that tokens can be added to the blocklist when the user logs out.
"""

BLOCKLIST = set()