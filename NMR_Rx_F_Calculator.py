#Imported libraries
from math import log10, log2, ceil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sys import exit

#Constants
T0 = 290 #K

#Functions
def isfloat(value):
    '''Use to determine the possibility of converting chr argument value to float'''
    try:
        float(value)
        return True
    except ValueError:
        return False

def capitalize_only(string):
    '''Use to only capitalize the first letter of the input string
without changing the rest of the letters'''
    str_1 = string[0]
    str_2 = string[1:]
    string = str_1.capitalize() + str_2
    return string
    
def model_select(selection_object):
    '''Use for choosing one of two possible noise models'''
    good_input = 0
    while not good_input:
        message = 'Choose ' + selection_object + ': '
        model_no = input(message)
        if model_no.isnumeric():
            model_no=int(model_no)
            if model_no == 1 or model_no == 2:
                good_input = 1
            else:
                print('Input error! Try again.')
        else:
            print('Input error! Cannot convert input to integer! Try again.')
    return model_no

def init_selection():
    '''Use for choosing the appropriate one of two possible noise models and paths'''
    #Showing both models
    img = mpimg.imread('Models.png')
    plt.imshow(img)
    plt.axis('off')
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()
    #Choosing the model
    model = model_select('model (1 or 2)')
    #Showing both paths along with both models
    if model == 1:
        img = mpimg.imread('Model_1.png')
    else:
        img = mpimg.imread('Model_2.png')
    plt.imshow(img)
    plt.axis('off')
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.show()
    #Choosing the path
    path = model_select('path (in-->out = 1; out-->in = 2)')
    return model, path

def dB_input(input_term, sign):
    '''Use for input of the values expressed in decibels (dB)'''
    if sign == '+':
        good_input = 0
        while not good_input:
            message = 'Input ' + input_term + ' in dB: '
            value = input(message)
            if isfloat(value):
                value = float(value)
                if value >= 0:
                    good_input = 1
                else:
                    print('Input error! Try again.')
                    print('(', capitalize_only(input_term), ' has to be greater than or equal to zero dB!)', sep='')
            else:
                print('Input error! Cannot convert input to float! Try again.')
    elif sign == '-':
        good_input = 0
        while not good_input:
            message = 'Input ' + input_term + ' in dB: '
            value = input(message)
            if isfloat(value):
                value = float(value)
                if value < 0:
                    good_input = 1
                else:
                    print('Input error! Try again.')
                    print('(', capitalize_only(input_term), ' has to be less than zero dB!)', sep='')
            else:
                print('Input error! Cannot convert input to float! Try again.')
    elif sign == 'both':
        good_input = 0
        while not good_input:
            message = 'Input ' + input_term + ' in dB: '
            value = input(message)
            if isfloat(value):
                value = float(value)
                good_input = 1
            else:
                print('Input error! Cannot convert input to float! Try again.')
    else:
        print('Sign selection error! Fix that.')
        input('Press Enter to terminate the calculator...')
        exit()
    return value

def lin_pos_input(input_term):
    '''Use for input of the positive values in linear scale'''
    good_input = 0
    while not good_input:
        message = 'Input ' + input_term + ': '
        value = input(message)
        if isfloat(value):
            value = float(value)
            if value > 0:
                good_input = 1
            else:
                print('Input error! Try again.')
                print('(', capitalize_only(input_term), ' has to be greater than zero!)', sep='')
        else:
            print('Input error! Cannot convert input to float! Try again.')
    return value

def dB_2_lin(dB_value, ratio):
    '''Use to transform dB values to linear scale'''
    if ratio == 'power':
        lin_value = 10 ** (dB_value/10)
    elif ratio == 'voltage':
        lin_value = 10 ** (dB_value/20)
    else:
        print('Ratio selection error! Fix that.')
        input('Press Enter to terminate the calculator...')
        exit()
    return lin_value

def lin_2_dB(lin_value, ratio):
    '''Use to transform linear values to dB scale'''
    if ratio == 'power':
        dB_value = 10 * log10(lin_value)
    elif ratio == 'voltage':
        dB_value = 20 * log10(lin_value)
    else:
        print('Ratio selection error! Fix that.')
        input('Press Enter to terminate the calculator...')
        exit()
    return dB_value

