
from pytest import fixture, raises

from datetime import timedelta

from beyond.orbits import Tle
from beyond.utils.ccsds import CCSDS


ref_opm = """CCSDS_OPM_VERS = 2.0
CREATION_DATE = 2017-06-21T13:20:25
ORIGINATOR = N/A

META_START
OBJECT_NAME          = N/A
OBJECT_ID            = N/A
CENTER_NAME          = Earth
REF_FRAME            = TEME
TIME_SYSTEM          = UTC
META_STOP

COMMENT  State Vector
EPOCH                = 2008-09-20T12:25:40.104192
X                    =  3459.023611 [km]
Y                    =  5617.725542 [km]
Z                    =  1316.222323 [km]
X_DOT                =    -3.535844 [km/s]
Y_DOT                =     3.550405 [km/s]
Z_DOT                =    -5.846067 [km/s]

COMMENT  Keplerian elements
SEMI_MAJOR_AXIS      =  6730.963463 [km]
ECCENTRICITY         =     0.000670
INCLINATION          =    51.641600 [deg]
RA_OF_ASC_NODE       =   247.462700 [deg]
ARG_OF_PERICENTER    =   130.536000 [deg]
TRUE_ANOMALY         =    35.015255 [deg]"""

ref_opm_no_units = """CCSDS_OPM_VERS = 2.0
CREATION_DATE = 2017-06-21T13:20:25
ORIGINATOR = N/A

META_START
OBJECT_NAME          = N/A
OBJECT_ID            = N/A
CENTER_NAME          = Earth
REF_FRAME            = TEME
TIME_SYSTEM          = UTC
META_STOP

COMMENT  State Vector
EPOCH                = 2008-09-20T12:25:40.104192
X                    =  3459.023611
Y                    =  5617.725542
Z                    =  1316.222323
X_DOT                =    -3.535844
Y_DOT                =     3.550405
Z_DOT                =    -5.846067

COMMENT  Keplerian elements
SEMI_MAJOR_AXIS      =  6730.963463
ECCENTRICITY         =     0.000670
INCLINATION          =    51.641600
RA_OF_ASC_NODE       =   247.462700
ARG_OF_PERICENTER    =   130.536000
TRUE_ANOMALY         =    35.015255"""

ref_opm_strange_units = """CCSDS_OPM_VERS = 2.0
CREATION_DATE = 2017-06-21T13:20:25
ORIGINATOR = N/A

META_START
OBJECT_NAME          = N/A
OBJECT_ID            = N/A
CENTER_NAME          = Earth
REF_FRAME            = TEME
TIME_SYSTEM          = UTC
META_STOP

COMMENT  State Vector
EPOCH                = 2008-09-20T12:25:40.104192
X                    =  3459023.611 [m]
Y                    =  5617725.542 [m]
Z                    =  1316222.323 [m]
X_DOT                =    -3535.844 [m/s]
Y_DOT                =     3550.405 [m/s]
Z_DOT                =    -5846.067 [m/s]

COMMENT  Keplerian elements
SEMI_MAJOR_AXIS      =  6730.963463 [km]
ECCENTRICITY         =     0.000670
INCLINATION          =    51.641600 [deg]
RA_OF_ASC_NODE       =   247.462700 [deg]
ARG_OF_PERICENTER    =   130.536000 [deg]
TRUE_ANOMALY         =    35.015255 [deg]"""

