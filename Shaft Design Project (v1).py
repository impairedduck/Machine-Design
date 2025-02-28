from math import sqrt, pi, pow

# function to calculate the required diameter for a specified safety factor
def required_diameter(Ma, Tm, Kf, Kfs, Se, Sut, Sy, n=1.5):
    # For infinite life (Goodman criterion) with safety factor n
    term_1 = (n/Se)*sqrt((4*(pow((Kf*Ma), 2)))+(0))
    term_2 = (n/Sut)*sqrt(((0))+(3*(pow(Kfs*Tm, 2))))
    min_d_goodman = pow(((16)/(pi))*(term_1+term_2), 1/3)
    
    # For conservative first cycle with safety factor n
    factor = (1024*pow(Kf, 2))*(pow(Ma, 2))+(768*(pow(Kfs, 2)))*(pow(Tm, 2))
    min_d_conservative = pow((n*sqrt(factor))/(pi*Sy), 1/3)
    
    # Return the larger of the two diameters
    return max(min_d_goodman, min_d_conservative)

# constants for 1030 HR steel
Sut = 68  # ksi
Sy = 37.5  # ksi
SePrime = 0.5 * Sut

# problem specifics
Ma = 400 / 1000  # Convert in-lbf to kip-in
Tm = 300 / 1000  # Convert in-lbf to kip-in
safety_factor = 1.5

# Wide radius condition (from your code)
Kt = 1.7 
Kts = 1.5

# We need to initialize d to calculate r, but this creates a circular dependency
# Let's use an iterative approach
d_guess = 0.5  # Initial guess in inches
tolerance = 0.0001
max_iterations = 20
converged = False

for i in range(max_iterations):
    # Calculate r based on current d_guess
    r = 0.1 * d_guess
    
    # Calculate notch sensitivity
    sqrtaBending = 0.246 - 3.08e-3 * Sut + 1.51e-5 * Sut**2 - 2.67e-8 * Sut**3
    sqrtaTorsion = 0.190 - 2.51e-3 * Sut + 1.35e-5 * Sut**2 - 2.67e-8 * Sut**3
    
    q = 1 / (1+(sqrtaBending / sqrt(r)))
    qs = 1 / (1+(sqrtaTorsion / sqrt(r)))
    
    # Calculate stress concentration factors
    Kf = 1 + q * (Kt - 1)
    Kfs = 1 + qs * (Kts - 1)
    
    # Calculate endurance limit factors
    Ka = 2 * Sut ** -0.217
    Kb = 0.879 * d_guess ** -0.107
    
    # Other factors = 1
    Kc = Kd = Ke = 1
    
    # Calculate endurance limit
    Se = Ka * Kb * Kc * Kd * Ke * SePrime
    
    # Calculate the required diameter
    d_new = required_diameter(Ma, Tm, Kf, Kfs, Se, Sut, Sy, safety_factor)
    
    # Check convergence
    if abs(d_new - d_guess) < tolerance:
        converged = True
        break
    
    # Update guess for next iteration
    d_guess = d_new

# Display results
if converged:
    print(f"Minimum required shaft diameter: {d_new:.4f} inches")
else:
    print(f"Warning: Solution did not fully converge after {max_iterations} iterations")
    print(f"Best estimate of minimum required shaft diameter: {d_new:.4f} inches")

# Calculate final safety factors to verify
d = d_new

# Recalculate parameters for final diameter
r = 0.1 * d
sqrtaBending = 0.246 - 3.08e-3 * Sut + 1.51e-5 * Sut**2 - 2.67e-8 * Sut**3
sqrtaTorsion = 0.190 - 2.51e-3 * Sut + 1.35e-5 * Sut**2 - 2.67e-8 * Sut**3
q = 1 / (1+(sqrtaBending / sqrt(r)))
qs = 1 / (1+(sqrtaTorsion / sqrt(r)))
Kf = 1 + q * (Kt - 1)
Kfs = 1 + qs * (Kts - 1)
Ka = 2 * Sut ** -0.217
Kb = 0.879 * d ** -0.107
Se = Ka * Kb * Kc * Kd * Ke * SePrime

# Calculate A and B
A = sqrt(4* (Kf * Ma) ** 2)
B = sqrt(3 * (Kfs * Tm) ** 2)

# Calculate Goodman safety factor
goodman_sf = ((pi * d ** 3) / 16) * (A / Se + B / Sut) ** -1

# Calculate Von Mises safety factor
sigA = ((32 * Kf * Ma) / (pi * (d ** 3))) ** 2
sigM = (3 * ((16 * Kfs * Tm) / (pi * (d ** 3))) ** 2)
sigmapmax = (sigA + sigM) ** (1/2)
von_mises_sf = (Sy / sigmapmax)

# Calculate Conservative safety factor
sigmaPa = (((32 * Kf * Ma) / (pi * (d ** 3))) ** 2) ** (1/2)
sigmaPm = ((3 * ((16 * Kfs * Tm) / (pi * (d ** 3))) ** 2)) ** (1/2)
cons_sf = (Sy / (sigmaPa + sigmaPm))

print(f"Verification of safety factors for diameter {d:.4f} inches:")
print(f"Goodman safety factor: {goodman_sf:.4f}")
print(f"Von Mises safety factor: {von_mises_sf:.4f}")
print(f"Conservative safety factor: {cons_sf:.4f}")