#!/usr/bin/python3
""" # doc string which gives details about the rpc server which runs a service, also info regarding the code its using and port its connecting to
classic rpyc server (threaded, forking or std) running a SlaveService
usage:
    rpyc_classic.py                         # default settings
    rpyc_classic.py -m forking -p 12345     # custom settings

    # ssl-authenticated server (keyfile and certfile are required) # establish a SSL certificate which makes sure the connection between the client and server is secure
    rpyc_classic.py --ssl-keyfile keyfile.pem --ssl-certfile certfile.pem --ssl-cafile cafile.pem # defined a cert?
"""
import sys # import the sys library which specifies the parameters and functions
import os # import the operating system library, allows to talk to the os that python is on
import rpyc # remote objects to be manipulated 
from plumbum import cli # from plumbum is a lib for shell script programs which imports the command line interface or tools
from rpyc.utils.server import ThreadedServer, ForkingServer, OneShotServer # from the rpyc server import the thread server, fork and one short server
from rpyc.utils.classic import DEFAULT_SERVER_PORT, DEFAULT_SERVER_SSL_PORT # from rpyc utilities it is importing the features for the server and its normal and SSL Ports
from rpyc.utils.registry import REGISTRY_PORT # imports the registry port
from rpyc.utils.registry import UDPRegistryClient, TCPRegistryClient # imports the UDP protocol client and TCP Protocol client
from rpyc.utils.authenticators import SSLAuthenticator # imports the SSL authentication for verification
from rpyc.lib import setup_logger # imports the set up logger feature to  examine log files?
from rpyc.core import SlaveService # imports the slave service ?



class ClassicServer(cli.Application): # defines method ClassicServer and passes in argument cmd line interface Application
    mode = cli.SwitchAttr(["-m", "--mode"], cli.Set("threaded", "forking", "stdio", "oneshot"), # var mode with cli 
        default = "threaded", help = "The serving mode (threaded, forking, or 'stdio' for "
        "inetd, etc.)")

    port = cli.SwitchAttr(["-p", "--port"], cli.Range(0, 65535), default = None, 
        help="The TCP listener port (default = %s, default for SSL = %s)" %
            (DEFAULT_SERVER_PORT, DEFAULT_SERVER_SSL_PORT), group = "Socket Options")
    host = cli.SwitchAttr(["--host"], str, default = "", help = "The host to bind to. "
        "The default is localhost", group = "Socket Options")
    ipv6 = cli.Flag(["--ipv6"], help = "Enable IPv6", group = "Socket Options")

    logfile = cli.SwitchAttr("--logfile", str, default = None, help="Specify the log file to use; "
        "the default is stderr", group = "Logging")
    quiet = cli.Flag(["-q", "--quiet"], help = "Quiet mode (only errors will be logged)",
        group = "Logging")

    ssl_keyfile = cli.SwitchAttr("--ssl-keyfile", cli.ExistingFile,
        help = "The keyfile to use for SSL. Required for SSL", group = "SSL",
        requires = ["--ssl-certfile"])
    ssl_certfile = cli.SwitchAttr("--ssl-certfile", cli.ExistingFile,
        help = "The certificate file to use for SSL. Required for SSL", group = "SSL",
        requires = ["--ssl-keyfile"])
    ssl_cafile = cli.SwitchAttr("--ssl-cafile", cli.ExistingFile,
        help = "The certificate authority chain file to use for SSL. Optional; enables client-side "
        "authentication", group = "SSL", requires = ["--ssl-keyfile"])

    auto_register = cli.Flag("--register", help = "Asks the server to attempt registering with "
        "a registry server. By default, the server will not attempt to register",
        group = "Registry")
    registry_type = cli.SwitchAttr("--registry-type", cli.Set("UDP", "TCP"),
        default = "UDP", help="Specify a UDP or TCP registry", group = "Registry")
    registry_port = cli.SwitchAttr("--registry-port", cli.Range(0, 65535), default=REGISTRY_PORT,
        help = "The registry's UDP/TCP port", group = "Registry")
    registry_host = cli.SwitchAttr("--registry-host", str, default = None,
        help = "The registry host machine. For UDP, the default is 255.255.255.255; "
        "for TCP, a value is required", group = "Registry")

    def main(self):
        if not self.host:
            self.host = "::1" if self.ipv6 else "127.0.0.1"

        if self.registry_type == "UDP":
            if self.registry_host is None:
                self.registry_host = "255.255.255.255"
            self.registrar = UDPRegistryClient(ip = self.registry_host, port = self.registry_port)
        else:
            if self.registry_host is None:
                raise ValueError("With TCP registry, you must specify --registry-host")
            self.registrar = TCPRegistryClient(ip = self.registry_host, port = self.registry_port)

        if self.ssl_keyfile:
            self.authenticator = SSLAuthenticator(self.ssl_keyfile, self.ssl_certfile,
                self.ssl_cafile)
            default_port = DEFAULT_SERVER_SSL_PORT
        else:
            self.authenticator = None
            default_port = DEFAULT_SERVER_PORT
        if self.port is None:
            self.port = default_port

        setup_logger(self.quiet, self.logfile)

        if self.mode == "threaded":
            self._serve_mode(ThreadedServer)
        elif self.mode == "forking":
            self._serve_mode(ForkingServer)
        elif self.mode == "oneshot":
            self._serve_oneshot()
        elif self.mode == "stdio":
            self._serve_stdio()

    def _serve_mode(self, factory):
        t = factory(SlaveService, hostname = self.host, port = self.port,
            reuse_addr = True, ipv6 = self.ipv6, authenticator = self.authenticator,
            registrar = self.registrar, auto_register = self.auto_register)
        t.start()

    def _serve_oneshot(self):
        t = OneShotServer(SlaveService, hostname = self.host, port = self.port,
            reuse_addr = True, ipv6 = self.ipv6, authenticator = self.authenticator,
            registrar = self.registrar, auto_register = self.auto_register)
        sys.stdout.write("rpyc-oneshot\n")
        sys.stdout.write("%s\t%s\n" % (t.host, t.port))
        sys.stdout.flush()
        t.start()

    def _serve_stdio(self):
        origstdin = sys.stdin
        origstdout = sys.stdout
        sys.stdin = open(os.devnull, "r")
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
        conn = rpyc.classic.connect_pipes(origstdin, origstdout)
        try:
            try:
                conn.serve_all()
            except KeyboardInterrupt:
                print( "User interrupt!" )
        finally:
            conn.close()


if __name__ == "__main__":
    ClassicServer.run()

