# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.interfaces.fsl.dti import DistanceMap

def test_DistanceMap_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    distance_map=dict(argstr='--out=%s',
    genfile=True,
    hash_files=False,
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    in_file=dict(argstr='--in=%s',
    mandatory=True,
    ),
    invert_input=dict(argstr='--invert',
    ),
    local_max_file=dict(argstr='--localmax=%s',
    hash_files=False,
    ),
    mask_file=dict(argstr='--mask=%s',
    ),
    output_type=dict(),
    terminal_output=dict(mandatory=True,
    nohash=True,
    usedefault=True,
    ),
    )
    inputs = DistanceMap.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value

def test_DistanceMap_outputs():
    output_map = dict(distance_map=dict(),
    local_max_file=dict(),
    )
    outputs = DistanceMap.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value

