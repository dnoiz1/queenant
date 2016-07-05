# QueenAnt: Queen of the Antminers

Application to take over mining destination of remote cgminer instances via RPC interface.

Changes are non-persistant, this is a PoC and not intended for real world use.

# You what, mate?

cgminer is a popular BTC mining application.    

cgminer can be (and often is) configured to accept incoming connections on a TCP port (4028)
to expose a RPC interface - usually for checking on and collecting statistics from groups of mining machines.
More importantly, configuration of cgminer.    

[cgminer API RTFM](https://github.com/ckolivas/cgminer/blob/master/API-README)

Of note, [Bitmain](http://www.bitmaintech.com) is a Chinese manufacturer of powerful, self managed ASIC arrays
called AntMiners. The S9 model, pushing over 14th/s.

The operating system of these devices is a openwrt build that include cgminer with configuration controlled by
the LuCi web interface from openwrt, running on a beageboard or similar.

Unfortunately, it collects its stats from the RPC interface, which is listening on 0.0.0.0 without a username
or password configured. many of these are on the internet.

This was tested and confirmed on an Antminer S5 with all available firmware releases.

# &then?

It's also interesting to note 2 other things about the Antminer firmware:
- cgminer is running as root, in screen, and RPC can write files.
- updating the admin password via LuCi web interface does not update system accounts
- root as ssh is open (default pw: admin)

# Author

Tim Noise <tim@drkns.net>    
also i stole some code from here: https://thomassileo.name/blog/2013/09/17/playing-with-python-and-cgminer-rpc-api/

# Tip Jar
Obligitory don't send me stolen BTC.

BTC: 1CN9DuS7u8UY1YGDWCKASswcoi1Sqdm61f
