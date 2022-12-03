import time
from webbrowser import get

def pressure_slope_is_dangerous(p_slope, threshold):    #TODO: Change this name for clarify
    if p_slope <= threshold:
        return True
    else:
        return False

def get_pressure_slope(current_p, previous_p, current_t, previous_t):
    return (current_p - previous_p)/(current_t - previous_t)

def pressure_validation(current_p, previous_p, current_t, previous_t, p_warn_treshold, p_emerg_threshold, p_slope_warn_threshold, p_slope_emerg_threshold):
    #Check if current absolute value is below p_threshold
    if current_p <= p_emerg_threshold:
        return 1
    elif current_p <= p_warn_treshold:
        return 2

    p_slope = get_pressure_slope(current_p, previous_p, current_t, previous_t)
    if p_slope <= p_slope_emerg_threshold:
        return 3
    elif p_slope <= p_slope_warn_threshold:
        return 4

    #if not yet returned, then pressure is okay!
    return 0

#Return pressure validation results:
'''
0 - Pass
1 - absolute_emergency
2 - absolute_warning
3 - slope_emergency
4 - slope_warning
'''
#TODO: Handle fail read cases.
