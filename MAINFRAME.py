import PySimpleGUI as sg
import mainreverb as mrv
import matplotlib.pyplot as plt
import convhelper as chp
import algohelper as ahp
import numpy as np
#setting theme
sg.theme('DarkGreen5')
szcol = (180,600)

# sg.preview_all_look_and_feel_themes() #uncomment this to preview other types of themes

"""
SETTING UP CONVOLUTION TAB
"""

############## UI SET UP LEFT COLUMN: CHOOSING AUDIO, CHOOSING IR, CHOOSING MIX
layout_input_audio = [
        # [sg.Text("Choose Input Audio ")],
        [sg.Text('You can either choose a Preset from the drop down menu \nOR select a .wav file of your own via the BROWSE button. \n\nIf you have selected both a Preset and your own .wav file, it will default to the .wav file')],
        [sg.Combo(values=['-','Preset 1', 'Preset 2', 'Preset 3'], default_value='-', enable_events=True, key='-COMBO-')],
        [sg.Input('', key='filename', enable_events=True), sg.FileBrowse()],
        [sg.Button('Reset Filename')],
]

layout_IR = [
        # [sg.Text("Choose an Impulse Response ")],
        [sg.Text('Select one of the recorded room impulse responses.')],
        [sg.Radio('Classroom', "IR", default=True, key="ir1", enable_events=True)],
        [sg.Radio('Hallway', "IR", default=False, key="ir2", enable_events=True)],
        [sg.Radio('Computer lab', "IR", default=False, key = "ir3", enable_events=True)],
]

layout_MIX = [
    [sg.Text("How much of the mix is the wet signal? (100% = Fully Wet, 0% = Fully Dry)")],
    [sg.Slider(orientation ='horizontal', key='mixslide', range=(0,100), enable_events=True)],
]


conv_options_FRAME= [[sg.Frame('Choose Your Input Audio',layout_input_audio)], 
                 [sg.Frame('Choose Your IR', layout_IR)],
                 [sg.Frame('Choose Your Mix', layout_MIX)],
                 ]

############## UI SET UP RIGHT COLUMN: BUTTONS
conv_buttons = [[sg.Cancel('Exit'),sg.Button('Reset') ],
                [sg.HorizontalSeparator()],
                [sg.Text('Press REVERB IT \nto hear the reverbed version')],
                [sg.Button('REVERB IT')],
                [sg.HorizontalSeparator()],
                [sg.Text('Press DOWNLOAD REVERB \nto download the .wav of the reverbed version')],
                [sg.Button('DOWNLOAD REVERB')],
                [sg.HorizontalSeparator()],
                [sg.Text('Press PLOT \nto see a comparison of the original and reverbed signals')],
                [sg.Button('PLOT')]]


conv_buttons_FRAME = [[sg.Frame('Options', conv_buttons)],]

""" ############ ALGORITHM UI SET UP """
layout_input_audio_B = [
        # [sg.Text("Choose Input Audio ")],
        [sg.Text('You can either choose a Preset from the drop down menu \nOR select a .wav file of your own via the BROWSE button. \n\nIf you have selected both a Preset and your own .wav file, \nit will default to the .wav file')],
        [sg.Combo(values=['-','Preset 1', 'Preset 2', 'Preset 3'], default_value='-', enable_events=True, key='input_b')],
        [sg.Input('', key='filename_b', enable_events=True), sg.FileBrowse()],
        [sg.Button('Reset Filename', key='rstfile_b')],
]

layout_ALG_options = [
        [sg.Text("Choose a classic Schroeder or Freeverb algorithm \nor enter your own variables for either")],
        [sg.Radio('Preset: Schroeder', "algo", default=True, key="alg1", enable_events=True)],
        [sg.Radio('Preset: Freeverb', "algo", default=False, key="alg2", enable_events=True)],
        [sg.Radio('Custom: Schroeder', "algo", default=False, key="alg3", enable_events=True)],
        [sg.Radio('Custom: Freeverb', "algo", default=False, key="alg4", enable_events=True)],
]

