# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.interfaces.afni.preprocess import TShift

def test_TShift_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    ignore=dict(argstr='-ignore %s',
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    in_file=dict(argstr='%s',
    copyfile=False,
    mandatory=True,
    position=-1,
    ),
    interp=dict(argstr='-%s',
    ),
    out_file=dict(argstr='-prefix %s',
    name_source='in_file',
    name_template='%s_tshift',
    ),
    outputtype=dict(),
    rlt=dict(argstr='-rlt',
    ),
    rltplus=dict(argstr='-rlt+',
    ),
    terminal_output=dict(mandatory=True,
    nohash=True,
    usedefault=True,
    ),
    tpattern=dict(argstr='-tpattern %s',
    ),
    tr=dict(argstr='-TR %s',
    ),
    tslice=dict(argstr='-slice %s',
    xor=['tzero'],
    ),
    tzero=dict(argstr='-tzero %s',
    xor=['tslice'],
    ),
    )
    inputs = TShift.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value

def test_TShift_outputs():
    output_map = dict(out_file=dict(),
    )
    outputs = TShift.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value

