# Fitting equations and functions

import scipy.optimize as opt
import numpy as np


def simplified(P, Kd, S, offset):
    return S * (P / (P + Kd)) + offset


def quad(P, Kd, S, offset, L):
    # L is ligand held at constant concentration
    a = P + L + Kd
    return S * ((a - (((a**2) - (4 * P * L)) ** 0.5)) / (2 * L)) + offset


def hill(P, Kd, S, offset, n):
    return S * ((P ** (n) / ((P ** (n) + (Kd ** (n)))))) + offset


def multi(P, Kd, Kd2, S, S2, offset):
    return (S * (P / (Kd + P)) + S2 * (P / (Kd2 + P))) + offset


def r_squared(y, residuals):
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - (ss_res / ss_tot)


def normalize_y(y, S, offset):
    return (y - offset) / S


def _run_fit(fn, x, y, p0):
    """Run curve_fit and return fit results common to all fit types."""
    bounds = ((0,) * len(p0), (np.inf,) * len(p0))
    popt, _ = opt.curve_fit(fn, x, y, p0=p0, bounds=bounds)
    x_fit = np.geomspace(x[-1], x[0], 50)
    y_fit = fn(x_fit, *popt)
    residuals = np.array(y) - fn(np.array(x), *popt)
    return x_fit, y_fit, popt, r_squared(y, residuals)


def get_simple_fit(x, y, units, fit_dict, **kwargs):
    p0 = [fit_dict["Kdi"], fit_dict["Si"], fit_dict["Oi"]]
    x_fit, y_fit, popt, r_sq = _run_fit(simplified, x, y, p0)
    Kd, S, offset = popt
    y_norm     = [normalize_y(yi, S, offset) for yi in y]
    y_fit_norm = [normalize_y(yi, S, offset) for yi in y_fit]
    return x_fit, y_fit, y_norm, y_fit_norm, {
        f"Kd ({units})": str(round(Kd, 2)),
        "S": str(round(S, 4)), "O": str(round(offset, 4)),
        "R^2": str(round(r_sq, 4)),
    }


def get_quad_fit(x, y, units, fit_dict, ligand_conc, **kwargs):
    p0 = [fit_dict["Kdi"], fit_dict["Si"], fit_dict["Oi"]]

    def fn(P, Kd, S, offset):
        return quad(P, Kd, S, offset, ligand_conc)

    x_fit, y_fit, popt, r_sq = _run_fit(fn, x, y, p0)
    Kd, S, offset = popt
    y_norm     = [normalize_y(yi, S, offset) for yi in y]
    y_fit_norm = [normalize_y(yi, S, offset) for yi in y_fit]
    return x_fit, y_fit, y_norm, y_fit_norm, {
        f"Kd ({units})": str(round(Kd, 2)),
        "S": str(round(S, 4)), "O": str(round(offset, 4)),
        "R^2": str(round(r_sq, 4)),
    }


def get_hill_fit(x, y, units, fit_dict, **kwargs):
    p0 = [fit_dict["Kdi"], fit_dict["Si"], fit_dict["Oi"], fit_dict["ni"]]
    x_fit, y_fit, popt, r_sq = _run_fit(hill, x, y, p0)
    Kd, S, offset, n = popt
    y_norm     = [normalize_y(yi, S, offset) for yi in y]
    y_fit_norm = [normalize_y(yi, S, offset) for yi in y_fit]
    return x_fit, y_fit, y_norm, y_fit_norm, {
        f"Kd ({units})": str(round(Kd, 2)), "n": str(round(n, 2)),
        "S": str(round(S, 4)), "O": str(round(offset, 4)),
        "R^2": str(round(r_sq, 4)),
    }


def get_multi_fit(x, y, units, fit_dict, **kwargs):
    p0 = [fit_dict["Kdi"], fit_dict["Kd2i"], fit_dict["Si"], fit_dict["S2i"], fit_dict["Oi"]]
    x_fit, y_fit, popt, r_sq = _run_fit(multi, x, y, p0)
    Kd, Kd2, S, S2, offset = popt
    y_norm     = [normalize_y(yi, S + S2, offset) for yi in y]
    y_fit_norm = [normalize_y(yi, S + S2, offset) for yi in y_fit]
    return x_fit, y_fit, y_norm, y_fit_norm, {
        f"Kd ({units})": str(round(Kd, 2)), f"Kd2 ({units})": str(round(Kd2, 2)),
        "S": str(round(S, 4)), "S2": str(round(S2, 4)), "O": str(round(offset, 4)),
        "R^2": str(round(r_sq, 4)),
    }
