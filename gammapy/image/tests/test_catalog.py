# Licensed under a 3-clause BSD style license - see LICENSE.rst
from __future__ import absolute_import, division, print_function, unicode_literals
from numpy.testing import assert_allclose
from astropy.units import Quantity
from astropy.wcs import WCS
from ...utils.testing import requires_dependency, requires_data
from .. import catalog
from ...image import make_empty_image
from ...irf import EnergyDependentTablePSF
from ...data import SpectralCube
from ...datasets import FermiGalacticCenter


def test_extended_image():
    # TODO: implement me
    pass


@requires_data('gammapy-extra')
def test_source_image():
    reference_hdu = make_empty_image(10, 10, 1)
    reference_wcs = WCS(reference_hdu.header)
    energy = Quantity([10, 500], 'GeV')
    reference = SpectralCube(data=reference_hdu.data,
                             wcs=reference_wcs, energy=energy)

    psf_file = FermiGalacticCenter.filenames()['psf']
    psf = EnergyDependentTablePSF.read(psf_file)

    image, energies = catalog._source_image(catalog='1FHL',
                                            reference_cube=reference,
                                            total_flux=True)

    actual = image.sum()
    # Flux of sources within a 10x10 deg region about Galactic Center
    expected = 1.6098631760996795e-07
    assert_allclose(actual, expected)


@requires_dependency('scipy')
@requires_data('gammapy-extra')
def test_catalog_image():
    reference_hdu = make_empty_image(10, 10, 1)
    reference_wcs = WCS(reference_hdu.header)
    energy = Quantity([10, 500], 'GeV')

    psf_file = FermiGalacticCenter.filenames()['psf']
    psf = EnergyDependentTablePSF.read(psf_file)

    out_cube = catalog.catalog_image(reference_hdu, psf, catalog='1FHL',
                                     source_type='point', total_flux=True,
                                     sim_table=None)

    actual = out_cube.data.sum()

    # Ensures flux is consistent following PSF convolution to within 1%
    expected = 1.6098631760996795e-07
    assert_allclose(actual, expected, rtol=0.01)


@requires_data('gammapy-extra')
def test_catalog_table():
    # Checks catalogs are loaded correctly

    table_1fhl = catalog.catalog_table('1FHL')
    assert len(table_1fhl) == 514

    table_2fgl = catalog.catalog_table('2FGL')
    assert len(table_2fgl) == 1873