ref_oem = """CCSDS_OEM_VERS = 2.0
CREATION_DATE = 2017-06-21T13:21:32
ORIGINATOR = N/A

META_START
OBJECT_NAME          = N/A
OBJECT_ID            = N/A
CENTER_NAME          = Earth
REF_FRAME            = TEME
TIME_SYSTEM          = UTC
START_TIME           = 2008-09-20T12:25:40.104192
STOP_TIME            = 2008-09-20T14:25:40.104192
INTERPOLATION        = Lagrange
INTERPOLATION_DEGREE = 7
META_STOP

2008-09-20T12:25:40.104192  4083.902464 -993.632000  5243.603665   2.512837   7.259889  -0.583779
2008-09-20T12:28:40.104192  4446.682604  324.930081  5028.090339   1.503730   7.338981  -1.802406
2008-09-20T12:31:40.104192  4621.397102  1629.746327  4599.304773   0.430591   7.107649  -2.945072
2008-09-20T12:34:40.104192  4600.571929  2865.602021  3975.349794  -0.661242   6.575412  -3.963237
2008-09-20T12:37:40.104192  4385.008276  3980.156563  3182.633358  -1.725479   5.764603  -4.813497
2008-09-20T12:40:40.104192  3983.777724  4926.185054  2254.768787  -2.716851   4.709550  -5.459500
2008-09-20T12:43:40.104192  3413.859123  5663.620893  1231.150896  -3.593103   3.455190  -5.873621
2008-09-20T12:46:40.104192  2699.420566  6161.301305  155.260192  -4.316915   2.055142  -6.038263
2008-09-20T12:49:40.104192  1870.774288  6398.318451 -927.224362  -4.857602   0.569297  -5.946690
2008-09-20T12:52:40.104192  963.051607  6364.905826 -1970.414096  -5.192495  -0.938921  -5.603303
2008-09-20T12:55:40.104192  14.667968  6062.814340 -2930.196340  -5.307898  -2.405451  -5.023347
2008-09-20T12:58:40.104192 -934.343798  5505.168129 -3766.120395  -5.199568  -3.768445  -4.232079
2008-09-20T13:01:40.104192 -1844.042731  4715.823893 -4443.090519  -4.872732  -4.970910  -3.263499
2008-09-20T13:04:40.104192 -2676.252828  3728.286282 -4932.798923  -4.341683  -5.962994  -2.158749
2008-09-20T13:07:40.104192 -3396.132523  2584.245378 -5214.851625  -3.629021  -6.703870  -0.964302
2008-09-20T13:10:40.104192 -3973.581416  1331.815891 -5277.556509  -2.764640  -7.163190   0.269951
2008-09-20T13:13:40.104192 -4384.445296  23.550466 -5118.363252  -1.784496  -7.322132   1.492652
2008-09-20T13:16:40.104192 -4611.485054 -1285.699209 -4743.950862  -0.729228  -7.174063   2.652940
2008-09-20T13:19:40.104192 -4645.083540 -2541.010297 -4169.963408   0.357384  -6.724831   3.702386
2008-09-20T13:22:40.104192 -4483.663382 -3689.630755 -3420.399045   1.430078  -5.992658   4.596909
2008-09-20T13:25:40.104192 -4133.794212 -4683.164832 -2526.661729   2.443897  -5.007591   5.298597
2008-09-20T13:28:40.104192 -3609.971567 -5479.615268 -1526.297610   3.356046  -3.810467   5.777381
2008-09-20T13:31:40.104192 -2934.059087 -6045.194803 -461.449620   4.127752  -2.451365   6.012455
2008-09-20T13:34:40.104192 -2134.404723 -6355.810710  622.909564   4.726019  -0.987549   5.993323
2008-09-20T13:37:40.104192 -1244.659051 -6398.142795  1680.893769   5.125155   0.518989   5.720383
2008-09-20T13:40:40.104192 -302.347805 -6170.249938  2667.675635   5.307970   2.004277   5.204973
2008-09-20T13:43:40.104192  652.736161 -5681.669803  3541.421025   5.266551   3.405222   4.468880
2008-09-20T13:46:40.104192  1580.238051 -4953.007966  4265.085772   5.002582   4.662392   3.543335
2008-09-20T13:49:40.104192  2440.962450 -4015.045319  4807.993735   4.527208   5.722567   2.467599
2008-09-20T13:52:40.104192  3198.534420 -2907.413304  5147.130765   3.860491   6.540956   1.287226
2008-09-20T13:55:40.104192  3820.927739 -1676.908758  5268.104550   3.030513   7.082997   0.052125
2008-09-20T13:58:40.104192  4281.806286 -375.522033  5165.743308   2.072196   7.325730  -1.185510
2008-09-20T14:01:40.104192  4561.629818  941.740139  4844.316363   1.025879   7.258727  -2.373326
2008-09-20T14:04:40.104192  4648.486474  2219.161521  4317.369815  -0.064305   6.884566  -3.460952
2008-09-20T14:07:40.104192  4538.616206  3402.663700  3607.179446  -1.152223   6.218831  -4.402107
2008-09-20T14:10:40.104192  4236.598734  4442.108641  2743.832051  -2.191672   5.289589  -5.156603
2008-09-20T14:13:40.104192  3755.186698  5293.456116  1763.962307  -3.138383   4.136309  -5.692163
2008-09-20T14:16:40.104192  3114.777867  5920.677848  709.186816  -3.952004   2.808215  -5.985926
2008-09-20T14:19:40.104192  2342.541924  6297.324902 -375.694970  -4.597935   1.362119  -6.025530
2008-09-20T14:22:40.104192  1471.237347  6407.666741 -1444.650659  -5.048908  -0.140158  -5.809680
2008-09-20T14:25:40.104192  537.778438  6247.339803 -2452.414417  -5.286183  -1.634621  -5.348147"""


