import pytest
import iss
import numpy as np


def test_1D():
    x = np.array( [0,1,2,3,4] )
    ISS = iss.Iss()
    ISS.compute(x)

    def get( *comp ):
        return ISS._sig[:,ISS._words.index( comp )]

    np.testing.assert_array_equal( x[1:], get(1), get(2), get(3) )
    np.testing.assert_array_equal( [0, 1, 3, 6], get(1,1) )

    ISS.compute( np.array( [0,2,4,6,8] ) )
    np.testing.assert_array_equal( [2,4,6,8], get(1) )
    np.testing.assert_array_equal( [4,8,12,16], get(2) )
