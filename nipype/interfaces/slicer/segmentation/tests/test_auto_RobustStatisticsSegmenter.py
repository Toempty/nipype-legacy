# AUTO-GENERATED by tools/checkspecs.py - DO NOT EDIT
from nipype.testing import assert_equal
from nipype.interfaces.slicer.segmentation.specialized import RobustStatisticsSegmenter

def test_RobustStatisticsSegmenter_inputs():
    input_map = dict(args=dict(argstr='%s',
    ),
    curvatureWeight=dict(argstr='--curvatureWeight %f',
    ),
    environ=dict(nohash=True,
    usedefault=True,
    ),
    expectedVolume=dict(argstr='--expectedVolume %f',
    ),
    ignore_exception=dict(nohash=True,
    usedefault=True,
    ),
    intensityHomogeneity=dict(argstr='--intensityHomogeneity %f',
    ),
    labelImageFileName=dict(argstr='%s',
    position=-2,
    ),
    labelValue=dict(argstr='--labelValue %d',
    ),
    maxRunningTime=dict(argstr='--maxRunningTime %f',
    ),
    originalImageFileName=dict(argstr='%s',
    position=-3,
    ),
    segmentedImageFileName=dict(argstr='%s',
    hash_files=False,
    position=-1,
    ),
    terminal_output=dict(mandatory=True,
    nohash=True,
    usedefault=True,
    ),
    )
    inputs = RobustStatisticsSegmenter.input_spec()

    for key, metadata in input_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(inputs.traits()[key], metakey), value

def test_RobustStatisticsSegmenter_outputs():
    output_map = dict(segmentedImageFileName=dict(position=-1,
    ),
    )
    outputs = RobustStatisticsSegmenter.output_spec()

    for key, metadata in output_map.items():
        for metakey, value in metadata.items():
            yield assert_equal, getattr(outputs.traits()[key], metakey), value

