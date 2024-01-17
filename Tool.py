#Link Budget Tool
import numpy as np

#Inputs:



#Spacecraft Parameters

Ps   =                       #[W] Transmitter Power
Ds   =                       #[m] Spacecraft Antenna Diameter
Tns  =                      #[K] Noise Temperature
wl =                       #[m] Wavelength
f   =                       #[GHz] Frequency
POAs =                       #[deg] Pointing Offset Angle

SWA =                       #[deg] Swath Width Angle
PSA =                       #[arcmin] Pixel Size Angle
Bp  =                       #[-] Bits per Pixel
Dc  =                       #[%] Duty Cycle
Tdl =                       #[hr/day] Downlink Time

InterPlanetaty = True
hb =                       #[m] Orbit Altitude above target body
Mb  =                       #[kg] Target Body Mass
Rb  =                       #[m] Target Body Radius

he =                       #[m] Orbit Altitude above Earth

e  =                       #[deg] Elongation Angle
dse =                       #[m] Distance between Earth and Sun
dss =                       #[m] Distance between Sun and Spacecraft

#Ground Station Parameters
Pg =                       #[W] Transmitter Power
Dg =                       #[m] Ground Antenna Diameter
Tng =                       #[K] Noise Temperature
POAg =                       #[deg] Pointing Offset Angle
Ru =                       #[bit/s] Required Uplink Data Rate


LFt =                       #[-] Transmitter Loss Factor
LFr =                       #[-] Receiver Loss Factor
TAR =                       #[-] Turn around Ratio
eff =0.55                   #[-] Antenna Efficiency (0.55 for parabolic))

#Other Parameters
Re  = 6371000                   #[m] Earth Radius
Gc  = 6.67408*(10**-11)         #[m^3/s^2] Gravitational Constant
c   = 299792458                 #[m/s] Speed of Light
kb = 1.38065*(10**-23)         #[m^2 kg s^-2 K^-1] Boltzmann Constant

#Caluclations:
def to_dB(x): #Converts input to dB
    return 10 * np.log10(x)

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


    
def SNR(P, Tn):
    return EIPR(P, Ds) - to_dB(Ls) - to_dB(Lpr) - to_dB(LFr) + to_dB(G(Dg)) - to_dB(Rd) - to_dB(TAR) - to_dB(Tn * kb) 

print ("SNR Downlink: ", SNR(Ps, Tns))
print ("SNR Uplink: ", SNR(Pg, Tng))


