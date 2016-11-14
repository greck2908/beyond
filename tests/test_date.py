#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pytest import raises
from unittest.mock import patch

from datetime import datetime, timedelta, timezone

from space.env.poleandtimes import ScalesDiff
from space.utils.date import Date


def test_creation():

    t = Date(2015, 12, 5)
    assert t.d == 57361
    assert t.s == 0

    t = Date(2015, 12, 5, 12)
    assert t.d == 57361
    assert t.s == 43200

    assert str(t) == "2015-12-05T12:00:00 UTC"
    # to trigger the cache mechanism
    assert str(t) == "2015-12-05T12:00:00 UTC"

    # Datetime object
    t = Date(datetime(2015, 12, 6, 12, 20))
    assert t.d == 57362
    assert t.s == 44400

    # Timezone handling (this is supposend to be the same time as the one just above)
    tz = timezone(timedelta(hours=2))
    t = Date(datetime(2015, 12, 6, 14, 20, tzinfo=tz))
    assert t.d == 57362
    assert t.s == 44400

    # Date object
    t2 = Date(t)
    assert t2.d == t.d
    assert t2.s == t.s

    # Julian day
    t = Date(57388, 0)
    assert t.d == 57388
    assert t.s == 0
    assert t.datetime == datetime(2016, 1, 1)

    t = Date(57388)
    assert t.d == 57388
    assert t.s == 0.

    t = Date(57388.5)
    assert t.d == 57388
    assert t.s == 43200

    # Wrong number of arguments
    with raises(TypeError):
        t = Date((2015, 12, 6))

    with raises(ValueError):
        t = Date(2015, 12, 6, 16, 52, 37, 2156, 'utc')

    # Scale
    t = Date(2015, 12, 6, 16, 52, 37, 2156, scale='TAI')

    # Unknown scale
    with raises(ValueError):
        t = Date(2015, 12, 6, 16, 52, 37, 2156, scale='unknown')

    t = Date.now()
    assert t.d > 57373

    with raises(TypeError):
        t.d = 5
        t.s = 32.


def test_operations():
    t1 = Date(2015, 12, 6)

    t2 = t1 + timedelta(hours=2)
    assert t2.d == t1.d
    assert t2.s == t1.s + 2 * 3600

    with raises(TypeError):
        t2 = t1 + 1

    t2 = t1 - timedelta(hours=12)
    assert t2.d == t1.d - 1
    assert t2.s == 43200.

    t2 = t1 - datetime(2015, 12, 4)
    assert type(t2) is timedelta
    assert t2.days == 2

    t2 = t1 - Date(2015, 12, 4)
    assert type(t2) is timedelta
    assert t2.days == 2

    with raises(TypeError):
        t2 = t1 - 2.5


def test_change_scale():

    with patch('space.utils.date.get_timescales') as m:
        m.return_value = ScalesDiff(0.1242558, 36.0)

        t = Date(2015, 12, 6)  # UTC object
        assert str(t.scale) == "UTC"

        t2 = t.change_scale('TT')
        assert str(t2) == "2015-12-06T00:01:08.184000 TT"

        t3 = t.change_scale('GPS')
        assert str(t3) == "2015-12-06T00:00:17 GPS"

        t4 = t.change_scale('UT1')
        assert str(t4) == "2015-12-06T00:00:00.124256 UT1"

        with raises(ValueError):
            t.change_scale('unknown')


def test_julian():

    with patch('space.utils.date.get_timescales') as m:
        m.return_value = ScalesDiff(0.10362957986110499, 36.0)

        t = Date(2015, 12, 18, 22, 25)
        assert t.mjd == 57374.93402777778
        assert t.jd == 2457375.434027778
        assert t.change_scale('TT').julian_century == 0.1596286055289367


def test_comparison():

    with patch('space.utils.date.get_timescales') as m:
        m.return_value = ScalesDiff(0.10362957986110499, 36.0)

        # Same scale
        t1 = Date(2016, 11, 14)
        t2 = Date(2016, 11, 14, 12)
        assert t2 > t1

        # Different scale
        t1 = Date(2016, 11, 14)     # 00:00:36 in TAI
        t2 = Date(2016, 11, 14, scale='TAI')

        assert t2 < t1
        assert t1 > t2

        t1 = Date(2016, 11, 14)
        t2 = Date(2016, 11, 14, 0, 0, 36, scale='TAI')
        assert t1 == t2
        assert t1 >= t2
        assert t1 <= t2
