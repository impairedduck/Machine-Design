from math import sqrt, pi, pow

# function to calculate goodman safety factor
def goodman_safety_factor(Sut, d, Se, A, B):
    # safety factor calculation
    gnf = ((pi * d ** 3) / 16) * (A / Se + B / Sut) ** -1

    return gnf

# function to calculate von mises
def von_mises_safety_factor(Kf, Kfs, Ma, Tm, d):
    sigA = ((32 * Kf * Ma) / (pi * (d ** 3))) ** 2
    sigM = (3 * ((16 * Kfs * Tm) / (pi * (d ** 3))) ** 2)
    sigmapmax = (sigA + sigM) ** (1/2)
    vmnf = (Sy / sigmapmax)
    
    return vmnf

# function to calculate conservative safety factor
def cons_safety_factor(Kf, Kfs, Ma, Tm, d):
    sigmaPa = (((32 * Kf * Ma) / (pi * (d ** 3))) ** 2) ** (1/2)
    sigmaPm = ((3 * ((16 * Kfs * Tm) / (pi * (d ** 3))) ** 2)) ** (1/2)
    cnf = (Sy / (sigmaPa + sigmaPm))
    return cnf

# function to calculate the required diameter based on Goodman
def required_diameter_goodman(nfMin, Se, A, Sut, B): 
    minD = ((16 * nfMin / pi) * (((1 / Se) * A ) + ((1 / Sut) * B))) ** (1 / 3)
    return minD

# function to calculate the required diameter based on conservative first cycle yield
def required_diamater_conservative(Kf, Ma, Kfs, Tm, nfMin, Sy):
    Vm = (1024 * (Kf ** 2) * (Ma ** 2)) + (768 * (Kfs ** 2) * (Tm ** 2))
    minD2 = (nfMin * sqrt(Vm) / (pi * Sy)) ** (1 / 3)
    return minD2

# constants
Sut = 68
Sy = 37.5
SePrime = 0.5 * Sut
nfMin = 1.5

# values based on user input to pass into the functions
Ma = float(input("Bending moment: ")) / 1000
Tm = float(input("Torque: ")) / 1000
d = float(input("Diameter: "))

# user input to determine the correct condition based on the question
KtInput = int(input(
    "Select appropriate condition:\n"
    "[1] Sharp radius\n"
    "[2] Wide radius\n"
    "[3] Retaining ring groove\n"
    "[4] Keyway\n"))

# values for Kt and Kts from table 7-1 depending on the user input
if KtInput == 1:
    Kt = 2.7 
    Kts = 2.2
    r = 0.02 * d
elif KtInput == 2:
    Kt = 1.7 
    Kts = 1.5
    r = 0.1 * d
elif KtInput == 3:
    Kt = 5
    Kts = 3
    r = 0.01
elif KtInput == 4:
    Kt = 2.14
    Kts = 3
    r = 0.02 * d
    
# calculations for the square root of a to calculate notch sensitivity
sqrtaBending = 0.246 - 3.08e-3 * Sut + 1.51e-5 * Sut**2 - 2.67e-8 * Sut**3 # equation for bending
sqrtaTorsion = 0.190 - 2.51e-3 * Sut + 1.35e-5 * Sut**2 - 2.67e-8 * Sut**3 # equation for torsion

# notch sensitivity
q = 1 / (1+(sqrtaBending / sqrt(r)))
qs = 1 / (1+(sqrtaTorsion / sqrt(r)))

# stress concentration factors, converting Kt and Kts to Kf and Kfs
Kf = 1 + q * (Kt - 1)
Kfs = 1 + qs * (Kts - 1)

# endurance limit factors
Ka = 2 * Sut ** -0.217
Kb = 0.879 * d ** -0.107
# other factors = 1
Kc = Kd = Ke = 1

# endurance limit calculation
Se = Ka * Kb * Kc * Kd * Ke * SePrime

# calculation for A and B
A = sqrt(4* (Kf * Ma) ** 2)
B = sqrt(3 * (Kfs * Tm) ** 2)


# getting safety factor values by plugging in variables into function and printing the results 
print("Goodman safety factor: " + str(goodman_safety_factor(Sut, d, Se, A, B)))
print("Von Mises safety factor: " + str(von_mises_safety_factor(Kf, Kfs, Ma, Tm, d)))
print("Conservative safety factor: " + str(cons_safety_factor(Kf, Kfs, Ma, Tm, d)))

# getting minimum diameter values from function and printing
print("The minimum diameter based on infinite life Goodman is: " + str(required_diameter_goodman(nfMin, Se, A, Sut, B)))
print("The minimum diameter based on conservative first cycle yield is: " + str(required_diamater_conservative(Kf, Ma, Kfs, Tm, nfMin, Sy)))