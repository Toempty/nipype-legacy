# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.interfaces.slicer.legacy.converters import BSplineToDeformationField

def test_BSplineToDeformationField_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    defImage=dict(argstr='--defImage %s',
    hash_files=False,
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    refImage=dict(argstr='--refImage %s',
    ),
    terminal_output=dict(mandatory=True,
    nohash=True,
    usedefault=True,
    ),
    tfm=dict(argstr='--tfm %s',
    ),
    )
    inputs = BSplineToDeformationField.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value

def test_BSplineToDeformationField_outputs():
    output_map = dict(defImage=dict(),
    )
    outputs = BSplineToDeformationField.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value

