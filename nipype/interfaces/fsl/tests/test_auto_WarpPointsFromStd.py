# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from ....testing import assert_equal
from ..utils import WarpPointsFromStd


def test_WarpPointsFromStd_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    coord_mm=dict(argstr='-mm',
    xor=['coord_vox'],
    ),
    coord_vox=dict(argstr='-vox',
    xor=['coord_mm'],
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    img_file=dict(argstr='-img %s',
    mandatory=True,
    ),
    in_coords=dict(argstr='%s',
    mandatory=True,
    position=-1,
    ),
    out_file=dict(name_source='in_coords',
    name_template='%s_warped',
    output_name='out_file',
    ),
    std_file=dict(argstr='-std %s',
    mandatory=True,
    ),
    terminal_output=dict(nohash=True,
    ),
    transform=dict(argstr='-xfm %s',
    ),
    warp_file=dict(argstr='-warp %s',
    xor=['xfm_file'],
    ),
    xfm_file=dict(argstr='-xfm %s',
    xor=['warp_file'],
    ),
    )
    inputs = WarpPointsFromStd.input_spec()

    for key, metadata in list(input_map.items()):
        for metakey, value in list(metadata.items()):
            yield assert_equal, getattr(inputs.traits()[key], metakey), value


def test_WarpPointsFromStd_outputs():
    output_map = dict(out_file=dict(),
    )
    outputs = WarpPointsFromStd.output_spec()

    for key, metadata in list(output_map.items()):
        for metakey, value in list(metadata.items()):
            yield assert_equal, getattr(outputs.traits()[key], metakey), value
