# Fitting equations and functions

import scipy.optimize as opt
import numpy as np

def simplified(P, Kd, S, O):
    return S*(P/(P+Kd))+O

def quad(P, Kd, S, O, L): # in this form, L refers to the ligand held at constant concentration
    a = P+L+Kd
    return S*((a-(((a**2)-(4*P*L))**0.5))/(2*L))+O
    # return S*(((P+L+Kd)-((((P+L+Kd)**2)-(4*P*L))**0.5))/(2*L))+O

def hill(P, Kd, S, O, n):
    return	S*((P**(n)/((P**(n)+(Kd**(n))))))+O

def multi(P, Kd, Kd2, S, S2, O):
    return (S*(P/(Kd+P))+S2*(P/(Kd2+P)))+O


def r_squared(y, residuals):
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y-np.mean(y))**2)
    r_sq = 1-(ss_res/ss_tot)
    return r_sq

def normalize_y(y, S, O):
    return (y - O) / S


def get_simple_fit(x, y, units, fit_dict, **kwargs):

    fit_params = {}

    p0 = [
        fit_dict["Kdi"],
        fit_dict["Si"],
        fit_dict["Oi"]
    ]

    popt, _ = opt.curve_fit(simplified, x, y, p0=p0, bounds=((0,0,0),(np.inf,np.inf,np.inf)))

    x_fit = np.geomspace(x[-1], x[0], 50)
    y_fit = simplified(x_fit, *popt)

    # popt[1] is S, popt[2] is O
    # y_norm = (y - popt[2]) / popt[1]
    y_norm = [normalize_y(yi, popt[1], popt[2]) for yi in y]
    y_fit_norm = [normalize_y(yi, popt[1], popt[2]) for yi in y_fit]

    #calculate R-squared
    residuals = y - simplified(x, *popt)
    r_sq = r_squared(y, residuals)

    fit_params[f"Kd ({units})"] = str(round(popt[0],2))
    fit_params["S"] = str(round(popt[1],4))
    fit_params["O"] = str(round(popt[2],4))
    fit_params["R^2"] = str(round(r_sq,4))

    return x_fit, y_fit, y_norm, y_fit_norm, fit_params


def get_quad_fit(x, y, units, fit_dict, ligand_conc=None, **kwargs):

    fit_params = {}

    p0 = [
        fit_dict["Kdi"],
        fit_dict["Si"],
        fit_dict["Oi"]
    ]

    quad_lambda = lambda P, Kd, S, O: quad(P, Kd, S, O, ligand_conc)

    popt, _ = opt.curve_fit(quad_lambda, x, y, p0=p0, bounds=((0,0,0),(np.inf,np.inf,np.inf)))

    x_fit = np.geomspace(x[-1], x[0], 50)
    y_fit = quad(x_fit, popt[0], popt[1], popt[2], ligand_conc)

    # popt[1] is S, popt[2] is O
    # y_norm = (y - popt[2]) / popt[1]
    y_norm = [normalize_y(yi, popt[1], popt[2]) for yi in y]
    y_fit_norm = [normalize_y(yi, popt[1], popt[2]) for yi in y_fit]

    #calculate R-squared
    # TODO: Error here
        # a = P+L+Kd
        # TypeError: can only concatenate list (not "int") to list
    residuals = y - quad(x, popt[0], popt[1], popt[2], ligand_conc)
    r_sq = r_squared(y, residuals)

    fit_params[f"Kd ({units})"] = str(round(popt[0],2))
    fit_params["S"] = str(round(popt[1],4))
    fit_params["O"] = str(round(popt[2],4))
    fit_params["R^2"] = str(round(r_sq,4))

    return x_fit, y_fit, y_norm, y_fit_norm, fit_params

def get_hill_fit(x, y, units, fit_dict, **kwargs):

    fit_params = {}

    p0 = [
        fit_dict["Kdi"],
        fit_dict["Si"],
        fit_dict["Oi"],
        fit_dict["ni"]
    ]

    popt, _ = opt.curve_fit(hill, x, y, p0=p0, bounds=((0,0,0,0),(np.inf,np.inf,np.inf,np.inf)))

    x_fit = np.geomspace(x[-1], x[0], 50)
    y_fit = hill(x_fit, *popt)

    # popt[1] is S, popt[2] is O
    # y_norm = (y - popt[2]) / popt[1]
    y_norm = [normalize_y(yi, popt[1], popt[2]) for yi in y]
    y_fit_norm = [normalize_y(yi, popt[1], popt[2]) for yi in y_fit]

    #calculate R-squared
    residuals = y - hill(x, *popt)
    r_sq = r_squared(y, residuals)

    fit_params[f"Kd ({units})"] = str(round(popt[0],2))
    fit_params["n"] = str(round(popt[3],2))
    fit_params["S"] = str(round(popt[1],4))
    fit_params["O"] = str(round(popt[2],4))
    fit_params["R^2"] = str(round(r_sq,4))

    return x_fit, y_fit, y_norm, y_fit_norm, fit_params

def get_multi_fit(x, y, units, fit_dict, **kwargs):

    fit_params = {}

    p0 = [
        fit_dict["Kdi"],
        fit_dict["Kd2i"],
        fit_dict["Si"],
        fit_dict["S2i"],
        fit_dict["Oi"]
    ]

    popt, _ = opt.curve_fit(multi, x, y, p0=p0, bounds=((0,0,0,0,0),(np.inf,np.inf,np.inf,np.inf,np.inf)))

    x_fit = np.geomspace(x[-1], x[0], 50)
    y_fit = multi(x_fit, *popt)

    # popt[2] is S, popt[3] is S2, popt[4] is O
    # y_norm = (y - popt[4]) / (popt[2] + popt[3])
    y_norm = [normalize_y(yi, (popt[2] + popt[3]), popt[4]) for yi in y]
    y_fit_norm = [normalize_y(yi, (popt[2] + popt[3]), popt[4]) for yi in y_fit]

    #calculate R-squared
    residuals = y - multi(x, *popt)
    r_sq = r_squared(y, residuals)

    fit_params[f"Kd ({units})"] = str(round(popt[0],2))
    fit_params[f"Kd2 ({units})"] = str(round(popt[1],2))
    fit_params["S"] = str(round(popt[2],4))
    fit_params["S2"] = str(round(popt[3],4))
    fit_params["O"] = str(round(popt[4],4))
    fit_params["R^2"] = str(round(r_sq,4))

    return x_fit, y_fit, y_norm, y_fit_norm, fit_params