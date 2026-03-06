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


def get_metadata(sxs_id):

    sxs_bbh = sxs.load(sxs_id)
    chi1 = sxs_bbh.metadata.reference_dimensionless_spin1
    chi2 = sxs_bbh.metadata.reference_dimensionless_spin2
    m1 = sxs_bbh.metadata.reference_mass1
    m2 = sxs_bbh.metadata.reference_mass2
    omega_ref = np.linalg.norm(sxs_bbh.metadata.reference_orbital_frequency)

    return m1, m2, chi1, chi2, omega_ref


#-----------------------------------------------------------------------------------------------------


def to_mode_dict(wf):

    data = wf.data.T
    mode_list = [(ell, m) for ell in range(wf.ell_min, wf.ell_max + 1)
                          for m in range(-ell, ell + 1)]
    
    return dict(zip(mode_list, data))


#-----------------------------------------------------------------------------------------------------


def orbital_phase_PN(sxs_id):

    m1, m2, chi1, chi2, omega_ref = get_metadata(sxs_id)
    wf = PNWaveform(m1, m2, chi1, chi2, omega_ref)

    return wf.t, wf.orbital_phase


#----------------------------------------------------------------------------------------------------- 



def h_copr_from_PN(sxs_id):

    m1, m2, chi1, chi2, omega_ref = get_metadata(sxs_id)
    wf = PNWaveform(m1, m2, chi1, chi2, omega_ref)
    wf_interp = wf.interpolate(np.arange(wf.t[0], wf.t[-1], 1))
    wf_copr = wf_interp.to_coprecessing_frame()

    return wf_copr.t, to_mode_dict(wf_copr)


#-----------------------------------------------------------------------------------------------------


# get sxs catalog with specific values

dataframe = sxs.load("dataframe", tag="3.0.0")
BHBH = dataframe[(dataframe["object_types"] == "BHBH") 
                   & (dataframe["reference_eccentricity"] < 1e-3)
                   & (dataframe["reference_chi1_perp"] + dataframe["reference_chi2_perp"] >= 1e-3)
                   & (dataframe['deprecated'] == False)]


#-----------------------------------------------------------------------------------------------------


# main loop
ell_min = 2
ell_max = 8
mode_list_m_pos = [(ell,m) for ell in range(ell_min, ell_max + 1) for m in range(1,ell+1)]

magic_factors_minus = []
magic_factors_plus = []

for i in tqdm(range(len(BHBH))):

    # get time, mode dict and orbital phase derivative
    sxs_id = BHBH.index[i]
    time, h_copr = h_copr_from_PN(sxs_id)
    t_phi_orb, phi_orb = orbital_phase_PN(sxs_id)
    phi_orb_dot = np.gradient(-phi_orb, t_phi_orb)
    phi_orb_dot = np.interp(time, t_phi_orb, phi_orb_dot)
    
    # cut time
    t_left = time[0] + 1000
    t_right = time[-1] - 1000 
    idx_cut_left = np.argmin(np.abs(time - t_left))
    idx_cut_right = np.argmin(np.abs(time - t_right))

    mf_realization_minus = []
    mf_realization_plus = []

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
        mf_realization_minus.append(mf_a)
        mf_s = np.median(phi_s_dot_savgol[idx_cut_left:idx_cut_right]/phi_orb_dot[idx_cut_left:idx_cut_right])
        mf_realization_plus.append(mf_s)
    
    magic_factors_minus.append(mf_realization_minus)
    magic_factors_plus.append(mf_realization_plus)

#-----------------------------------------------------------------------------------------------------  

# save data
data = {'magic_factors_plus' : magic_factors_plus,
        'magic_factors_minus' : magic_factors_minus, 
        'mode_list_m_pos' : mode_list_m_pos}                   


with open('mf_data.json', 'w') as outfile:
    json.dump(data, outfile)

#-----------------------------------------------------------------------------------------------------  

print('magic factors ready')

