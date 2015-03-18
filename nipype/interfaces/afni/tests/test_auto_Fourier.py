# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.interfaces.afni.preprocess import Fourier

def test_Fourier_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    highpass=dict(argstr='-highpass %f',
    mandatory=True,
    position=1,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    in_file=dict(argstr='%s',
    copyfile=False,
    mandatory=True,
    position=-1,
    ),
    lowpass=dict(argstr='-lowpass %f',
    mandatory=True,
    position=0,
    ),
    out_file=dict(argstr='-prefix %s',
    name_source='in_file',
    name_template='%s_fourier',
    ),
    outputtype=dict(),
    terminal_output=dict(mandatory=True,
    nohash=True,
    usedefault=True,
    ),
    )
    inputs = Fourier.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value

def test_Fourier_outputs():
    output_map = dict(out_file=dict(),
    )
    outputs = Fourier.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value

