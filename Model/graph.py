from io import BytesIO
from matplotlib.colors import Normalize
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

def draw(values):
    y = values
    y = [i*100 for i in y]
    x = np.linspace(0, 24, len(y))  # Create evenly spaced x values

    norm = Normalize(vmin=min(y), vmax=max(y))
    # Define new x values for interpolation
    x_interp = np.linspace(0, 24, 1000)

    # Interpolate y values for the new x values
    y_interp = np.interp(x_interp, x, y)

    # Plot the scatter plot with interpolated colors
    plt.scatter(x_interp, y_interp, c=cm.coolwarm(norm(y_interp)), edgecolor="none", s=15)
    plt.xlabel('Hours')
    plt.ylabel('Probabilities (%)')
    plt.title('Accident trend over time')
    plt.xticks([i for i in range(0,24)])
    plt.xlim(0,23)

    # Save the plot to a BytesIO object
    img_bytes_io = BytesIO()
    plt.savefig(img_bytes_io, format='jpeg')
    img_bytes_io.seek(0)
    
    # Clear the plot to avoid memory leaks
    plt.clf()
    
    return img_bytes_io.getvalue()