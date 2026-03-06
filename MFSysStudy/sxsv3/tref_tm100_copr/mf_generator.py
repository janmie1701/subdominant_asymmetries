import pandas as pd
import sxs
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


def phi_dot(h, t, l, m, phi_type):
    '''
    Returns the phase derivative of the anti-symmetric (minus)
    or symmetric (plus) (l,m) mode
    h:  mode dictionary with (l, m) tuples as keys (dict)
    l:  greater equal 2 (int) 
    m:  greater equal 1 less equal l (int)
    '''

    if phi_type == 'plus':
        phi = np.unwrap(np.angle(h_plus(h, l, m)))
    elif phi_type == 'minus':
        phi = np.unwrap(np.angle(h_minus(h, l, m))) 
    else:
        raise ValueError("phi_type must be 'plus' or 'minus'")
    
    phi_dot = np.gradient(phi, t) 
    phi_dot_savgol = savgol_filter(phi_dot, int(len(phi_dot)/20), 3)

    return phi_dot_savgol


#-----------------------------------------------------------------------------------------------------


def h_copr_from_sxs(sxs_id):

    # load sxs waveform object with truncation of junk and time shift
    sxs_bbh = sxs.load(sxs_id, ignore_deprecation=True)
    wf = sxs_bbh.h
    time = wf.t 
    t_peak = wf.max_norm_time()
    t_ref = sxs_bbh.metadata.reference_time 
    idx_ref = wf.index_closest_to(t_ref) 
    wf = wf[idx_ref:]
    time = time[idx_ref:] - t_peak

    # frame transformation and mode dict building
    wf_copr = wf.to_coprecessing_frame()
    data_copr = wf_copr.data.T 
    mode_list = [(ell,m) for ell in range(wf.ell_min, wf.ell_max + 1) for m in range(-ell,ell+1)]
    h_copr = dict(zip(mode_list, data_copr))

    return time, h_copr 


#-----------------------------------------------------------------------------------------------------


# get sxs catalog with specific values

dataframe = sxs.load("dataframe", tag="3.0.0")
BHBH = dataframe[(dataframe["object_types"] == "BHBH") 
                   & (dataframe["reference_eccentricity"] < 1e-3)
                   & (dataframe["reference_chi1_perp"] + dataframe["reference_chi2_perp"] >= 1e-3)
                   & (dataframe['deprecated'] == False)]


#-----------------------------------------------------------------------------------------------------


# main loop

t_max = -100
ell_min = 2
ell_max = 8
mode_list_m_pos = [(ell,m) for ell in range(ell_min, ell_max + 1) for m in range(0, ell+1)]

magic_factors_minus = np.zeros((len(BHBH), len(mode_list_m_pos)))
magic_factors_plus = np.zeros((len(BHBH), len(mode_list_m_pos)))

for i in tqdm(range(len(BHBH))):

    # get time, mode dict and orbital phase derivative
    sxs_id = BHBH.index[i]
    time, h_copr = h_copr_from_sxs(sxs_id)
    phi_orb = - 1/4 * (np.unwrap(np.angle(h_copr[(2,-2)])) - np.unwrap(np.angle(h_copr[(2,2)]))) 
    phi_orb_dot = np.gradient(phi_orb, time)
    
    # window (full inspiral time up to a few cycles before merger)
    idx_max = np.argmin(np.abs(time - t_max))

    mf_realization_minus = np.zeros(len(mode_list_m_pos))
    mf_realization_plus = np.zeros(len(mode_list_m_pos))

    for mode in mode_list_m_pos:
    
        # prepare phase and omega
        l, m = mode
        phi_minus_dot = phi_dot(h_copr, time, l, m, 'minus')
        phi_plus_dot = phi_dot(h_copr, time, l, m, 'plus')

        # get median value 
        mf_minus = np.median(phi_minus_dot[:idx_max] / phi_orb_dot[:idx_max])
        mf_realization_minus[mode_list_m_pos.index(mode)] = mf_minus
        mf_plus = np.median(phi_plus_dot[:idx_max] / phi_orb_dot[:idx_max])
        mf_realization_plus[mode_list_m_pos.index(mode)] = mf_plus
    
    magic_factors_minus[i] = mf_realization_minus
    magic_factors_plus[i] = mf_realization_plus


#-----------------------------------------------------------------------------------------------------  


# save data

data = {'magic_factors_plus' : magic_factors_plus.tolist(),
        'magic_factors_minus' : magic_factors_minus.tolist(), 
        'mode_list_m_pos' : mode_list_m_pos}                   


with open('mf_data.json', 'w') as outfile:
    json.dump(data, outfile)


#-----------------------------------------------------------------------------------------------------  


print('magic factors ready')