layout_ALG_Fcustom = [
        [sg.Text("Comb Gain")],
        [sg.Slider(orientation ='horizontal', key='gcf', range=(0,1), resolution=0.1, enable_events=True)],
        [sg.Text("Secondary Comb Gain")],
        [sg.Slider(orientation ='horizontal', key='sgcf', range=(0,1), resolution = 0.1,enable_events=True)],
        [sg.Text("All-Pass Gain")],
        [sg.Slider(orientation ='horizontal', key='gapf', range=(0,1), resolution = 0.1,enable_events=True)],
        [sg.Text("Low Pass Comb Delays")],
        [sg.Text('Comb Delay 1', size =(15, 1)), sg.InputText(key='dc1f')],
        [sg.Text('Comb Delay 2', size =(15, 1)), sg.InputText(key='dc2f')],
        [sg.Text('Comb Delay 3', size =(15, 1)), sg.InputText(key='dc3f')],
        [sg.Text('Comb Delay 4', size =(15, 1)), sg.InputText(key='dc4f')],
        [sg.Text('Comb Delay 5', size =(15, 1)), sg.InputText(key='dc5f')],
        [sg.Text('Comb Delay 6', size =(15, 1)), sg.InputText(key='dc6f')],
        [sg.Text('Comb Delay 7', size =(15, 1)), sg.InputText(key='dc7f')],
        [sg.Text('Comb Delay 8', size =(15, 1)), sg.InputText(key='dc8f')],
        [sg.Text("All Pass Delays")],
        [sg.Text('All-Pass Delay 1', size =(15, 1)), sg.InputText(key='dap1f')],
        [sg.Text('All-Pass Delay 2', size =(15, 1)), sg.InputText(key='dap2f')],
        [sg.Text('All-Pass Delay 3', size =(15, 1)), sg.InputText(key='dap3f')],
        [sg.Text('All-Pass Delay 4', size =(15, 1)), sg.InputText(key='dap4f')],
        [sg.Text("Mix Amount")],
        [sg.Slider(orientation ='horizontal', key='mixamt_bf', range=(0,1), resolution=0.1, enable_events=True)],
]

layout_ALG_Scustom = [
        [sg.Text("Comb Gain")],
        [sg.Slider(orientation ='horizontal', key='gcs1', range=(0,1), resolution=0.01, enable_events=True)],
        [sg.Text("Comb Gain 2")],
        [sg.Slider(orientation ='horizontal', key='gcs2', range=(0,1), resolution = 0.01,enable_events=True)],
        [sg.Text("Comb Gain 3")],
        [sg.Slider(orientation ='horizontal', key='gcs3', range=(0,1), resolution = 0.01,enable_events=True)],
        [sg.Text("Comb Gain 4")],
        [sg.Slider(orientation ='horizontal', key='gcs4', range=(0,1), resolution = 0.01,enable_events=True)],
        [sg.Text("All-Pass Gain")],
        [sg.Slider(orientation ='horizontal', key='gaps', range=(0,1), resolution = 0.01,enable_events=True)],
        [sg.Text("Comb Delays")],
        [sg.Text('Comb Delay 1', size =(15, 1)), sg.InputText(key='dc1s')],
        [sg.Text('Comb Delay 2', size =(15, 1)), sg.InputText(key='dc2s')],
        [sg.Text('Comb Delay 3', size =(15, 1)), sg.InputText(key='dc3s')],
        [sg.Text('Comb Delay 4', size =(15, 1)), sg.InputText(key='dc4s')],
        [sg.Text("All Pass Delays")],
        [sg.Text('All-Pass Delay 1', size =(15, 1)), sg.InputText(key='dap1s')],
        [sg.Text('All-Pass Delay 2', size =(15, 1)), sg.InputText(key='dap2s')],
        [sg.Text('All-Pass Delay 3', size =(15, 1)), sg.InputText(key='dap3s')],
        [sg.Text("Mix Amount")],
        [sg.Slider(orientation ='horizontal', key='mixamt_bs', range=(0,1), resolution=0.1, enable_events=True)],
]
alg_buttons = [[sg.Cancel('Exit', key='Exit_b'),sg.Button('Reset', key='reset_b') ],
                [sg.HorizontalSeparator()],
                [sg.Text('Press REVERB IT \nto hear the reverbed version')],
                [sg.Button('REVERB IT', key='reverb_b')],
                [sg.HorizontalSeparator()],
                [sg.Text('Press DOWNLOAD REVERB \nto download the .wav of the reverbed version')],
                [sg.Button('DOWNLOAD REVERB', key='dwnld_b')],
                [sg.HorizontalSeparator()],
                [sg.Text('Press PLOT \nto see a comparison of the original and reverbed signals')],
                [sg.Button('PLOT', key='plt_b')]]

