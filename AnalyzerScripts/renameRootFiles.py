###########################################################################################
# this is the code to rename root files coming out of the Geant4 simulation
# please remember, this will work only if the root files are ordered according to the follwoing momenta list:
# 0.1, 0.2, 0.5, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0, 2.2, 2.5, 3.0, 3.5, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 18.0, 21.0, 25.0, 30.0, 35.0, 40.0, 50.0, 60.0, 70.0, 80.0, 100.0
# If Geant4 did not produce one or two files because the corresponding momenta are below the Cherenkov threshold, this will still work.

### run: python3 renameRootFiles.py <particleName>
### example: python3 renameRootFiles.py proton

###########################################################################################


### importing python libraries
import glob
import os, sys
import time



### this is the dictionary that maps root file names with the corresponding momenta values
### if you change the momenta values in your original simulation, you have to change the following map accordingly.
### for example, if the 1.5 GeV momentum is missing from your simulation, you need to remove the line "6":"1.5"  - instead use "6":"1.8", "7":"2.0" and so on.

momentumDictionary = {"0":"0.1", # because output0.root corresponds to 0.1 GeV momentum
                      "1":"0.2", # because output1.root corresponds to 0.2 GeV momentum
                      "2":"0.5", # because output2.root corresponds to 0.5 GeV momentum
                      "3":"0.8", # because output3.root corresponds to 0.8 GeV momentum
                      "4":"1.0",
                      "5":"1.2",
                      "6":"1.5",
                      "7":"1.8",
                      "8":"2.0",
                      "9":"2.2",
                      "10":"2.5",
                      "11":"3.0",
                      "12":"3.5",
                      "13":"5.0",
                      "14":"6.0",
                      "15":"8.0",
                      "16":"10.0",
                      "17":"12.0",
                      "18":"15.0",
                      "19":"18.0",
                      "20":"21.0",
                      "21":"25.0",
                      "22":"30.0",
                      "23":"35.0",
                      "24":"40.0",
                      '25':"50.0",
                      "26":"60.0",
                      "27":"70.0",
                      "28":"80.0",
                      "29":"100.0"
                      }

### the main function
def main():
    ### we assume this file is kept inside `MyProject/ProjectGeant4/AnalyzerScripts` directory
    ### we also assume the root files are kept inside the 'MyProject/ProjectGeant4/build'
    FileLocation = "../build/"
    ### get all the root files from `build`
    inFileList = glob.glob(FileLocation+"*root")

    ### please input the particle type
    particleName = sys.argv[1]

    ### create the folder if it does not exist
    try:
        os.makedirs(particleName) 
        print("Folder '% s' created" % particleName)
    except:
        print("The folder ", particleName, " already exists")

    ### Now rename the root files and save them inside the directory
    for filename in inFileList:
        ### get the order number of the root file
        orderNumber = filename.split("output")[1].split(".root")[0]

        try:
            newmomentum = momentumDictionary[orderNumber].replace('.','p')
        except:
            print("The order number of the root file does not match with the momentum value in the dictionary. Can't proceed, please check what is wrong!!!")
            exit()

        newFileName = "output_"+particleName+"_"+newmomentum+"GeV.root"
        ### first rename the root files
        os.system('mv '+filename+" "+newFileName)
        ### then move them inside the folder
        os.system("mv "+newFileName+" "+particleName)
        print("The file ", filename, " is renamed to ", newFileName, " and kept inside ", particleName, " folder")


if __name__=="__main__":
    ### call the main function above
    main()

