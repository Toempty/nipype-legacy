# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.interfaces.freesurfer.preprocess import SynthesizeFLASH

def test_SynthesizeFLASH_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    fixed_weighting=dict(argstr='-w',
    position=1,
    ),
    flip_angle=dict(argstr='%.2f',
    mandatory=True,
    position=3,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    out_file=dict(argstr='%s',
    genfile=True,
    ),
    pd_image=dict(argstr='%s',
    mandatory=True,
    position=6,
    ),
    subjects_dir=dict(),
    t1_image=dict(argstr='%s',
    mandatory=True,
    position=5,
    ),
    te=dict(argstr='%.3f',
    mandatory=True,
    position=4,
    ),
    terminal_output=dict(mandatory=True,
    nohash=True,
    usedefault=True,
    ),
    tr=dict(argstr='%.2f',
    mandatory=True,
    position=2,
    ),
    )
    inputs = SynthesizeFLASH.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value

def test_SynthesizeFLASH_outputs():
    output_map = dict(out_file=dict(),
    )
    outputs = SynthesizeFLASH.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value

