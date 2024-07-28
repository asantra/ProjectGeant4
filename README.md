# Introduction 
This is a repository of Geant4. The goal is to generate Cherenkov light and detect them. 
You can know more about the Cherenkov light here on this [YouTube](https://www.youtube.com/watch?v=Yjx0BSXa0Ks&ab_channel=Fermilab) video.

## Code setup
The code is written using C++ following the class structure of Geant4.
If you want, this is a very good tutorial [video series](https://www.youtube.com/watch?v=Lxb4WZyKeCE&list=PLLybgCU6QCGWgzNYOV0SKen9vqg4KXeVL&ab_channel=PhysicsMatters) on Cherenkov light detector on Geant4.
The code setup is based exactly on this video series (upto Tutorial 9). 
*(This is a long video series. You can save the details for future.)*

# Useful commands for a Linux Terminal
This section highlights a few useful linux commands that may be used during this simulation project. 
1. Open a terminal window: if you are on Ubuntu, look for `terminal` app on the Ubuntu left side panel. Then click on it - this will open the terminal window which will be your main work area (don't forget to hit the `enter` button after typing out each command).

2. Go inside a directory: suppose you want to go inside the directory `Temp`. Then you have to do
```
cd Temp
```

3. Come out of a directory: suppose you need to come out of the directory `Temp`. Then you have to do (if you are already inside the directory `Temp`):
```
cd ..
```
(remember the space between `cd` and `..`)

4. Edit a file: you can use your favourite code editor, like `vim`, `emacs` or `VSCode`. For simplicity, we will use `gedit` code editor. If you need to edit a file (say `run.mac`), then you can open the file (first you have to go to the folder where the file exists):
``` 
gedit run.mac&
```
the trailing `&` is necessary to detach the terminal from `gedit`. 
After editing the file, you need to save the file by just pressing `control` and `s` keys together (`ctrl+s`) from the keyboard.

The `gedit` has many keyboard shortcuts similar to `MS Word`: for copying, use `ctrl+c` (meaning pressing `control` and `c` keys together); for pasting, use `ctrl+v`; for undo the recent edit, use `ctrl+z`

5. See the name of the folders or files in a particular location:
```
ls
```
this will list all the files/folders on the terminal.

6. To delete something in the terminal: to delete a file (say `myFile.txt`), simply type `rm myFile.txt` and hit enter; to delete a folder (say `Temp`) type `rm -rf Temp` and hit enter.

7. If you need to copy something from the terminal, use `ctrl+shift+c` (meaning pressing the `control`, `shift` and the `c` keys together). For pasting on the terminal, use `ctrl+shift+v` (note the difference from the `gedit` commands). 

# Installation of the code setup
The code setup depends explicitly on Geant4 classes.
Before you compile the code, make sure that in your system, Geant4 is properly installed and sourced.
The instructions on Geant4 download and installation can be found on this [Geant4 Doc Page](https://geant4.web.cern.ch/docs/getting-started).

**For the BHU ISc Physics MSc final year nuclear physics lab PC, Geant4 is already installed.**
## Download the Cherenkov Code setup from git
1. Please first open a terminal. Then create a new repository (here `MyProject`) and go inside that: 
```
mkdir MyProject && cd MyProject
``` 

2. Download the git repository
```
git clone https://github.com/asantra/ProjectGeant4.git
```

3. Go inside the git repository and download the relevant tag:
```
cd ProjectGeant4
git checkout tags/Cherenkov -b CherenkovBranch
```

4. Make the repository using `cmake` (use the commands on the terminal one by one):
```
mkdir build && cd build
cmake ..
cmake --build . -j6
```

5. If there is no installation error message, then the code setup should be properly installed. 


# Running the setup
1. While inside the `build` directory, please look for the built object `sim` (you can use `ls` command).

2. You can run it interactively or in batch mode. 
- ## For intereactive running, please type the following command on the terminal inside the `build` directory: 
 ```
 ./sim
 ```
   - This should open a `QT` dialogue box. The experimental setup should be visible here. 
   - Click on the green arrow button on the top panel. One click on this arrow will initiate one particle. The original particle (in blue) and Cherenkov light (in green) coming out of that should be clearly visible.
   - You can click more on the green arrow to generate more events.
   - The interactive setup is good for 5-10 events; if we want to generate events in bulk (say around 1000), then we need to use the batch mode of running (simply because we cannot hit the green button 1000 times in a short time). 
   - Cross out the dialogue box (cross button on the top corner, either left or right depending on your system)
   - The output of the Cherenkov detection should be saved inside `output0.root` file. This file must be kept inside the `build` folder. 
   - This root file keeps only a few events: not very useful for us. You can delete the root files generated here by using the command: `rm output*.root`

- ## For batch mode running,  please type the following command on the terminal inside the `build` directory: 
 ```
 ./sim run.mac
 ```
   - This should initiate the batch mode of running, i.e. here you won't see any dialogue box.
   - If you are using the original `run.mac` (i.e. didn't edit anything there), then you should see three output files stored inside `build` directory:
    - output0.root for 0.5 GeV proton (100 events)
    - output1.root for 1.0 GeV proton (100 events)
    - output2.root for 5.0 GeV proton (100 events)

   - We will learn to analyze the root files later.

# Change the particles and its parameters. 
1. Emission of Cherenkov light depends on the particle velocity. The cone angle of Cherenkov light emission also depends on particle velocity.
2. If we use different particle type and particle energy, then the detected Cherenkov light should be different too. This is why many particle physics experiments use the Cherenkov detectors to identify the particle. 
3. To change the momentum of the particle, please go inside the `run.mac` file in the top level directory of the repository (in this example: `ProjectGeant4`).
4. You will see lines:
```
/gun/momentumAmp 0.5 GeV
/run/printProgress 10
/run/beamOn 100
```
5. Here first line refers to the particle momentum of 0.5 GeV. The second line dictates after how many events you want a print out. The third line tells you how many particles we want to generate (here it is 100).
6. In the unedited `run.mac` file, there should be three sets of such commands: the first set corresponds to `output0.root`, the second corresponds to `output1.root` and so on. If there is a fourth set of commands appended to `run.mac`, the corresponding output file will be `output3.root`. 
6. You can either change the values there, or you can append your lines to this file:
```
/gun/momentumAmp 10 GeV
/run/printProgress 20
/run/beamOn 200
```
7. This means we want to generate 10 GeV particle and the number of particles will be 200, and the print progression is 20 (i.e. `Geant4` will print the progress of the run in every 20 events). 
8. Now we have to use the following commands inside the `build` directory:
```
cmake ..
./sim run.mac
```
9. After the run, you should be able to find the output root files.
10. Changing the particle type is a little bit involved. Please go to the top level directory of the repository (in this example `ProjectGeant4`). If you are in the `build` directory then use `cd ..` to reach to the `ProjectGeant4`.
11. Go to the file `generator.cc` and look for this line:
```
G4String particleName = "proton";
```

12. This means we used `proton` as our particle. We can change to any charged particles (please use these names, otherwise `Geant4` may not understand your request):
> alpha, anti_proton, e+, e-, mu+, mu-, pi+, pi-, proton, tau+, tau-.

13. Please change to your desired particle name in the lines mentioned in step 11 above. Save the file `generator.cc`.
14. Now go to the `build` directory and compile the project again:
```
cd build
cmake ..
cmake --build . -j6
```

15. If the compilation is successful, you can run the project just like before:
```
./sim run.mac
```

16. Remember one thing, _everytime you run the setup, the previous output root files are overwritten. If you need to keep the output files from the previous runs, please store the root files away from the `build` directory_. 

17. It is a good practice to rename the output root files according to the particle type and energy. You can rename the root files in the following way inside the `build` directory:
```
mv output0.root output_proton_0p5GeV.root
mv output1.root output_proton_1p0GeV.root
...
```
as `output0.root` belongs to 0.5 GeV proton and `output1.root` belongs to 1.0 GeV proton. Similarly for electron particle (after running on `electron` particles in `Geant4`), one can change the output root files to 
```
mv output0.root output_electron_0p5GeV.root
mv output1.root output_electron_1p0GeV.root
...
```

18. If you want to save the root files from proton in a separate folder (say `ProtonFiles` inside the `ProjectGeant4` repository) outside of `build` directory, then use the commands inside the `build` directory:
```
mkdir ../ProtonFiles
mv output_proton_*root ../ProtonFiles
```

Similarly, if you want to keep electron files away from the `build` directory then use the following commands from the `build` directory:
```
mkdir ../ElectronFiles
mv output_electron_*root ../ElectronFiles
```

