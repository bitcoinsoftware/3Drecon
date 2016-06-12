"""
Photogrammetry toolkit
"""
import argparse
import os

import SupportFunctions
import SocketServer
import Photogrammetry2 as Photogrammetry
import PhotogrammetryServer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Reconstruct a Poisson surface from photos using photogrammetry.')
    
    parser.add_argument("--deamon", help="Run as deamon", action="store_true", default = False)
    parser.add_argument("--port", help="Deamon port",default = 12345, type=int)
    
    parser.add_argument('--url', help='URL of a folder with photos or video file')
    parser.add_argument("-s", "--sparse-recon", help="Step 0. Sparse pointcloud reconstruction", action="store_true", default = False)
    parser.add_argument("-d", "--dense-recon",  help="Step 1. Dense pointcloud reconstruction", action="store_true", default = False)
    parser.add_argument("-m", "--mesh-texture", help="Step 2. Meshing and texturing", action="store_true", default =False)
    parser.add_argument("-g", "--georeference", help="Step 3. generate mesh", action="store_true", default = False)

    args = parser.parse_args()
    pg = Photogrammetry.Photogrammetry()
    print args
    if args.deamon and args.port:#TODO
        server = SocketServer.TCPServer(("localhost", args.port), PhotogrammetryServer.PhotogrammetryServer)
        # Activate the server; this will keep running until you interrupt the program with Ctrl-C
        server.serve_forever()

    elif os.path.isdir(args.url):
        sparse_recon_output_path, dense_recon_output_path, meshing_output_path, texturing_output_path, georeference_output_url = None, None, None, None, None
        input_url = args.url
        if args.sparse_recon:#sparse recon
            sparse_recon_output_path = pg.getSparseRecon(input_url)
        if args.dense_recon:
            if args.sparse_recon:
                input_url = sparse_recon_output_path
            dense_recon_output_path = pg.getDenseRecon(input_url)
        if args.mesh_texture:
            if args.dense_recon:
                input_url = dense_recon_output_path
            meshing_output_path = pg.getMesh(input_url)
            texturing_output_path = pg.getTexture(meshing_output_path)
        if args.georeference:
            if args.mesh_texture:
                input_url = texturing_output_path
            georeference_output_url = pg.getGeoreference(input_url)
    else:
        parser.print_help()
        exit("Error: Incorrect url provided")


