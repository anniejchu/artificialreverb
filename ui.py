import mainreverb as mrv
import time
import mainreverb as mrv
import algohelper
import convhelper
import sys
def welcome():
    print("""
    ---------------------------------------------------------------
    CAN I REVERB IT? (YES, YOU CAN!)
    ---------------------------------------------------------------
    WELCOME! GIVE AN INPUT .WAV FILE OF YOUR CHOICE
    AND YOU'LL GET BACK A REVERBED VERSION OF YOUR CHOOSING
    """)
def chooseinputwav():
    print("""
    --------------------------------
    STEP 1: CHOOSE AN INPUT .WAV FILE
    --------------------------------
    You may choose your own local 
    .wav file or an existing preset.
    ---------------------------------
    [1] - Cantina Band (3 second version)
    [2] - XYZ
    [3] - XYZ
    [4] - Choose this to enter your filepath next.
    """)
    
    choice = input("INPUT SIGNAL OF CHOICE: ")
    if choice in str([1,2,3,4]):
        if choice == str(4):
            input_sig = input("Enter .wav local path: ")
            if input_sig[-4:] == ".wav":
                print("success")
                print(f"You Chose: {input_sig}")
                return input_sig
            else:
                print("ERROR: Try again")
                # return False
                chooseinputwav()
        else:
            input_sig = mrv.in_presets[int(choice)-1]
            print(f"You Chose: {input_sig}")
            return input_sig
    elif choice == "exit":
        quit()
    else:
        print("ERROR: Not one of the options")
        chooseinputwav()

def choose_reverb():
    print("""
    --------------------------------
    STEP 2: CHOOSE A REVERB TYPE
    --------------------------------
    You can choose between ALGORITHMIC AND CONVOLUTION.
    ---------------------------------
    [1] - CONVOLUTION
    [2] - ALGORITHMIC
    """)
    choice = int(input("INPUT REVERB: "))
    if choice == 1:
        return True
    else:
        return False

def choose_IR():
    print("""
    --------------------------------
    STEP 3: CHOOSE AN IR
    --------------------------------
    You can choose a PRESET IR or load your own in (.wav)
    ---------------------------------
    [1] - CLASSROOM
    [2] - HALLWAY
    [3] - COMPUTER LAB
    [4] - Choose this to enter your own IR.
    """)
    choice = input("INPUT IR OF CHOICE: ")
    if choice in str([1,2,3,4]):
        if choice == str(4):
            input_IR = input("Enter .wav local path: ")
            if input_IR[-4:] == ".wav":
                print("success")
                print(f"You Chose: {input_IR}")
                return input_IR
            else:
                print("ERROR: Try again")
                # return False
                choose_IR()
        else:
            input_IR = mrv.in_presets[int(choice)-1]
            print(f"You Chose: {input_IR}")
            return input_IR
    else:
        print("ERROR: Not one of the options")
        choose_IR()
    
def choose_mix():
    print("""
    --------------------------------
    STEP 3: HOW DO YOU WANT IT MIXED?
    --------------------------------
    ENTER A PERCENTAGE OUT OF 100
    100% = COMPLETELY WET
    0% = COMPLETELY DRY
    ---------------------------------
    """)
    mix_amt = input("Mix %: ")
    return int(mix_amt)/100



def main():
    welcome()
    # time.sleep(2)
    input_sig = chooseinputwav()
    rev_type = choose_reverb()
    if rev_type == True:
        input_IR = choose_IR()
        mix_amt = choose_mix()
        print(input_IR, input_sig, mix_amt)
        #convreverb(input_sig, input_IR, mix_amt)



main()
# mrv.artreverb(mrv.Preset_Schroeder, mrv.input_sig3)