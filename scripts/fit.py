# Fitting equations and functions

import scipy.optimize as opt
import numpy as np

def kdfit(P, Kd, S, O):
    return S*(P/(P+Kd))+O

def quad(P, Kd, S, O, L): # in this form, L refers to the ligand held at constant concentration
    a = P+L+Kd
    return S*((a-(((a**2)-(4*P*L))**0.5))/(2*L))+O

def hill(P, Kd, n, S, O):
    return	S*((P**(n)/((P**(n)+(Kd**(n))))))+O

def multi(P, Kd, S, O, Kd2, S2):
    return (S*(P/(Kd+P))+S2*(P/(Kd2+P)))+O


def r_squared(y, residuals):
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y-np.mean(y))**2)
    r_sq = 1-(ss_res/ss_tot)
    return r_sq

def getkdfit(x, y, units, fit_dict):
    # need to re-write the fitting functions to work with 1 sample at a time
    parameters_dict = {}

    p0 = [
        fit_dict["Kdi"],
        fit_dict["Si"],
        fit_dict["Oi"]
    ]

    popt, _ = opt.curve_fit(kdfit, x, y, p0=p0, bounds=((0,0,0),(np.inf,np.inf,np.inf)))

    x_fit = np.geomspace(x[-1], x[0], 50)
    y_fit = kdfit(x_fit, *popt)

    # popt[1] is S, popt[2] is O
    y_norm = (y-popt[2])/popt[1]

    #calculate R-squared
    residuals = y - kdfit(x, *popt)
    r_sq = r_squared(y, residuals)

    parameters_dict[f"Kd ({units})"] = str(round(popt[0],2))
    parameters_dict["S"] = str(round(popt[1],4))
    parameters_dict["O"] = str(round(popt[2],4))
    parameters_dict["R^2"] = str(round(r_sq,4))

    return x_fit, y_fit, y_norm, parameters_dict


def getquadfit(x, y, ligand, p0, units):
    fits_x = []
    fits_y = []
    y_norm = []
    param_table = [["Kd ("+units+")"],["S"],["O"],["R^2"]]
    for i in range(len(y)):
        x[i] = np.array(x[i])
        y[i] = np.array(y[i])
        #use a lambda function to fix L in the quad equation
        popt, _ = opt.curve_fit(lambda P, Kd, S, O: quad(P, Kd, S, O, ligand[i]), 
            x[i], y[i], p0=p0, bounds=((0,0,0),(np.inf,np.inf,np.inf)))
        fits_x.append(np.geomspace(x[i][len(x[i])-1], x[i][0], 50))   
        fits_y.append(quad(fits_x[i], popt[0], popt[1], popt[2], ligand[i]))
        #use estimated parameters to normalize anisotropy to be fraction bound
        y_norm.append((y[i]-popt[2])/popt[1])
        #calculate R-squared
        residuals = (y[i] - quad(x[i], popt[0], popt[1], popt[2], ligand[i]))
        r_sq = r_squared(y[i], residuals)
        #format parameters for table
        param_table[0].append(str(round(popt[0],2)))
        param_table[1].append(str(round(popt[1],4)))
        param_table[2].append(str(round(popt[2],4)))
        param_table[3].append(str(round(r_sq,4)))
    return fits_x, fits_y, y_norm, param_table

def gethillfit(x, y, p0, units):
    fits_x = []
    fits_y = []
    y_norm = []
    p0_n = [p0[0], 1.0, 1.0, p0[1], p0[2]]
    param_table = [["Kd ("+units+")"],["n"],["S"],["O"],["R^2"]]
    for i in range(len(y)):
        x[i] = np.array(x[i])
        y[i] = np.array(y[i])
        popt, _ = opt.curve_fit(hill, x[i], y[i], p0=p0_n, bounds=((0,0,0,0),(np.inf,np.inf,np.inf,np.inf)))
        fits_x.append(np.geomspace(x[i][len(x[i])-1], x[i][0], 50))   
        fits_y.append(hill(fits_x[i], *popt))
        #use estimated parameters to normalize anisotropy to be fraction bound
        y_norm.append((y[i]-popt[3])/popt[2])
        #calculate R-squared
        residuals = y[i] - hill(x[i], *popt)
        r_sq = r_squared(y[i], residuals)
        #format parameters for table
        param_table[0].append(str(round(popt[0],2)))
        param_table[1].append(str(round(popt[1],2)))
        param_table[2].append(str(round(popt[2],4)))
        param_table[3].append(str(round(popt[3],4)))
        param_table[4].append(str(round(r_sq,4)))
    return fits_x, fits_y, y_norm, param_table

def getmultifit(x, y, p0, units):
    fits_x = []
    fits_y = []
    y_norm = []
    param_table = [["Kd1 ("+units+")"],["Kd2 ("+units+")"],["S1"],["S2"],["O"],["R^2"]]
    for i in range(len(y)):
        x[i] = np.array(x[i])
        y[i] = np.array(y[i])
        popt, _ = opt.curve_fit(multi, x[i], y[i], p0=p0, bounds=((0,0,0,0,0),(np.inf,np.inf,np.inf,np.inf,np.inf)))
        fits_x.append(np.geomspace(x[i][len(x[i])-1], x[i][0], 50))   
        fits_y.append(multi(fits_x[i], *popt))
        #use estimated parameters to normalize anisotropy to be fraction bound
        #I have no idea how normalization works for the multi-site fit
        #y_norm.append((y[i]-popt[2])/popt[1])
        #calculate R-squared
        residuals = y[i] - multi(x[i], *popt)
        r_sq = r_squared(y[i], residuals)
        #format parameters for table
        param_table[0].append(str(round(popt[0],2)))
        param_table[1].append(str(round(popt[3],2)))
        param_table[2].append(str(round(popt[1],4)))
        param_table[3].append(str(round(popt[4],4)))
        param_table[4].append(str(round(popt[2],4)))
        param_table[5].append(str(round(r_sq,4)))
    return fits_x, fits_y, y_norm, param_table