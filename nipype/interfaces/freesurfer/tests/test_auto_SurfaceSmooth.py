# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.interfaces.freesurfer.utils import SurfaceSmooth

def test_SurfaceSmooth_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    cortex=dict(argstr='--cortex',
    usedefault=True,
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    fwhm=dict(argstr='--fwhm %.4f',
    xor=['smooth_iters'],
    ),
    hemi=dict(argstr='--hemi %s',
    mandatory=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    in_file=dict(argstr='--sval %s',
    mandatory=True,
    ),
    out_file=dict(argstr='--tval %s',
    genfile=True,
    ),
    reshape=dict(argstr='--reshape',
    ),
    smooth_iters=dict(argstr='--smooth %d',
    xor=['fwhm'],
    ),
    subject_id=dict(argstr='--s %s',
    mandatory=True,
    ),
    subjects_dir=dict(),
    terminal_output=dict(mandatory=True,
    nohash=True,
    usedefault=True,
    ),
    )
    inputs = SurfaceSmooth.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value

def test_SurfaceSmooth_outputs():
    output_map = dict(out_file=dict(),
    )
    outputs = SurfaceSmooth.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value

