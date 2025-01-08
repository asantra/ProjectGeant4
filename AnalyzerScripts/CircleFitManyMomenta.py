### use this code to fit 2D circle and for many momenta and many particles


import numpy as np
import uproot
import matplotlib.pyplot as plt
from scipy.optimize import least_squares


# Define the circle residual function
def circle_residuals(params, x, y, weights):
    x_center, y_center, radius = params
    distances = np.sqrt((x - x_center)**2 + (y - y_center)**2)
    residuals = (distances - radius) * np.sqrt(weights)  # Weighted residuals
    return residuals


# Function to fit a circle
def fit_circle(x_data, y_data, weights):
    # Initial guess for [x_center, y_center, radius]
    initial_guess = [np.mean(x_data), np.mean(y_data), np.std(x_data)]

    # Perform least squares fit
    result = least_squares(circle_residuals, initial_guess, args=(x_data, y_data, weights))

    # Extract fitted parameters
    x_center_fit, y_center_fit, radius_fit = result.x

    # Estimate parameter uncertainties
    jacobian = result.jac  # Jacobian matrix
    covariance_matrix = np.linalg.inv(jacobian.T @ jacobian)  # Covariance matrix
    param_errors = np.sqrt(np.diag(covariance_matrix))  # Parameter errors
    x_center_err, y_center_err, radius_err = param_errors

    # Calculate chi-squared and reduced chi-squared
    residuals = circle_residuals(result.x, x_data, y_data, weights)
    chi_squared = np.sum(residuals**2)
    ndf = len(x_data) - len(result.x)  # Degrees of freedom
    reduced_chi_squared = chi_squared / ndf

    return (x_center_fit, y_center_fit, radius_fit, 
            x_center_err, y_center_err, radius_err, 
            chi_squared, reduced_chi_squared)


### the momentum dictionary: this should match exactly as you used in renameRootFiles.py
momentumDictionary = {"0":"0.0001", # because output0.root corresponds to 0.01 GeV momentum
                      "1":"0.0005", # because output1.root corresponds to 0.2 GeV momentum
                      "2":"0.001", # because output2.root corresponds to 0.5 GeV momentum
                      "3":"0.005", # because output3.root corresponds to 0.8 GeV momentum
                      "4":"0.01", # because output0.root corresponds to 0.01 GeV momentum
                      "5":"0.05", # because output1.root corresponds to 0.2 GeV momentum
                      "6":"0.1", # because output2.root corresponds to 0.5 GeV momentum
                      "7":"0.2", # because output3.root corresponds to 0.8 GeV momentum
                      "8":"0.3",
                      "9":"0.4",
                      "10":"0.5",
                      "11":"0.7",
                      "12":"0.9",
                      "13":"1.1",
                      "14":"1.3",
                      "15":"1.5",
                      "16":"1.8",
                      "17":"2.1",
                      "18":"2.4",
                      "19":"2.7",
                      "20":"3.0",
                      "21":"3.3",
                      "22":"3.6",
                      "23":"4.0",
                      "24":"4.4",
                      "25":"4.8",
                      "26":"5.2",
                      "27":"5.6",
                      "28":"6.0",
                      "29":"7.0",
                      "30":"8.0",
                      "31":"9.0",
                      "32":"10.0",
                      "33":"12.0",
                      "34":"15.0",
                      "35":"20.0",
                      }

## add the particles that you want to prepare the plot for
## the name of the particles must match with what you used for Geant4 file preparation
particleList = ["electron", "proton", "pion"]

### add how you want to make the plots.
### This is explained here: https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot
### Look for "format strings"
### each element in particleList above should have one entry in the following colorDict
colorDict = {"proton":"r-.o", "electron":"p:k", "muon": "1-b", "pion": "+--g", "alpha":"D-c"}

# Load data from ROOT file containing a TTree
# give the absolute path where the root files are living
inDir="/Users/arkasantra/arka/ProjectGeant4/Ex1/"

