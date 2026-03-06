import pandas as pd
import sxs
from sxs.julia import PNWaveform
import numpy as np
from scipy.signal import savgol_filter 
import json 
from tqdm import tqdm


#-----------------------------------------------------------------------------------------------------

def h_minus(h, l, m):
    '''
    anti-symmetric waveform definition
    '''
    return (h[(l,m)] - (-1)**l * np.conjugate(h[(l,-m)]))/2


#-----------------------------------------------------------------------------------------------------


def h_plus(h, l, m):
    '''
    symmetric waveform definition
    '''
    return (h[(l,m)] + (-1)**l * np.conjugate(h[(l,-m)]))/2


#-----------------------------------------------------------------------------------------------------


def phi_minus(h, l, m):
    '''
    Returns the phase of the anti-symmetric waveform 
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    phi_minus = np.unwrap(np.angle(h_minus(h, l, m)))
    return phi_minus 


#-----------------------------------------------------------------------------------------------------


def phi_plus(h, l, m):
    '''
    Returns the phase of the symmetric waveform 
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''
    phi_plus = np.unwrap(np.angle(h_plus(h, l, m)))
    return phi_plus 


#----------------------------------------------------------------------------------------------------- 


def orbital_phase_PN(q, chi1, chi2, omega_ref):

    m1 = q/(1 + q)
    m2 = 1/(1 + q)
    wf = PNWaveform(m1, m2, chi1, chi2, omega_ref)

    return wf.t, wf.orbital_phase


#----------------------------------------------------------------------------------------------------- 


def h_copr_from_PN(q, chi1, chi2, omega_ref):

    # create sxs PN object 
    m1 = q/(1 + q)
    m2 = 1/(1 + q)
    wf = PNWaveform(m1, m2, chi1, chi2, omega_ref)
    wf_interpolated = wf.interpolate(np.arange(wf.t[0], wf.t[-1], 1))

    # frame transformation and mode dict building
    wf_copr = wf_interpolated.to_coprecessing_frame()
    data_copr = wf_copr.data.T 
    mode_list = [(ell,m) for ell in range(wf.ell_min, wf.ell_max + 1) for m in range(-ell,ell+1)]
    h_copr = dict(zip(mode_list, data_copr))

    return wf_copr.t, h_copr


#-----------------------------------------------------------------------------------------------------


# random samples in parameter space
N = 2**12
qs = np.random.uniform(1, 10, N)
a1s = np.random.uniform(0, 0.99, N)
theta1s = np.random.uniform(0, np.pi, N)
phi1s = np.random.uniform(0, 2*np.pi, N)
a2s = np.random.uniform(0, 0.99, N)
theta2s = np.random.uniform(0, np.pi, N)
phi2s = np.random.uniform(0, 2*np.pi, N)
omega_ref = 0.01


#-----------------------------------------------------------------------------------------------------


# main loop
ell_min = 2
ell_max = 8
mode_list_m_pos = [(ell,m) for ell in range(ell_min, ell_max + 1) for m in range(0, ell+1)]

magic_factors_from_omega_a = []
magic_factors_from_omega_s = []

for i in tqdm(range(N)):

    # get time, mode dict and phi_orb
    q = qs[i]
    chi1x = a1s[i] * np.sin(theta1s[i]) * np.cos(phi1s[i])
    chi1y = a1s[i] * np.sin(theta1s[i]) * np.sin(phi1s[i])
    chi1z = a1s[i] * np.cos(theta1s[i])
    chi1 = [chi1x, chi1y, chi1z] 
    chi2x = a2s[i] * np.sin(theta2s[i]) * np.cos(phi2s[i])
    chi2y = a2s[i] * np.sin(theta2s[i]) * np.sin(phi2s[i])
    chi2z = a2s[i] * np.cos(theta2s[i])
    chi2 = [chi2x, chi2y, chi2z]
    time, h_copr = h_copr_from_PN(q, chi1, chi2, omega_ref)
    t_phi_orb, phi_orb = orbital_phase_PN(q, chi1, chi2, omega_ref)
    phi_orb_dot = np.gradient(-phi_orb, t_phi_orb)
    phi_orb_dot = np.interp(time, t_phi_orb, phi_orb_dot)
    
    # cut time
    t_left = time[0] + 1000
    t_right = time[-1] - 1000 
    idx_cut_left = np.argmin(np.abs(time - t_left))
    idx_cut_right = np.argmin(np.abs(time - t_right))

    mf_realization_from_omega_a = []
    mf_realization_from_omega_s = []

    for mode in mode_list_m_pos:
    
        # prepare phase and omega
        l, m = mode
        phi_a = phi_minus(h_copr, l, m)
        phi_a_dot = np.gradient(phi_a, time)
        phi_a_dot_savgol = savgol_filter(phi_a_dot, int(len(phi_a_dot)/20), 3)
        phi_s = phi_plus(h_copr, l, m)
        phi_s_dot = np.gradient(phi_s, time)
        phi_s_dot_savgol = savgol_filter(phi_s_dot, int(len(phi_s_dot)/20), 3)

        # get median value 
        mf_a = np.median(phi_a_dot_savgol[idx_cut_left:idx_cut_right]/phi_orb_dot[idx_cut_left:idx_cut_right])
        mf_realization_from_omega_a.append(mf_a)
        mf_s = np.median(phi_s_dot_savgol[idx_cut_left:idx_cut_right]/phi_orb_dot[idx_cut_left:idx_cut_right])
        mf_realization_from_omega_s.append(mf_s)
    
    magic_factors_from_omega_a.append(mf_realization_from_omega_a)
    magic_factors_from_omega_s.append(mf_realization_from_omega_s)

#-----------------------------------------------------------------------------------------------------  

# save data
data = {'magic_factors_from_omega_s' : magic_factors_from_omega_s,
        'magic_factors_from_omega_a' : magic_factors_from_omega_a, 
        'mode_list_m_pos' : mode_list_m_pos}                   


with open('mf_data.json', 'w') as outfile:
    json.dump(data, outfile)

#-----------------------------------------------------------------------------------------------------  

print('magic factors ready')

