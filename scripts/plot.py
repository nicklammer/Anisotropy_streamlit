import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.font_manager import FontProperties
matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"
plt.rcParams['svg.fonttype'] = 'none'
import scipy.optimize as opt
import numpy as np

def r_squared(y, residuals):
	ss_res = np.sum(residuals**2)
	ss_tot = np.sum((y-np.mean(y))**2)
	r_sq = 1-(ss_res/ss_tot)
	return r_sq

