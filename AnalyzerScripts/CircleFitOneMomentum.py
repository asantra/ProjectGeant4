### use this code to fit 2D circle and for one momentum
import numpy as np
import uproot
import sys
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

# Load data from ROOT file containing a TTree
root_file_path = sys.argv[1]  # Get the tree name from the command line during run time
tree_name = "Hits"       # Replace with your TTree name
x_branch = "fX"          # Replace with your x-coordinate branch name
y_branch = "fY"          # Replace with your y-coordinate branch name

# Use uproot to read the TTree and extract x and y data
with uproot.open(root_file_path) as file:
    tree = file[tree_name]
    x_data = tree[x_branch].array(library="np")
    y_data = tree[y_branch].array(library="np")

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

# Print results
print("Fitted Circle Parameters:")
print(f"Center: ({x_center_fit:.3f} ± {x_center_err:.3f}, {y_center_fit:.3f} ± {y_center_err:.3f})")
print(f"Radius: {radius_fit:.3f} ± {radius_err:.3f}")
print("\nGoodness of Fit:")
print(f"Chi-squared: {chi_squared:.3f}")
print(f"Reduced Chi-squared (Chi^2/ndf): {reduced_chi_squared:.3f}")

# Plot the 2D histogram and the fitted circle
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
plt.savefig("circlefit.png")
plt.show()