@fixture
def tle():
    return Tle("""1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
    2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537""")


@fixture
def orb(tle):
    return tle.orbit()


@fixture
def ephem(orb):
    return orb.ephem(orb.date, timedelta(minutes=120), timedelta(minutes=3))


def assert_orbit(ref, orb):
    assert ref.frame == orb.frame
    assert ref.date == orb.date

    # Precision down to millimeter due to the truncature when writing the CCSDS OPM
    assert abs(ref.x - orb.x) < 1e-3
    assert abs(ref.y - orb.y) < 1e-3
    assert abs(ref.z - orb.z) < 1e-3
    assert abs(ref.vx - orb.vx) < 1e-3
    assert abs(ref.vy - orb.vy) < 1e-3
    assert abs(ref.vz - orb.vz) < 1e-3


def test_dummy():
    with raises(TypeError):
        CCSDS.dumps(None)
    with raises(ValueError):
        CCSDS.loads("dummy text")


def test_dump_opm(orb):

    ref = ref_opm.splitlines()
    txt = CCSDS.dumps(orb).splitlines()

    # the split is here to avoid the creation date line
    assert txt[0] == ref[0]
    assert "\n".join(txt[2:]) == "\n".join(ref[2:])


def test_dump_oem(ephem):

    ref = ref_oem.splitlines()
    txt = CCSDS.dumps(ephem).splitlines()
    # the split is here to avoid the creation date line
    assert txt[0] == ref[0]
    assert "\n".join(txt[2:]) == "\n".join(ref[2:])


def test_dump_oem_linear(ephem):

    ephem.method = ephem.LINEAR
    txt = CCSDS.dumps(ephem).splitlines()

    assert "\n".join(txt[2:14]) == """ORIGINATOR = N/A

META_START
OBJECT_NAME          = N/A
OBJECT_ID            = N/A
CENTER_NAME          = Earth
REF_FRAME            = TEME
TIME_SYSTEM          = UTC
START_TIME           = 2008-09-20T12:25:40.104192
STOP_TIME            = 2008-09-20T14:25:40.104192
INTERPOLATION        = Linear
META_STOP"""


def test_load_opm(orb):

    orb.form = "cartesian"

    orb2 = CCSDS.loads(ref_opm)
    assert_orbit(orb, orb2)

    orb3 = CCSDS.loads(ref_opm_no_units)
    assert_orbit(orb, orb3)

    # Dummy units, that aren't specified as valid
    with raises(ValueError):
        CCSDS.loads(ref_opm_strange_units)

    # One mandatory line is missing
    truncated_opm = "\n".join(ref_opm.splitlines()[:15] + ref_opm.splitlines()[16:])
    with raises(ValueError):
        CCSDS.loads(truncated_opm)


def test_load_oem(ephem):

    ephem2 = CCSDS.loads(ref_oem)

    assert ephem2.frame == ephem.frame
    assert ephem2.start == ephem.start
    assert ephem2.stop == ephem.stop
    assert ephem2.method == ephem2.LAGRANGE
    assert ephem2.order == 8

    for orb, orb2 in zip(ephem, ephem2):
        assert_orbit(orb, orb2)

    with raises(ValueError):
        CCSDS.loads("\n".join(ref_oem.splitlines()[:15]))

    with raises(ValueError):
        CCSDS.loads("\n".join(ref_oem.splitlines()[:8] + ref_oem.splitlines()[9:]))