# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.interfaces.fsl.preprocess import SliceTimer

def test_SliceTimer_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    custom_order=dict(argstr='--ocustom=%s',
    ),
    custom_timings=dict(argstr='--tcustom=%s',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    global_shift=dict(argstr='--tglobal',
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    in_file=dict(argstr='--in=%s',
    mandatory=True,
    position=0,
    ),
    index_dir=dict(argstr='--down',
    ),
    interleaved=dict(argstr='--odd',
    ),
    out_file=dict(argstr='--out=%s',
    genfile=True,
    hash_files=False,
    ),
    output_type=dict(),
    slice_direction=dict(argstr='--direction=%d',
    ),
    terminal_output=dict(mandatory=True,
    nohash=True,
    usedefault=True,
    ),
    time_repetition=dict(argstr='--repeat=%f',
    ),
    )
    inputs = SliceTimer.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value

def test_SliceTimer_outputs():
    output_map = dict(slice_time_corrected_file=dict(),
    )
    outputs = SliceTimer.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value

