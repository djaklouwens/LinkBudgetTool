#Link Budget Tool
import numpy as np

#Inputs:
ReqSNR_d    = 10                        #[-] Required Signal to Noise Ratio
ReqSNR_u    = 10                        #[-] Required Signal to Noise Ratio

#Spacecraft Parameters
Ps          = 10                        #[W] Transmitter Power
Ds          = 10                        #[m] Spacecraft Antenna Diameter
POAs        = 10                        #[deg] Pointing Offset Angle
wl          = 10                        #[m] Wavelength

SWA         = 10                        #[deg] Swath Width Angle
PSA         = 10                        #[arcmin] Pixel Size Angle
Bp          = 10                        #[-] Bits per Pixel
Dc          = 10                        #[%] Duty Cycle
Tdl         = 10                        #[hr/day] Downlink Time

#Ground Station Parameters
Pg          = 10                        #[W] Transmitter Power
Dg          = 10                        #[m] Ground Antenna Diameter

POAg        = 10                        #[deg] Pointing Offset Angle
Ru          = 10                        #[bit/s] Required Uplink Data Rate


LFt         = 10                        #[-] Transmitter Loss Factor
LFr         = 10                        #[-] Receiver Loss Factor
TAR         = 10                        #[-] Turn around Ratio
eff         = 0.55                      #[-] Antenna Efficiency (0.55 for parabolic))

#Target Body Parameters
hb          = 10                        #[m] Orbit Altitude above target body
Mb          = 10                        #[kg] Target Body Mass
Rb          = 10                        #[m] Target Body Radius

InterPlanetaty = True
#if false fill this in:
he          = 10                        #[m] Orbit Altitude above Earth

#if true fill this in:
e           = 10                        #[deg] Elongation Angle
dse         = 10                        #[m] Distance between Earth and Sun
dss         = 10                        #[m] Distance between Sun and Spacecraft

#Only fill this in if the f is out of range of the diagram
Tn_d        = 10                        #[K] Noise Temperature Dowlink
Tn_u        = 10                        #[K] Noise Temperature Uplink

#Other Parameters (Do not change)
Re          = 6371000                   #[m] Earth Radius
Gc          = 6.67408*(10**-11)         #[m^3/s^2] Gravitational Constant
c           = 299792458                 #[m/s] Speed of Light
kb          = 1.38065*(10**-23)         #[m^2 kg s^-2 K^-1] Boltzmann Constant

#Caluclations:
def to_dB(x): #Converts input to dB
    return 10 * np.log10(np.abs(x))

f = c / wl

#Transmitter Power
Ps = to_dB(Ps) #dB
Pg = to_dB(Pg) #dB

#Transmitter and Receiver Loss
LFt = to_dB(LFt) #dB
LFr = to_dB(LFr) #dB

#Antenna Gain 
def G(D):
    return np.pi ** 2 * D**2 / wl**2 * eff

#Distance between Earth and Satellite
if InterPlanetaty:
    S = np.sqrt(dse ** 2 + dss ** 2 - 2 * dse * dss * np.cos(e))
else :
    S = np.sqrt((Re + he)**2 - Re**2)
    
#Space Loss
Ls = ( wl/ (4 * np.pi * S))**2

#Half Power Beam Angle
def HPBA(D):
    return 21 / (D * f) #meters and GHz

#Antenna pointing loss
def Lpr(D,POA):
    return -12 * (POA / HPBA(D))**2



#Required Data Rate Calculation
#Orbital Speed
Vo = np.sqrt(Gc * Mb / (Rb + hb))

#Ground Speed
Vg = Vo * Rb / (Rb + hb)

#Swath Width
Sw = 2 * np.tan(SWA/2) * hb

#Pixel Size
Ps = 2 * np.tan(PSA/2) * hb

#Generated Data Rate
Rg = Bp * Sw * Vg / (Ps**2)

#Required Data Rate
Rd = Dc / Tdl

def EIPR(P, D):
    return to_dB(P) + to_dB(G(D)) -to_dB(LFt)

def get_Tn_d(f):
    if f == 0.2:
        return 221
    if f <= 12:
        if f >= 2:
            return 135
    if f == 20:
        return 424
    else:
      print("Frequency out of range, enter Tn_d manually")
      return Tn_d
        
def get_Tn_u(f):
    if f <= 20:
        if f >= 0.2:
            return 614
    if f == 40:
        return 763
    else:
        print("Frequency out of range, enter Tn_u manually")
        return Tn_u


    
def SNR(P, Tn, Dt, Dr, POAt):
    return EIPR(P, Dt) - to_dB(Ls) - to_dB(Lpr(Dt, POAt)) - to_dB(LFr) + to_dB(G(Dr)) - to_dB(Rd) - to_dB(TAR) - to_dB(Tn * kb) 

def print_link_details(link_type, P, Tn, Dt, Dr, POAt):
    print(f"\n{link_type} Link Details:")
    print(f"Transmitter Power (Ps): {P} dB")
    print(f"Space Loss (Ls): {Ls} dB")
    print(f"Pointing Loss (Lpr): {Lpr(Dt, POAt)} dB")
    print(f"Receiver Loss (LFr): {LFr} dB")
    print(f"Antenna Gain (G): {G(Dr)} dB")
    print(f"Required Data Rate (Rd): {Rd} ")
    print(f"Turn Around Ratio (TAR): {TAR}")
    print(f"Effective Noise Temperature (Tn * kb): {Tn * kb} dB")

print ("SNR Downlink: ", SNR(Ps, get_Tn_d(f), Ds, Dg, POAs))
print ("SNR Downlink Margin: ", SNR(Ps, get_Tn_d(f), Ds, Dg, POAs) - ReqSNR_d)
print_link_details("Downlink", Ps, get_Tn_d(f), Ds, Dg, POAs)

print ("SNR Uplink: ", SNR(Pg, get_Tn_u(f), Dg, Ds, POAg))
print ("SNR Uplink Margin: ", SNR(Pg, get_Tn_u(f), Dg, Ds, POAg) - ReqSNR_u)
print_link_details("Uplink", Pg, get_Tn_u(f), Dg, Ds, POAg)

# Your existing code ...

# Example usage:







