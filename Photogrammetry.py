import os
import commands
import subprocess
import sys

class Photogrammetry:
    def __init__(self):
        script_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.OPENMVG_SFM_BIN = os.path.join(script_path, "openMVG/openMVG_Build/Linux-x86_64-RELEASE") # Indicate the openMVG binary directory
        self.CAMERA_SENSOR_WIDTH_DIRECTORY = os.path.join(script_path, "3Drecon") # Indicate the openMVG camera sensor width directory
        self.MVE_BIN = os.path.join(script_path,"../mve/apps")
        self.TEXRECON_BIN = os.path.join(script_path,"../mvs-texturing/build/apps/texrecon/texrecon")

    def getSparseRecon(self, input_dir): #TODO add parameters
        matches_dir = os.path.join(input_dir, "matches")
        reconstruction_dir = os.path.join(input_dir, "reconstruction_global")
        camera_file_params = os.path.join(self.CAMERA_SENSOR_WIDTH_DIRECTORY, "sensor_width_camera_database.txt")
        print ("Using input dir  : ", input_dir)
        # Create the matches folder if not present
        if not os.path.exists(matches_dir):
          os.mkdir(matches_dir)
        print ("1. Intrinsics analysis")
        print os.path.join(self.OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing")
        pIntrisics = subprocess.Popen( [os.path.join(self.OPENMVG_SFM_BIN, "openMVG_main_SfMInit_ImageListing"),  "-i", input_dir, "-o", matches_dir, "-d", camera_file_params] )
        pIntrisics.wait()
        exit()
        print ("2. Compute features")
        pFeatures = subprocess.Popen( [os.path.join(self.OPENMVG_SFM_BIN, "openMVG_main_ComputeFeatures"), "-pULTRA", "--numThreads="+"8", "-i", os.path.join(matches_dir, "sfm_data.json"), "-o", matches_dir, "-m", "SIFT"] )
        pFeatures.wait()
        print ("3. Compute matches")
        pMatches = subprocess.Popen( [os.path.join(self.OPENMVG_SFM_BIN, "openMVG_main_ComputeMatches"),  "-i", os.path.join(matches_dir, "sfm_data.json"), "-o", matches_dir, "-g", "e"] )
        pMatches.wait()
        # Create the reconstruction if not present
        if not os.path.exists(reconstruction_dir):
            os.mkdir(reconstruction_dir)
        print ("4. Do Global reconstruction")
        pRecons = subprocess.Popen( [os.path.join(self.OPENMVG_SFM_BIN, "openMVG_main_GlobalSfM"),  "-i", os.path.join(matches_dir, "sfm_data.json"), "-m", matches_dir, "-o", reconstruction_dir] )
        pRecons.wait()
        print ("5. Colorize Structure")
        pRecons = subprocess.Popen( [os.path.join(self.OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", os.path.join(reconstruction_dir, "sfm_data.bin"), "-o", os.path.join(reconstruction_dir,"colorized.ply")] )
        pRecons.wait()
        print ("8. Transfer to MVE format")
        pRecons = subprocess.Popen( [os.path.join(self.OPENMVG_SFM_BIN, "openMVG_main_openMVG2MVE2"),  "-i", os.path.join(reconstruction_dir, "sfm_data.bin"), "-o", reconstruction_dir] )
        pRecons.wait()
        return reconstruction_dir
        """
        # optional, compute final valid structure from the known camera poses
        print ("6. Structure from Known Poses (robust triangulation)")
        pRecons = subprocess.Popen( [os.path.join(self.OPENMVG_SFM_BIN, "openMVG_main_ComputeStructureFromKnownPoses"),  "-i", output_url, "-m", matches_dir, "-f", os.path.join(matches_dir, "matches.e.bin"), "-o", os.path.join(reconstruction_dir,"robust.bin")] )
        pRecons.wait()
        print ("7. Colorize robust structure")
        pRecons = subprocess.Popen( [os.path.join(self.OPENMVG_SFM_BIN, "openMVG_main_ComputeSfM_DataColor"),  "-i", os.path.join(reconstruction_dir, "robust.bin"), "-o", os.path.join(reconstruction_dir, "robust_colorized.ply")] )
        pRecons.wait()
        print ("###!!!>>> SPARSE RECONSTRUCTION SAVED TO "+ os.path.join(reconstruction_dir, "robust_colorized.ply") +" <<<!!!###")
        """

    def getDenseRecon(self, reconstruction_dir): #TODO add parameters
        print ("9. Run MVE::dmrecon")
        #print os.path.join(self.MVE_BIN, "dmrecon/dmrecon"), os.path.join(reconstruction_dir, "MVE" )
        pMVErecon = subprocess.Popen([os.path.join(self.MVE_BIN, "dmrecon", "dmrecon"), "-s1", "--force", os.path.join(reconstruction_dir, "MVE")])
        pMVErecon.wait()
        print ("10. Generate point set with MVE::scene2pset")
        #print os.path.join(self.MVE_BIN, "scene2pset","scene2pset") , "-pcsn", "-F1", os.path.join(reconstruction_dir, "MVE"), os.path.join(reconstruction_dir, "MVE")
        output_url = os.path.join(reconstruction_dir, "MVE", "dense_pointset.ply")
        pMVErecon = subprocess.Popen([os.path.join(self.MVE_BIN, "scene2pset", "scene2pset"), "-pcsn","-F1", os.path.join(reconstruction_dir, "MVE"), output_url])
        pMVErecon.wait()
        print ("###!!!>>> DENSE RECONSTRUCTION SAVED TO "+ output_url +" <<<!!!###")
        return output_url

    def getMesh(self, input_file_path): #TODO add parameters
        print("Please provide the file path to dense_pointset.ply")
        reconstruction_dir_MVE = os.path.dirname(input_file_path)
        print("11. Surface reconstruction with MVE::fssrecon")
        #pMVErecon = subprocess.Popen([os.path.join(self.MVE_BIN, "fssrecon/fssrecon"), "--interpolation="+"linear", os.path.join(reconstruction_dir, "MVE", "dense_pointset.ply"), os.path.join(reconstruction_dir, "MVE", "surface.ply")])
        surface_file_path = os.path.join(reconstruction_dir_MVE, "surface.ply")
        pMVErecon = subprocess.Popen([os.path.join(self.MVE_BIN, "fssrecon", "fssrecon"), "--interpolation=" + "linear", input_file_path, surface_file_path])
        pMVErecon.wait()
        print("12. Surface cleaning with MVE::meshclean")
        output_url = os.path.join(reconstruction_dir_MVE, "clean_surface.ply")
        pMVErecon = subprocess.Popen([os.path.join(self.MVE_BIN, "meshclean", "meshclean"), "--percentile="+"10", "--component-size="+"10000", "--delete-scale", "--delete-conf", surface_file_path, output_url ])
        pMVErecon.wait()
        print ("###!!!>>> MESH SAVED TO "+ output_url +" <<<!!!###")
        return output_url

    def getTexture(self, input_file_path): #TODO add parameters
        print("Please provide the file path to clean_surface.ply")
        reconstruction_dir_MVE = os.path.dirname(input_file_path)
        print("13. Surface texturing with texrecon::texrecon")
        pTexrecon = subprocess.Popen([self.TEXRECON_BIN, reconstruction_dir_MVE + "::undistorted", input_file_path, "textured_clean_surface"])
        pTexrecon.wait()
        output_url = os.path.join(reconstruction_dir_MVE, "textured_clean_surface"+".obj")
        print ("###!!!>>> TEXTURED OBJECT SAVED TO "+ output_url +" <<<!!!###")
        return output_url

    def getGeoreference(self, input_file_path):
        return None