alg_options_FRAME = [[sg.Frame('Choose Your Input Audio',layout_input_audio_B)], 
                 [sg.Frame('Choose Your Algorithm', layout_ALG_options)],
                 [sg.Text('If you chose a custom option, \nuse the fields on the right to enter the parameters.\nThey will not reset when you press the reset button')],
                #  [sg.Frame('CUSTOM: Parameters', Flayout_ALG_custom)],
]

alg_buttons_FRAME =[[sg.Frame('Options', alg_buttons)],]

alg_options_customF = [[sg.Frame('Custom: Freeverb', layout_ALG_Fcustom)]]
alg_options_customS = [[sg.Frame('Custom: Schroeder', layout_ALG_Scustom)]]

conv_layout = [[sg.Column(conv_options_FRAME, element_justification='l', vertical_alignment='top'), sg.VSeparator(),sg.Column(conv_buttons_FRAME, element_justification='r', vertical_alignment='top')]]
alg_layout = [[sg.Column(alg_options_FRAME, element_justification='l', vertical_alignment='top',s=(350,600)), sg.VSeparator(),sg.Column(alg_options_customS, vertical_alignment='top', element_justification='r',s=szcol),sg.VSeparator(),sg.Column(alg_options_customF, element_justification='r', s=szcol),sg.VSeparator(),sg.Column(alg_buttons_FRAME, element_justification='r',s=(300,600))]]

layout = [[sg.Text('Artificial Reverb Generator', size = (40,1), justification='center', font=("Courier", 32), relief=sg.RELIEF_GROOVE, k='-TEXT HEADING-', enable_events=True)], [sg.Text('Annie Chu | Fall 2021 | Olin College')]]
layout +=[[sg.TabGroup([[  sg.Tab('Convolution', conv_layout),
                           sg.Tab('Algorithmic', alg_layout),
                              ]], key='-TAB GROUP-', size = (1200,600),enable_events=True)]]

window = sg.Window('Artificial Reverb Generator', layout, resizable = True,size = (1200, 1000))

def get_input():
    init = ''
    if values['filename'] != '':
        # init = values['filename']
        mrv.in_presets[3] = values['filename']
        # print(mrv.in_presets)
        init = 3
    else:
        if values['-COMBO-'] == 'Preset 1':
            init = 0
        elif values['-COMBO-'] == 'Preset 2':
            init = 1
        elif values['-COMBO-'] == 'Preset 3':
            init = 2
        # init = values['-COMBO-']
        # print(init)
    return init
def get_IR():
    ir = ''
    if values['ir1'] == True:
        ir = 0
    if values['ir2'] == True:
        ir = 1
    if values['ir3'] == True:
        ir = 2
    return ir

def get_input_algo():
    init = ''
    if values['filename_b'] != '':
        # init = values['filename']
        mrv.in_presets[3] = values['filename_b']
        # print(mrv.in_presets)
        init = 3
    else:
        if values['input_b'] == 'Preset 1':
            init = 0
        elif values['input_b'] == 'Preset 2':
            init = 1
        elif values['input_b'] == 'Preset 3':
            init = 2
    return init
    