def F11():
    '''Model: 1; Path: in --> out'''
    #Parameter input
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Parameter input~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    SNRin = dB_2_lin(dB_input('input signal-to-noise ratio', 'both'), 'power')
    Tcoil = lin_pos_input('coil temperature in K')
    L1 = dB_2_lin(dB_input('input cable loss', '+'), 'power')
    L2 = dB_2_lin(dB_input('duplexer loss', '+'), 'power')
    G3 = dB_2_lin(dB_input('pre-amplifier gain', '+'), 'power')
    F3 = dB_2_lin(dB_input('pre-amplifier noise factor', '+'), 'power')
    S11_3 = dB_2_lin(dB_input('pre-amplifier S11 parameter', '-'), 'voltage')
    L4 = dB_2_lin(dB_input('output cable loss', '+'), 'power')
    F5 = dB_2_lin(dB_input('NMR spectrometer RF receiver noise factor', '+'), 'power')
    n_meas = lin_pos_input('number of averaged measurements')
    #n_acq = lin_pos_input('number of acquisition points')
    #Calculation
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Calculated values~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    #Noise figure of hardware part of NMR spectroscopy Rx chain
    F_HW = 1 + ((2 * T0) / (Tcoil + T0)) * (L1 * L2 * (1 + (1 / (1 - (S11_3 ** 2))) * (F3 - 1 + ((L4 * F5 - 1) / G3))) - 1)
    print('Noise figure of the hardware part of NMR spectroscopy Rx chain:\n{:.4f} (linear scale) = {:.4f} dB\n'.format(F_HW, lin_2_dB(F_HW, 'power')))
    #Overall noise figure of NMR spectroscopy Rx chain
    #F11 = (F_HW / (n_meas * n_acq)) * 2
    F11 = F_HW / n_meas
    print('Overall noise figure of NMR spectroscopy system Rx chain:\n{:.4f} (linear scale) = {:.4f} dB\n'.format(F11, lin_2_dB(F11, 'power')))
    #Expected signal-to-noise ratio on the spectrometer screen
    SNRout = SNRin / F11
    print('Expected signal-to-noise ratio on the spectrometer screen:\n{:.4f} (linear scale; power ratio) = {:.4f} dB\n'.format(SNRout, lin_2_dB(SNRout, 'power')))
    return

def F12():
    '''Model: 1; Path: out --> in'''
    #Parameter input
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Parameter input~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    SNRout = dB_2_lin(dB_input('output signal-to-noise ratio\n(shown on the spectrometer screen)', 'both'), 'power')
    #n_acq = lin_pos_input('number of acquisition points')
    n_meas = lin_pos_input('number of averaged measurements')
    F5 = dB_2_lin(dB_input('NMR spectrometer RF receiver noise factor', '+'), 'power')
    L4 = dB_2_lin(dB_input('output cable loss', '+'), 'power')
    G3 = dB_2_lin(dB_input('pre-amplifier gain', '+'), 'power')
    F3 = dB_2_lin(dB_input('pre-amplifier noise factor', '+'), 'power')
    S11_3 = dB_2_lin(dB_input('pre-amplifier S11 parameter', '-'), 'voltage')
    L2 = dB_2_lin(dB_input('duplexer loss', '+'), 'power')
    L1 = dB_2_lin(dB_input('input cable loss', '+'), 'power')
    Tcoil = lin_pos_input('coil temperature in K')
    #Calculation
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Calculated values~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    #Noise figure of hardware part of NMR spectroscopy Rx chain
    F_HW = 1 + ((2 * T0) / (Tcoil + T0)) * (L1 * L2 * (1 + (1 / (1 - (S11_3 ** 2))) * (F3 - 1 + ((L4 * F5 - 1) / G3))) - 1)
    print('Noise figure of the hardware part of NMR spectroscopy Rx chain:\n{:.4f} (linear scale) = {:.4f} dB\n'.format(F_HW, lin_2_dB(F_HW, 'power')))
    #Overall noise figure of NMR spectroscopy Rx chain
    #F12 = (F_HW / (n_meas * n_acq)) * 2
    F12 = F_HW / n_meas
    print('Overall noise figure of NMR spectroscopy system Rx chain:\n{:.4f} (linear scale) = {:.4f} dB\n'.format(F12, lin_2_dB(F12, 'power')))
    #Expected signal-to-noise ratio on the probe
    SNRin = SNRout * F12
    print('Expected signal-to-noise ratio on the probe:\n{:.4f} (linear scale; power ratio) = {:.4f} dB\n'.format(SNRin, lin_2_dB(SNRin, 'power')))
    return

