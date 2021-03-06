# Changelog

This file tries to regroup all notable modifications of the ``beyond`` library.
Each release is linked to a git commit.

## [v0.6.1] - 2018-11-01

### Added

- Visibility allow passing user listeners and merge them with station listeners
- Better describe when a wrong argument type is provided to ``Date`` constructor

### Changed

- Better ``Date`` subclass handling
- When interpolating an ``Ephem`` object, the research for the good points is faster
  due to the use of binary search, particularly when dealing with long ephemeris files

## [v0.6] - 2018-10-20

### Added

- Tle generator error handling
- Maneuvers for the Kepler propagator
- CCSDS handling of maneuvers
- Possibility to have tolerant ephems regarding date inputs
- Entry points for EOP databases registration
- JPL module now callable on bsp files for details on content
- Python 3.7 compatibility and tests
- Library custom errors
- Config set method
- Ephem object deep copy and conversions

### Changed

- Eop acquisition is done at Date creation, instead of at frame transformation
- get_body only allows one body selection at a time

### Removed

- Station propagation delay : The method was heavy and not entirely correct, if not totally wrong

## [v0.5] - 2018-05-01

### Added

- TLE tests and coverages
- Possibility to compute passes with light propagation delay taken into account
- CCSDS OEM handle multiple Ephems
- CCSDS handling of frame central body
- JPL frames bulk creation
- JPL .tpc files handling for frame central body definition
- Date.strftime
- Define a mask for a station

### Changed

- The CCSDS API now mimicks the json (load, loads, dump, dumps)
- Frames translation now directly with vectors
- Node harmonisation, only one implementation used
- Stations handling has a proper module
- MIT license

## [v0.4] - 2017-12-10

### Added
- Config get() method to implement default behaviour in case of missing parameter
- Documentation of orbital forms (cartesian, keplerian, etc.)
- TDB timescale
- Tle now keep any keyword argument passed in a kwargs attribute
- Others listeners can be added to a visibility computation
- Possibility to issue an error, a warning or nothing in case of missing Earth Orientation Parameters
- Possibility to define a custom Earth Orientation Parameters database

### Removed
- The config variable does not depend on a specific file anymore (previously ConfigParser, then TOML)
  but is a dictionnary

### Changed
- replacement of incorrect 'pole_motion' functions and variables names for
  'earth_orientation'
- Moon analytic position now computed with respect to TDB timescale
- A Listener does not return a string anymore, but an Event object
- Tests are now conducted by tox

## [v0.3] - 2017-06-27

### Added
- Integration of JPL ephemeris by interfacing Brandon Rhodes' [jplephem](https://github.com/brandon-rhodes/python-jplephem) python library
- First try at RK4 numerical propagator
- Listeners for events computation (AOS, LOS, umbra, etc.)
- CCSDS Orbit Data Message reading and writing
- Multi TLE parser (#18)
- frames now declare a central body, with some caracteristics (#20)

### Changed
- Spherical parameters orders (now r, theta, phi)
- Propagators are now instances instead of classes
- ``solarsystem`` module

### Fixed
- Correction of velocity computation when switching from cartesian to spherical
- COSPAR ID parsing in TLE

## [v0.2.1] - 2017-03-09

Change the name of the library to beyond (formerly space-api)

## [v0.2] - 2017-03-04

### Added
- CIO based frames (#1)
- Ephem object (#3)
- Full SGP4/SDP4 propagator, by interfacing Brandon Rhodes' [sgp4](https://github.com/brandon-rhodes/python-sgp4) python library (#4)
- Python classifiers for PyPI (#8)
- Lagrange Interpolation in Ephem objects (#15)

### Changed
- Date inner values in TAI (#13)

### Fixed
- Ordering of Node2 graphs (#2)

## [v0.1] - 2016-05-22

Initial release with basic functionnalities