def set_param_algo():
    custom = ''
    if values['alg1'] == True:
        custom = mrv.Preset_Freeverb
    elif values['alg2'] == True:
        custom = mrv.Preset_Schroeder
    elif values['alg3'] == True:
        custom = ahp.Schroeder(
            [int(values['gcs1']), int(values['gcs2']), int(values['gcs3']), int(values['gcs4'])],
            [int(values['dc1s']), int(values['dc2s']), int(values['dc3s']), int(values['dc4s'])],
            [int(values['gaps']),int(values['gaps']),int(values['gaps'])],
            [int(values['dap1s']), int(values['dap2s']), int(values['dap3s'])],
            int(values['mixamt_bs'])
        )
    elif values['alg4'] == True:
        custom = ahp.Freeverb(
            int(values['gcf']),
            int(values['sgcf']),
            [int(values['dc1f']),int(values['dc2f']),int(values['dc3f']),int(values['dc4f']),int(values['dc5f']),int(values['dc6f']),int(values['dc7f']),int(values['dc8f'])],
            int(values['gapf']),
            [int(values['dap1f']), int(values['dap2f']), int(values['dap3f']), int(values['dap4f'])],
            int(values['mixamt_bf'])
        )
    return custom

########## EVENT LOOP
while True:
    event, values = window.read()
    if event in ('Exit', 'Exit_b', sg.WIN_CLOSED):
        break
    # print(event, values) #for debugging

    #CONVOLUTION
    if values['-TAB GROUP-'] == 'Convolution':
        # print('in convo')
        IN = get_input()
        ir = get_IR()
        mixamt = values['mixslide']
        # print(f"CON ==> input: {IN} || ir: {ir} || mixamt: {mixamt}")
        if event == 'REVERB IT':
            sg.popup('You input signal: ' + str(IN) + '\nIR sig: ' + str(ir) + '\nMIX (%): ' + str(mixamt))
            mrv.convreverb(mrv.in_presets[IN], mrv.IR_presets[ir], mixamt/100)
        if event == 'DOWNLOAD REVERB':
            fs, mixed, original = mrv.convreverb(mrv.in_presets[IN], mrv.IR_presets[ir], mixamt/100, playout = False)
            mrv.download(fs, mixed)
        if event == 'PLOT':
            fs, mixed, original = mrv.convreverb(mrv.in_presets[IN], mrv.IR_presets[ir], mixamt/100, playout = False)
            mrv.plotty(original, mixed, fs)
        if event == 'Reset':
            window['filename'].update('')
            window['-COMBO-'].update('-')
            window['ir1'].Update(True)
            window['ir2'].Update(False)
            window['ir3'].Update(False)
            window['mixslide'].Update(1)
        if event == 'Reset Filename':
            window['filename'].update('')

    #ALGORITHMIC
    if values['-TAB GROUP-'] == 'Algorithmic':
        # print("IN ALGO TAB")
        # custom_alg = set_param_algo()
        in_alg = get_input_algo()
        if event == 'reverb_b':
            custom_alg = set_param_algo()
            sg.popup('You input signal: ' + str(type(in_alg)) + '\nAlg: ' + str(custom_alg))
            mrv.artreverb(custom_alg, mrv.in_presets[in_alg])
        if event == 'dwnld_b':
            fs, mixed, original = mrv.artreverb(custom_alg, mrv.in_presets[in_alg], playout = False)
            mrv.download(fs, mixed)
        if event == 'plt_b':
            fs, mixed, original = mrv.artreverb(custom_alg, mrv.in_presets[in_alg], playout = False)
            mrv.plotty(original, mixed, fs)
        if event == 'reset_b':
            window['filename_b'].update('')
            window['input_b'].update('-')
            window['alg1'].Update(True)
            window['alg2'].Update(False)
            window['alg3'].Update(False)
            window['alg4'].Update(False)
        if event == 'rstfile_b':
            window['filename_b'].update('')

window.close()