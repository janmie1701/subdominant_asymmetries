import numpy as np
from scipy.integrate import simpson
import gwsurrogate as gws
import scri
import json 
from tqdm import tqdm

#-----------------------------------------------------------------------------------------------------

# define surrogate model
sur = gws.LoadSurrogate('NRSur7dq4')

#-----------------------------------------------------------------------------------------------------

def ampl_minus(h, ell_min, ell_max):
    '''
    amplitude of the total antisymmetric waveform
    '''
    h_minus = np.zeros(len(h[(ell_max, ell_max)]), dtype=complex)
    for l in range(ell_min, ell_max+1):
        for m in range(0, l+1):
            h_minus_lm = (h[(l,m)] - (-1)**l * np.conjugate(h[(l,-m)]))/2
            h_minus += h_minus_lm

    return np.abs(h_minus)

#-----------------------------------------------------------------------------------------------------

def main_asym_kick(t, h, ell_min, ell_max):
    '''
    Transforms a strain in the inertial frame into the coprecessing frame 
    and gives the kick calculated in the coprecessing frame.
    t:       time array (arr)
    h:       dictionary of available modes with (l, m) tuples as keys in inertial frame (dict)
    '''
    
    # available modes
    mode_list = [(ell,m) for ell in range(ell_min, ell_max+1) for m in range(-ell,ell+1)]

    # build scri WaveformModes object
    data = list(h.values())
    data = np.array(data).T
    waveform_modes = scri.WaveformModes(
                            dataType=scri.h,
                            t=t,
                            data=data,
                            ell_min=ell_min,
                            ell_max=ell_max,
                            frameType=scri.Inertial,
                            r_is_scaled_out=True,
                            m_is_scaled_out=True,
                            )                      
    
    # asyms and kick in copr frame
    waveform_modes.to_coprecessing_frame()
    data_copr = waveform_modes.data.T
    h_copr = dict(zip(mode_list, data_copr))
    momentum_flux_copr = waveform_modes.momentum_flux()
    vz_copr = -simpson(momentum_flux_copr[:,2], dx=dt) 
    max_copr_minus = np.max(ampl_minus(h_copr, ell_min, ell_max))
        
    return h_copr, vz_copr, max_copr_minus

#-----------------------------------------------------------------------------------------------------

def h_dict_22_only(h, ell_min, ell_max):

    mode_list = [(ell,m) for ell in range(ell_min, ell_max+1) for m in range(-ell, ell+1)]
    h_only_22 = h
    for mode in mode_list:
        if mode == (2,2) or mode==(2,-2):
            continue
        else:
            l, m = mode
            h_only_22[mode] = (h[l,m] + (-1)**l * np.conjugate(h[(l,-m)]))/2
            
    return h_only_22
    
#-----------------------------------------------------------------------------------------------------    

def get_kick_with_22_modes(t, h, ell_min, ell_max, frameType):

    h_only_22 = h_dict_22_only(h, ell_min, ell_max)
        
    data = list(h_only_22.values())
    data = np.array(data).T

    waveform_modes = scri.WaveformModes(
                            dataType=scri.h,
                            t=t,
                            data=data,
                            ell_min=ell_min,
                            ell_max=ell_max,
                            frameType=frameType,
                            r_is_scaled_out=True,
                            m_is_scaled_out=True,
                            ) 

    momentum_flux_only_22 = waveform_modes.momentum_flux()
    vz_22 = -simpson(momentum_flux_only_22[:,2], dx=dt)
    
    return vz_22

#-----------------------------------------------------------------------------------------------------

# fixed parameters
q = 3                               
a = 0.8                               
dt = 0.1                    
ell_min = 2
ell_max = 4
f_low = 0   
f_ref = 6**(-3/2)/np.pi  
omega0 = f_ref*np.pi

#-----------------------------------------------------------------------------------------------------
  
n_theta1 = 2**4 +1
n_phi1 = 2**5 +1
n_theta2 = 2**4 +1
n_phi2 = 2*5 +1
total_iterations = n_theta1*n_phi1*n_theta2*n_phi2

# spin direction grid
theta1 = np.linspace(0, np.pi, n_theta1)
phi1 = np.linspace(0, 2*np.pi, n_phi1)
theta2 = np.linspace(0, np.pi, n_theta2)
phi2 = np.linspace(0, 2*np.pi, n_phi2)

THETA1, PHI1, THETA2, PHI2 = np.meshgrid(theta1, phi1, theta2, phi2, indexing='ij') 
  
#-----------------------------------------------------------------------------------------------------

# main loop

vs_all_modes_copr = np.zeros(total_iterations)
vs_22_modes_copr = np.zeros(total_iterations)
max_minus_copr = np.zeros(total_iterations)
j = 0

for i in tqdm(np.ndindex(n_theta1, n_phi1, n_theta2, n_phi2), 
              total=total_iterations):
                
    # spin BH1 
    theta1 = THETA1[i]
    phi1 = PHI1[i]
    chi1x = a * np.sin(theta1) * np.cos(phi1)
    chi1y = a * np.sin(theta1) * np.sin(phi1)
    chi1z = a * np.cos(theta1)
    chi1 = [chi1x, chi1y, chi1z]

    # spin BH12
    theta2 = THETA2[i]
    phi2 = PHI2[i]
    chi2x = a * np.sin(theta2) * np.cos(phi2)
    chi2y = a * np.sin(theta2) * np.sin(phi2)
    chi2z = a * np.cos(theta2)
    chi2 = [chi2x, chi2y, chi2z]
    
    # anti-symmetric waveform peak and kicks from coprecessing with all modes
    t, h_iner, dyn = sur(q, chi1, chi2, dt=dt, f_low=f_low, f_ref=f_ref)
    h_copr, vz_copr, max_copr_minus = main_asym_kick(t, h_iner, ell_min, ell_max)
    max_minus_copr[j] = max_copr_minus
    vs_all_modes_copr[j] = vz_copr
    
    # dominat modes only
    vz_22_copr = get_kick_with_22_modes(t, h_copr, ell_min, ell_max, scri.Coprecessing)
    vs_22_modes_copr[j] = vz_22_copr

    j += 1


#-----------------------------------------------------------------------------------------------------  


data = {'THETA1': THETA1.tolist(), 
        'PHI1': PHI1.tolist(),
        'THETA2': THETA2.tolist(), 
        'PHI2': PHI2.tolist(),
        'vs_all_modes_copr' : vs_all_modes_copr.tolist(),
        'vs_22_modes_copr' : vs_22_modes_copr.tolist(),
        'max_minus_copr': max_minus_copr.tolist(),
        'q': q,
        'a': a,
        'chi2': chi2,
        'dt': dt,
        'ell_min': ell_min,
	    'ell_max': ell_max,
	    'f_low': f_low,
	    'omega0': omega0,
	    'f_ref': f_ref,      
        'n_theta1': n_theta1, 
        'n_phi1': n_phi1, 
        'n_theta2': n_theta2, 
        'n_phi2': n_phi2}                   


with open('dolphin_data.json', 'w') as outfile:
    json.dump(data, outfile)

#-----------------------------------------------------------------------------------------------------  

print('dolphin ready')
 