savedAllFitResults = {}
for particle in particleList:
    savedAllFitResults[particle] = {}
    for mom in momentumDictionary:
        print("--- working on: ", particle, " for momentum: ", momentumDictionary[mom]," GeV")
        root_file_path = inDir+particle+"/output_"+particle+"_"+momentumDictionary[mom].replace('.','p')+"GeV.root"  # Replace with your ROOT file path

        tree_name = "Hits"       # Replace with your TTree name
        x_branch = "fX"          # Replace with your x-coordinate branch name
        y_branch = "fY"          # Replace with your y-coordinate branch name

        # Use uproot to read the TTree and extract x and y data
        try:
            with uproot.open(root_file_path) as file:
                tree = file[tree_name]
                x_data = tree[x_branch].array(library="np")
                y_data = tree[y_branch].array(library="np")
        except:
            print("This file does not exist: ", root_file_path)
            ### if the file does not exist, then the default value is -99999
            savedAllFitResults[particle][mom] = {"radius": -99999, "radius_err": -99999, "angle": -99999, "angle_error": 0, "reduced_chi_square": -99999}
            continue

        # Create a 2D histogram
        hist, x_edges, y_edges = np.histogram2d(x_data, y_data, bins=50)
        x_bin_centers = (x_edges[:-1] + x_edges[1:]) / 2
        y_bin_centers = (y_edges[:-1] + y_edges[1:]) / 2

        # Extract bin centers with significant counts
        x_grid, y_grid = np.meshgrid(x_bin_centers, y_bin_centers)
        x_flat, y_flat = x_grid.flatten(), y_grid.flatten()
        hist_flat = hist.flatten()
        x_fit_data = x_flat[hist_flat > 0]
        y_fit_data = y_flat[hist_flat > 0]
        weights = hist_flat[hist_flat > 0]  # Use counts as weights

        # Fit a circle to the data
        (x_center_fit, y_center_fit, radius_fit,
        x_center_err, y_center_err, radius_err,
        chi_squared, reduced_chi_squared) = fit_circle(x_fit_data, y_fit_data, weights)

        ### the distance from the Cherenkov medium to the detector face is 490 mm, hence the radius is divided by 490 mm to get the Cherenkov angle
        savedAllFitResults[particle][mom] = {"radius": radius_fit, "radius_err": radius_err, "angle": radius_fit/490, "angle_error": (radius_err/490), "reduced_chi_square":reduced_chi_squared}

        # Print results
        print("Fitted Circle Parameters:")
        print(f"Center: ({x_center_fit:.3f} ± {x_center_err:.3f}, {y_center_fit:.3f} ± {y_center_err:.3f})")
        print(f"Radius: {radius_fit:.3f} ± {radius_err:.3f}")
        print("\nGoodness of Fit:")
        print(f"Chi-squared: {chi_squared:.3f}")
        print(f"Reduced Chi-squared (Chi^2/ndf): {reduced_chi_squared:.3f}")

        ### turn off the following lines if you don't want to see the plots
        ### Plot the 2D histogram and the fitted circle
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.imshow(hist.T, origin='lower', extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]], cmap='Blues', alpha=0.7)
        ax.scatter(x_fit_data, y_fit_data, color='red', s=10, label='Significant Points')

        # Plot the fitted circle
        fitted_circle = plt.Circle((x_center_fit, y_center_fit), radius_fit, color='green', fill=False, label='Fitted Circle', linewidth=2)
        ax.add_artist(fitted_circle)

        ax.set_aspect('equal', adjustable='datalim')
        plt.title("2D Histogram Circle Fit from ROOT TTree")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid()
        plt.show()


#### now plot all the angles vs momentum for a particular particle species

### select any three particles, just not to get a very busy plot

angle_values    = {}
angle_errors    = {}
momentum_values = {}
momentum_errors = {}

for particle in savedAllFitResults:
    angle_values[particle]      = []
    angle_errors[particle]      = []
    momentum_values[particle]   = []
    momentum_errors[particle]   = []

    for momentum in savedAllFitResults[particle]:
        if savedAllFitResults[particle][momentum]["angle"] > 0:
            momentum_values[particle].append(momentumDictionary[momentum])
            momentum_errors[particle].append(0.0)
            angle_values[particle].append(savedAllFitResults[particle][momentum]["angle"])
            angle_errors[particle].append(savedAllFitResults[particle][momentum]["angle_error"])




fig2, ax2               = plt.subplots(figsize=(8, 8))

for particle in particleList:
    angle_values_np         = np.array(angle_values[particle])
    angle_values_error_np   = np.array(angle_errors[particle])
    momentum_values_np      = np.array(momentum_values[particle])
    momentum_errors_np      = np.array(momentum_errors[particle])
    ax2.errorbar(momentum_values_np, angle_values_np, angle_values_error_np, linewidth=2,label=particle, fmt=colorDict[particle])

ax2.set(xlabel='momentum [GeV]', ylabel='Angles (Rad)',
       title='Cherenkov angle vs momentum')
ax2.grid()
leg = ax2.legend()

plt.semilogy()
plt.savefig("anglevsmomentum.png")
plt.show()





