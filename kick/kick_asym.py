'''
Description:
This script contains various functions to calculate the +/- waveform and kick information from it. 
Waveforms with mode dictionaries are required. Based on https://arxiv.org/abs/2412.06913

Usage:
Make sure you have downloaded all modules in your environment and
save this script in a folder of your choose and import in a Jupyter notebook via
    import sys
    sys.path.append('~/subdominant_asymmetries/')
    from kick_asym import *

Author:
Jannik Mielke
Max Planck Institute for Gravitational Physics (Albert Einstein Institute)
jannik.mielke@aei.mpg.de

'''


#-----------------------------------------------------------------------------------------------------


import numpy as np
from scipy.interpolate import CubicSpline


#-----------------------------------------------------------------------------------------------------


def interpolate(y, t):

    spline = CubicSpline(t, y)
    y_interp = spline(t)

    return y_interp


#-----------------------------------------------------------------------------------------------------


def deriv(y, t, order=1):

    spline = CubicSpline(t, y)
    ydot = spline(t, nu=order)  

    return ydot


#-----------------------------------------------------------------------------------------------------


def h_minus(h, t, l, m):
    '''
    Returns the anti-symmetric waveform 
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    return (h[(l,m)] - (-1)**l * np.conjugate(h[(l,-m)]))/2


#-----------------------------------------------------------------------------------------------------


def a_minus(h, t, l, m):
    '''
    Returns the amplitude of the anti-symmetric waveform
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    a = np.abs(h_minus(h, t, l, m)) 
    return interpolate(a, t)


#-----------------------------------------------------------------------------------------------------


def a_minus_dot(h, t, l, m):
    '''
    Returns the amplitude derivative of the anti-symmetric waveform
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    a = a_minus(h, t, l, m)
    return deriv(a, t)


#-----------------------------------------------------------------------------------------------------


def phi_minus(h, t, l, m):
    '''
    Returns the phase of the anti-symmetric waveform 
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    phi = np.unwrap(np.angle(h_minus(h, t, l, m)))
    return interpolate(phi, t)


#-----------------------------------------------------------------------------------------------------


def phi_minus_dot(h, t, l, m):
    '''
    Returns the phase derivative of the anti-symmetric waveform
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    phi = phi_minus(h, t, l, m)
    return deriv(phi, t)


#-----------------------------------------------------------------------------------------------------

    
def h_plus(h, t, l, m):
    '''
    Returns the symmetric waveform 
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    return (h[(l,m)] + (-1)**l * np.conjugate(h[(l,-m)]))/2    


#-----------------------------------------------------------------------------------------------------


def a_plus(h, t, l, m):
    '''
    Returns the amplitude of the symmetric waveform 
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    a = np.abs(h_plus(h, t, l, m)) 
    return interpolate(a, t)


#-----------------------------------------------------------------------------------------------------


def a_plus_dot(h, t, l, m):
    '''
    Returns the amplitude derivative of the symmetric waveform
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    a = a_plus(h, t, l, m)
    return deriv(a, t)


#-----------------------------------------------------------------------------------------------------


def phi_plus(h, t, l, m):
    '''
    Returns the phase of the symmetric waveform 
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    phi = np.unwrap(np.angle(h_plus(h, t, l, m))) 
    return interpolate(phi, t)


#-----------------------------------------------------------------------------------------------------


def phi_plus_dot(h, t, l, m):
    '''
    Returns the phase derivative of the symmetric waveform
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    phi = phi_plus(h, t, l, m)
    return deriv(phi, t) 


#-----------------------------------------------------------------------------------------------------


def c_lm(l, m):
    if np.abs(m) <= l:
        return 2*m/(l*(l+1))
    else:
        return 0


#-----------------------------------------------------------------------------------------------------


def d_lm(l, m):
    if np.abs(m) <= l:
        return np.sqrt((l-2)*(l+2)*(l-m)*(l+m)/((2*l-1)*(2*l+1)))/l
    else:
        return 0


#-----------------------------------------------------------------------------------------------------


def kron(m):
	if m == 0: 
		return 1
	else:
		return 0


#-----------------------------------------------------------------------------------------------------


def alpha(h, t, l_minus, m_minus, l_plus, m_plus): 
    return a_minus_dot(h, t, l_minus, m_minus)*a_plus_dot(h, t, l_plus, m_plus)


#-----------------------------------------------------------------------------------------------------


def beta(h, t, l_minus, m_minus, l_plus, m_plus):
    return a_minus(h, t, l_minus, m_minus)*a_plus(h, t, l_plus, m_plus)*phi_minus_dot(h, t, l_minus, m_minus)*phi_plus_dot(h, t, l_plus, m_plus)


#-----------------------------------------------------------------------------------------------------


