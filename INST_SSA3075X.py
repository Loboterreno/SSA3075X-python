##
## Siglent SSA3075X Spectrum Analyzer Library
##
## This library has been made to operate the basic functionalities of the SSA3075X
## spectrum analyzer. The functions include things as select frequency, bandwidth and acquire 
## for these specific tunnings.
## Author : German G.

from math import isnan
import pyvisa
from functools import wraps
from pyvisa.constants import StopBits, Parity

#Constants initialization
TIMEOUT= 5000
TERMINATION = "\n"
DEVICE_DESCRIPTION= "SSA5PGCD6R0697"
DEVICE_NAME= "SSA3075X"

#Variable initialization"

## Connectivity error handler
def connectivity_error_handler(fn):
    @wraps(fn)
    def decorator(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except NameError as e:
            print(DEVICE_NAME+":ERROR.Device not connected.Use "+DEVICE_NAME+".connect() first")
        except AssertionError as e:
            print(DEVICE_NAME+":ERROR.Could not perform action.Check the device is correctly detected by the OS, or the connection parameters are adequate.")
        except AttributeError as e:
            print(DEVICE_NAME+":ERROR.Device not connected.Check the device is correctly detected by the OS, or the connection parameters are adequate.")
    return decorator

## Connects to the SSA3075X. Since this device uses an special IVI driver for instrumentation,
## looks like the connection settings don't need to be specified.
def connect():
    global instrument
    rm = pyvisa.ResourceManager()
    rlist = rm.list_resources()
    instrument = None
    for resource in rlist:
        if DEVICE_DESCRIPTION in resource:
            instrument = rm.open_resource(resource)
            instrument.read_termination = TERMINATION
            instrument.write_termination = TERMINATION
            instrument.timeout = TIMEOUT
            print(DEVICE_NAME+":Correctly detected and connected")
    if instrument == None:
            print(DEVICE_NAME+":ERROR.Device not detected, check connection cables, drivers or instrument at OS settings.Current instrument description:'"+DEVICE_DESCRIPTION+"'")
     
## Upon loading the library, the device will attempt a connection     
connect()
 
## Ask for the IDN of the device in VISA programming language -OK
## example command: SSA3075X.get_device_identity()
@connectivity_error_handler
def get_device_identity():
    global instrument
    #print(instrument.baud_rate)
    command = "*IDN?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response
    
## turn off the spectrum analyzer -OK
## example command: SSA3075X.turn_off()
@connectivity_error_handler
def shutdown():
    global instrument
    command = "SYST:POW:OFF"
    instrument.write(command)
    print("Sending: "+command )
    
## Save spectrum analyzer current measurement. it can be saved in several typefiles
## being the most interesting CSV or images -OK
## example command: SSA3075X.save_measurement("JPG","measurement_test.jpg")
@connectivity_error_handler
def save_measurement(ftype,fname):
    global instrument
    if ftype not in ["STA","TRC","COR","CSV","LIM","JPG","BMP","PNG"]:
        print("ERROR: Unexpected frequency order of magnitude")
    command = "MMEM:STOR "+str(ftype)+",'"+str(fname)+"'"
    instrument.write(command)
    print("Sending: "+command )

## Gets the central frequency from the SpectrumAnalyzer - OK
## example command: SSA3075X.get_center_frequency() ans: '3.75000000000E+09'
@connectivity_error_handler
def get_center_frequency():
    global instrument
    command = "SENS:FREQ:CENT?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response
    
## Set a central frequency to the SpectrumAnalyzer - OK
## example command: SSA3075X.set_center_frequency(250,"MHz")
@connectivity_error_handler
def set_center_frequency(f,fmag):
    global instrument
    if fmag not in ["Hz","kHz","MHz","GHz"]:
        print("ERROR: Unexpected frequency order of magnitude")
    command = "SENS:FREQ:CENT "+str(f)+" "+str(fmag)
    instrument.write(command)
    print("Sending: "+command)

## get start frequency of the span 
@connectivity_error_handler
def get_start_frequency():
    global instrument
    command = "SENS:FREQ:STAR?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response
    
## set start frequency of the span 
@connectivity_error_handler
def set_start_frequency(f, fmag):
    global instrument 
    if fmag not in ["Hz","kHz","MHz","GHz"]:
        print("ERROR: Unexpected frequency order of magnitude")
    command = "SENS:FREQ:STAR "+str(f)+" "+str(fmag)
    instrument.write(command)
    print("Sending: "+command)
   
## get stop frequency of the span 
@connectivity_error_handler
def get_stop_frequency():
    global instrument
    command = "SENS:FREQ:STOP?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response
    
## set start frequency of the span 
@connectivity_error_handler
def set_stop_frequency(f, fmag):
    global instrument 
    if fmag not in ["Hz","kHz","MHz","GHz"]:
        print("ERROR: Unexpected frequency order of magnitude")
    command = "SENS:FREQ:STOP "+str(f)+" "+str(fmag)
    instrument.write(command)
    print("Sending: "+command)
    
## Gets the span frequency range from the SpectrumAnalyzer - OK
## example command: SSA3075X.get_span_range() ans: '7.50000000000E+09'
@connectivity_error_handler
def get_span_range():
    global instrument
    command = "SENS:FREQ:SPAN?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response

## Set a span frequency range to the SpectrumAnalyzer - OK
## example command: SSA3075X.set_span_range(100,"MHz")
@connectivity_error_handler
def set_span_range(f,fmag):
    global instrument
    if fmag not in ["Hz","kHz","MHz","GHz"]:
        print("ERROR: Unexpected frequency order of magnitude") 
    command = "SENS:FREQ:SPAN "+str(f)+" "+str(fmag)
    instrument.write(command)
    print("Sending: "+command)

## Sets a full span at the SpectrumAnalyzer - OK
## example command: SSA3075X.set_full_span()
@connectivity_error_handler
def set_full_span():
    global instrument
    command = "SENS:FREQ:SPAN:FULL"
    instrument.write(command)
    print("Sending: "+command )

## Sets a zero span at the SpectrumAnalyzer - OK
## example command: SSA3075X.set_zero_span()
@connectivity_error_handler
def set_zero_span():
    global instrument
    command = "SENS:FREQ:SPAN:ZERO"
    instrument.write(command)
    print("Sending: "+command)
    
## asks for a the reference level of the SpectrumAnalyzer - OK
## example command: SSA3075X.get_reference_level()  ans: '3.000000000E+01'
@connectivity_error_handler
def get_reference_level():
    global instrument
    command = "DISP:WIND:TRAC:Y:RLEV?"
    instrument.write(command)
    print("Sending: "+command)
    response = instrument.read()
    return response

## Sets a the reference level of the SpectrumAnalyzer - OK
## example command: SSA3075X.set_reference_level(0,"dbm")
@connectivity_error_handler
def set_reference_level(amplitude,mag):
    global instrument
    if mag not in ["DBM","DBMV","DBuV","V","W"]:
        print("ERROR: Unexpected voltage or power unit")
    command = "DISP:WIND:TRAC:Y:RLEV "+str(amplitude)+" "+str(mag)
    instrument.write(command)
    print("Sending: "+command )

## gets a the auto attenuation state of the SpectrumAnalyzer - OK
## example command: SSA3075X.get_auto_attenuation_state() ans: '1'
@connectivity_error_handler
def get_auto_attenuation_state():
    global instrument
    command = "SENS:POW:RF:ATT:AUTO?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response

## Sets a the auto attenuation state of the SpectrumAnalyzer - OK
## example command: SSA3075X.set_reference_level(0,"dbm")
@connectivity_error_handler
def set_auto_attenuation_state(state):
    global instrument
    if state not in ["ON","OFF"]:
        print("ERROR: Unexpected state")
    command = "SENS:POW:RF:ATT:AUTO "+str(state)
    instrument.write(command)
    print("Sending: "+command )

## Gets the attenuation set by the SpectrumAnalyzer in dB - OK
## example command: SSA3075X.get_attenuation_dB() ans: '3.000000000E+01'
@connectivity_error_handler
def get_attenuation_dB():
    global instrument
    command = "SENS:POW:RF:ATT?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response

## Sets a attenuation to the signal read by the SpectrumAnalyzer in dB - OK
## example command: SSA3075X.set_attenuation_dB() 
@connectivity_error_handler
def set_attenuation_dB(amplitude):
    global instrument
    command = "SENS:POW:RF:ATT "+str(amplitude)
    instrument.write(command)
    print("Sending: "+command )
 
## Gets the auto amplifyer gain state of the SpectrumAnalyzer - OK
## example command: SSA3075X.get_auto_preamplifyer_gain_state() ans: '1'
@connectivity_error_handler
def get_auto_preamplifyer_gain_state():
    global instrument
    command = "SENS:POW:RF:GAIN:STAT?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response

## Sets the auto amplifyer gain state of the SpectrumAnalyzer ("ON","OFF")- OK
## example command: SSA3075X.set_auto_preamplifyer_gain_state()
@connectivity_error_handler
def set_auto_preamplifyer_gain_state(state):
    global instrument
    if state not in ["ON","OFF"]:
        print("ERROR: Unexpected state")
    command = "SENS:POW:RF:GAIN:STAT "+str(state)
    instrument.write(command)
    print("Sending: "+command )

## Gets the sweep mode of the SpectrumAnalyzer - OK
## example command: SSA3075X.get_sweep_mode() ans: 'AUTO'
@connectivity_error_handler
def get_sweep_mode():
    global instrument
    command = "SENS:SWE:MODE?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response

## Sets the sweep mode of the SpectrumAnalyzer - OK
## example command: SSA3075X.set_sweep_mode("AUTO")
@connectivity_error_handler
def set_sweep_mode(mod):
    global instrument
    if mod not in ["AUTO","FFT","SWE"]:
        print("ERROR: Unexpected sweep mode command")        
    command = "SENS:SWE:MODE "+str(mod)
    instrument.write(command)
    print("Sending: "+command )

## Gets the sweep time of the SpectrumAnalyzer - OK
## example command: SSA3075X.get_sweep_time() ans: '9.303200000E-02'
@connectivity_error_handler
def get_sweep_time():
    global instrument
    command = "SENS:SWE:TIME?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response

## Sets the sweep time of the SpectrumAnalyzer - OK
## important: this function only works if sweep mode is in "SWE"
## example command: SSA3075X.set_sweep_time() 
@connectivity_error_handler
def set_sweep_time(sweeptime, tmag):
    global instrument
    if tmag not in ["ks","s","ms","us"]:
        print("WARNING: Unexpected time magnitude")        
    command = "SENS:SWE:TIME "+str(sweeptime)+str(tmag)
    instrument.write(command)
    print("Sending: "+command )

## Gets the sweep continuity (if it has been stopped or not) - OK
## example command: SSA3075X.get_sweep_continuity() ans: '1'
@connectivity_error_handler
def get_sweep_continuity():
    global instrument
    command = "INIT:CONT?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response
    
## Sets the sweep continuity (to stop it or restart it) - OK
## example command that freezes the acquisition: SSA3075X.set_sweep_continuity("OFF") 
@connectivity_error_handler
def set_sweep_continuity(state):
    global instrument
    if state not in ["ON","OFF"]:
        print("ERROR: Unexpected state")
    command = "INIT:CONT "+str(state)
    instrument.write(command)
    print("Sending: "+command )
    
## sets a specific trace to an specific configuration; activate, deactivate it, etc..
## example command that activates trace 1: SSA3075X.set_trace_mode(1,"WRIT")
@connectivity_error_handler
def set_trace_mode(ntrace,tracemode):
    global instrument
    if tracemode not in ["WRIT","MAXH","MINH","VIEW","BLAN","AVER"]:
        print("WARNING: Unexpected formatted mode")
    if ntrace not in [1,2,3,4]:
        print("WARNING: Unrecognized trace number")
    command = ":TRAC"+str(ntrace)+":MODE "+str(tracemode)
    instrument.write(command)
    print("Sending: "+command )

## gets the information about a specific trace and its configuration
## example command that queries trace 1: SSA3075X.set_trace_mode(1,"VIEW")
@connectivity_error_handler
def get_trace_mode(ntrace):
    global instrument
    if ntrace not in [1,2,3,4]:
        print("WARNING: Unrecognized trace number")
    command = ":TRAC"+str(ntrace)+":MODE?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response
   
## gets the displayed data about a specific trace and its configuration
## example command that queries trace 1 data: SSA3075X.get_trace_data(1) ans: (751 values)
@connectivity_error_handler
def get_trace_data(ntrace):
    global instrument
    if ntrace not in [1,2,3,4]:
        print("WARNING: Unrecognized trace number")
    command = ":TRAC"+str(ntrace)+":DATA?"
    instrument.write(command)
    print("Sending: "+command )
    response = instrument.read()
    return response
    
## auxiliary function to find out the frequency of each of the captured points
def points_frequency_division(initial_f,final_f):
    fo = initial_f
    ff = final_f
    POINTS = 751
    point_range = POINTS-1
    
    nums= []
    
    diff = ff-fo
    intervals = diff/(point_range)
    print(intervals)
    
    for n in range (0,POINTS):
        nums.append(fo+n*intervals) 
    print(nums)
    return nums
    
## auxiliary function to do a bigger sweep than 751 points in definite span range
#unfinished
def total_span_division(initial_f, final_f, step_size, step_size_magnitude, stage):
    fo = initial_f
    ff = final_f
    diff = ff-fo
    total_points_calculated = diff/step_size_magnitude
    if total_points <751:
        fo = initial_f
        ff = final_f
    else:
        q = total_points_calculated 
    
    
    
    