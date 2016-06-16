"""
Photogrammetry toolkit
"""
import argparse
import os

import SocketServer
import Photogrammetry
import PhotogrammetryServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Reconstruct a Poisson surface from photos using photogrammetry.')
    parser.add_argument("--telnet_port", help="Telnet port",default = 12345, type=int)
    parser.add_argument("--ftp_port", help="Ftp port", default = 54321, type=int)

    args = parser.parse_args()
    pg = Photogrammetry.Photogrammetry()
    print args
    if args.telnet_port:#TODO
        server = SocketServer.TCPServer(("localhost", args.telnet_port), PhotogrammetryServer.PhotogrammetryServer)
        print("Running daemon on port ", args.telnet_port)
        # Activate the server; this will keep running until you interrupt the program with Ctrl-C
        server.serve_forever()
    else:
        parser.print_help()
        exit("Error: Incorrect arguments provided")