def F21():
    '''Model: 2; Path: in --> out'''
    #Parameter input
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Parameter input~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    SNRin = dB_2_lin(dB_input('input signal-to-noise ratio', 'both'), 'power')
    Tcoil = lin_pos_input('coil temperature in K')
    L1 = dB_2_lin(dB_input('input cable loss', '+'), 'power')
    L2 = dB_2_lin(dB_input('duplexer loss', '+'), 'power')
    G3 = dB_2_lin(dB_input('pre-amplifier gain', '+'), 'power')
    F3 = dB_2_lin(dB_input('pre-amplifier noise factor', '+'), 'power')
    S11_3 = dB_2_lin(dB_input('pre-amplifier S11 parameter', '-'), 'voltage')
    G3b = dB_2_lin(dB_input('second stage amplifier gain', '+'), 'power')
    F3b = dB_2_lin(dB_input('second stage amplifier noise factor', '+'), 'power')
    S11_3b = dB_2_lin(dB_input('second stage amplifier S11 parameter', '-'), 'voltage')
    L4 = dB_2_lin(dB_input('output cable loss', '+'), 'power')
    F5 = dB_2_lin(dB_input('NMR spectrometer RF receiver noise factor', '+'), 'power')
    n_meas = lin_pos_input('number of averaged measurements')
    #n_acq = lin_pos_input('number of acquisition points')
    #Calculation
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Calculated values~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    #Noise figure of hardware part of NMR spectroscopy Rx chain
    F_HW = 1 + ((2 * T0) / (Tcoil + T0)) * (L1 * L2 * (1 + (1 / (1 - (S11_3 ** 2))) * (F3 - 1 + (1 / (G3 * (1 - (S11_3b ** 2)))) * (F3b - 1 + ((L4 * F5 - 1) / G3b)))) - 1)
    print('Noise figure of the hardware part of NMR spectroscopy Rx chain:\n{:.4f} (linear scale) = {:.4f} dB\n'.format(F_HW, lin_2_dB(F_HW, 'power')))
    #Overall noise figure of NMR spectroscopy Rx chain
    #F21 = (F_HW / (n_meas * n_acq)) * 2
    F21 = F_HW / n_meas
    print('Overall noise figure of NMR spectroscopy system Rx chain:\n{:.4f} (linear scale) = {:.4f} dB\n'.format(F21, lin_2_dB(F21, 'power')))
    #Expected signal-to-noise ratio on the spectrometer screen
    SNRout = SNRin / F21
    print('Expected signal-to-noise ratio on the spectrometer screen:\n{:.4f} (linear scale; power ratio) = {:.4f} dB\n'.format(SNRout, lin_2_dB(SNRout, 'power')))
    return

def F22():
    '''Model: 2; Path: out --> in'''
    #Parameter input
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Parameter input~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    SNRout = dB_2_lin(dB_input('output signal-to-noise ratio\n(shown on the spectrometer screen)', 'both'), 'power')
    #n_acq = lin_pos_input('number of acquisition points')
    n_meas = lin_pos_input('number of averaged measurements')
    F5 = dB_2_lin(dB_input('NMR spectrometer RF receiver noise factor', '+'), 'power')
    L4 = dB_2_lin(dB_input('output cable loss', '+'), 'power')
    G3b = dB_2_lin(dB_input('second stage amplifier gain', '+'), 'power')
    F3b = dB_2_lin(dB_input('second stage amplifier noise factor', '+'), 'power')
    S11_3b = dB_2_lin(dB_input('second stage amplifier S11 parameter', '-'), 'voltage')
    G3 = dB_2_lin(dB_input('pre-amplifier gain', '+'), 'power')
    F3 = dB_2_lin(dB_input('pre-amplifier noise factor', '+'), 'power')
    S11_3 = dB_2_lin(dB_input('pre-amplifier S11 parameter', '-'), 'voltage')
    L2 = dB_2_lin(dB_input('duplexer loss', '+'), 'power')
    L1 = dB_2_lin(dB_input('input cable loss', '+'), 'power')
    Tcoil = lin_pos_input('coil temperature in K')
    #Calculation
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Calculated values~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    #Noise figure of hardware part of NMR spectroscopy Rx chain
    F_HW = 1 + ((2 * T0) / (Tcoil + T0)) * (L1 * L2 * (1 + (1 / (1 - (S11_3 ** 2))) * (F3 - 1 + (1 / (G3 * (1 - (S11_3b ** 2)))) * (F3b - 1 + ((L4 * F5 - 1) / G3b)))) - 1)
    print('Noise figure of the hardware part of NMR spectroscopy Rx chain:\n{:.4f} (linear scale) = {:.4f} dB\n'.format(F_HW, lin_2_dB(F_HW, 'power')))
    #Overall noise figure of NMR spectroscopy Rx chain
    #F22 = (F_HW / (n_meas * n_acq)) * 2
    F22 = F_HW / n_meas
    print('Overall noise figure of NMR spectroscopy system Rx chain:\n{:.4f} (linear scale) = {:.4f} dB\n'.format(F22, lin_2_dB(F22, 'power')))
    #Expected signal-to-noise ratio on the probe
    SNRin = SNRout * F22
    print('Expected signal-to-noise ratio on the probe:\n{:.4f} (linear scale; power ratio) = {:.4f} dB\n'.format(SNRin, lin_2_dB(SNRin, 'power')))
    return

def formula_determinator(model, path):
    '''Use for choosing the appropriate noise model of NMR spectroscopy Rx chain'''
    if model == 1:
        if path == 1:
            F11()
        else:
            F12()
    else:
        if path == 1:
            F21()
        else:
            F22()

#Main program written as a function
def main():
    '''NMR spectroscopy system Rx chain noise figure calculator'''
    print('~~~~~~~~~~~NMR Spectroscopy System Rx Chain Noise Figure Calculator~~~~~~~~~~~')
    print()
    #Noise model and path selection
    model, path = init_selection()
    #Calculation
    F = formula_determinator(model, path)
    input('For calculator termination press Enter...') #so that the program doesn't close immediately after execution when run via cmd
    return

#Main program execution
main()
