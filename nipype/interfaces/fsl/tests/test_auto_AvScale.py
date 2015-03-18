# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.interfaces.fsl.utils import AvScale

def test_AvScale_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    mat_file=dict(argstr='%s',
    position=0,
    ),
    output_type=dict(),
    terminal_output=dict(mandatory=True,
    nohash=True,
    usedefault=True,
    ),
    )
    inputs = AvScale.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value

def test_AvScale_outputs():
    output_map = dict(average_scaling=dict(),
    backward_half_transform=dict(),
    determinant=dict(),
    forward_half_transform=dict(),
    left_right_orientation_preserved=dict(),
    rotation_translation_matrix=dict(),
    scales=dict(),
    skews=dict(),
    )
    outputs = AvScale.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value