def gamma(h, t, l_minus, m_minus, l_plus, m_plus):
    return -a_minus(h, t, l_minus, m_minus)*a_plus_dot(h, t, l_plus, m_plus)*phi_minus_dot(h, t, l_minus, m_minus)


#-----------------------------------------------------------------------------------------------------


def delta(h, t, l_minus, m_minus, l_plus, m_plus):
    return a_minus_dot(h, t, l_minus, m_minus)*a_plus(h, t, l_plus, m_plus)*phi_plus_dot(h, t, l_plus, m_plus)


#-----------------------------------------------------------------------------------------------------


def psi(h, t, l_minus, m_minus, l_plus, m_plus):
    return phi_minus(h, t, l_minus, m_minus) - phi_plus(h, t, l_plus, m_plus)
    
    
#----------------------------------------------------------------------------------------------------- 


def abcdp(h, t, l_minus, m_minus, l_plus, m_plus): 

    if (l_minus, m_minus) in h and (l_plus, m_plus) in h: 
        a = alpha(h, t, l_minus, m_minus, l_plus, m_plus) 
        b = beta(h, t, l_minus, m_minus, l_plus, m_plus) 
        c = gamma(h, t, l_minus, m_minus, l_plus, m_plus) 
        d = delta(h, t, l_minus, m_minus, l_plus, m_plus) 
        p = psi(h, t, l_minus, m_minus, l_plus, m_plus) 
    else :
        a = np.zeros(len(t))
        b = np.zeros(len(t))
        c = np.zeros(len(t))
        d = np.zeros(len(t))
        p = np.zeros(len(t))

    return a, b, c, d, p


#----------------------------------------------------------------------------------------------------- 


def abcdp_dicts(h, t, l_max):

    alpha_dict = {}
    beta_dict = {}
    gamma_dict = {}
    delta_dict = {}
    psi_dict = {} 

    for l in range(2, l_max+1):
        for m in range(0, l+1):

            # (l,m,l-1,m)  
            a, b, c, d, p = abcdp(h, t, l, m, l-1, m)
            alpha_dict[(l,m,l-1,m)] = a
            beta_dict[(l,m,l-1,m)] = b
            gamma_dict[(l,m,l-1,m)] = c
            delta_dict[(l,m,l-1,m)] = d
            psi_dict[(l,m,l-1,m)] = p 

            # (l,m,l,m)
            a, b, c, d, p = abcdp(h, t, l, m, l, m)
            alpha_dict[(l,m,l,m)] = a
            beta_dict[(l,m,l,m)] = b
            gamma_dict[(l,m,l,m)] = c
            delta_dict[(l,m,l,m)] = d
            psi_dict[(l,m,l,m)] = p 

            # (l,m,l+1,m) 
            a, b, c, d, p = abcdp(h, t, l, m, l+1, m)
            alpha_dict[(l,m,l+1,m)] = a
            beta_dict[(l,m,l+1,m)] = b
            gamma_dict[(l,m,l+1,m)] = c
            delta_dict[(l,m,l+1,m)] = d
            psi_dict[(l,m,l+1,m)] = p 

    return alpha_dict, beta_dict, gamma_dict, delta_dict, psi_dict 


#----------------------------------------------------------------------------------------------------- 


def omg(h, t, l_max): 

    alpha_dict, beta_dict, gamma_dict, delta_dict, psi_dict = abcdp_dicts(h, t, l_max+1)

    sum = np.zeros(len(t)) 
    for l in range(2, l_max+1):
        for m in range(0, l+1):
            sum += c_lm(l, m)*(alpha_dict[(l,m,l,m)] + beta_dict[(l,m,l,m)])*np.cos(psi_dict[(l,m,l,m)])*(1-.5*kron(m))
            sum += c_lm(l, m)*(gamma_dict[(l,m,l,m)] + delta_dict[(l,m,l,m)])*np.sin(psi_dict[(l,m,l,m)])*(1-.5*kron(m))
            sum += d_lm(l, m)*(alpha_dict[(l,m,l-1,m)] + beta_dict[(l,m,l-1,m)])*np.cos(psi_dict[(l,m,l-1,m)])*(1-.5*kron(m))
            sum += d_lm(l, m)*(gamma_dict[(l,m,l-1,m)] + delta_dict[(l,m,l-1,m)])*np.sin(psi_dict[(l,m,l-1,m)])*(1-.5*kron(m))
            sum += d_lm(l+1, m)*(alpha_dict[(l,m,l+1,m)] + beta_dict[(l,m,l+1,m)])*np.cos(psi_dict[(l,m,l+1,m)])*(1-.5*kron(m))
            sum += d_lm(l+1, m)*(gamma_dict[(l,m,l+1,m)] + delta_dict[(l,m,l+1,m)])*np.sin(psi_dict[(l,m,l+1,m)])*(1-.5*kron(m))

    dPzdt = sum/(4*np.pi)

    return dPzdt
