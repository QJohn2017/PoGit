from pogit.laser import Laser
from pogit.grid import GridSolver
from pogit.particle import Particle
from pogit.writer import WriteSimulationFiles

# Sizes of the simulation box and grid
xmax, ymax, zmax = 25e-6, 35e-6, 25e-6
Nx, Ny, Nz = 128, 1024, 128

# Total number of simulations steps
Nsteps = 6000

# Number of steps between diagnostics
N_diag = 2000

## Laser parameters
ctau = 4e-6                 # Laser duration in meters
a0 = 3.0                    # Laser normalized amplitude
waist = 5.0e-6              # Laser waist in meters
cdelay = 3 * ctau          # Delay of laser centroid in meters

## Plasma parameters
# Base density
n_p = 8e18/5 * 1e6

# Density profile defined in `codelets/density.py`
density_profile = { 'type': 'Gaussian', 'vacuumCellsY': 100,
         'gasFactor': -1.0, 'gasPower': 4.0,
         'gasCenterLeft': 40e-6, 'gasCenterRight': 60e-6,
         'gasSigmaLeft': 20e-6, 'gasSigmaRight': 80e-6 }

initial_positions = ('Random', 2)

## Creating simulation objects and writing files

gridSolver = GridSolver( xmax, ymax, zmax, Nx, Ny, Nz, Nsteps,
                         N_diag, movingWindow=True, movePoint=1.)

laser = Laser( a0=a0, ctau=ctau, waist=waist, cdelay=cdelay)

eons = Particle( name='Electrons', species='electron' )

ions = Particle( name='Ions', species='ion',
                 base_density=n_p, typicalNppc=2*initial_positions[1],
                 density_profile=density_profile,
                 initial_positions=initial_positions,
                 element='Nitrogen', initial_charge=5,
                 target_species=eons, ionizer_polarization='Lin' )
# Note: only one species can define `base_density` and `typicalNppc`

WriteSimulationFiles( ( eons, ions, gridSolver, laser ) )