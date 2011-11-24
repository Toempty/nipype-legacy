import nipype.interfaces.io as nio           # Data i/o
import nipype.interfaces.utility as util     # utility
import nipype.pipeline.engine as pe          # pypeline engine
import nipype.interfaces.camino as camino
import nipype.interfaces.fsl as fsl
import nipype.interfaces.camino2trackvis as cam2trk
import nipype.interfaces.freesurfer as fs    # freesurfer
import nipype.interfaces.cmtk as cmtk
from nipype.workflows.camino.connectivity_mapping import create_connectivity_pipeline
import nipype.algorithms.misc as misc
import inspect
import nibabel as nb
import os, os.path as op                      # system functions
import cmp                                    # connectome mapper

def get_vox_dims(volume):
    import nibabel as nb
    if isinstance(volume, list):
        volume = volume[0]
    nii = nb.load(volume)
    hdr = nii.get_header()
    voxdims = hdr.get_zooms()
    return [float(voxdims[0]), float(voxdims[1]), float(voxdims[2])]

def get_data_dims(volume):
    import nibabel as nb
    if isinstance(volume, list):
        volume = volume[0]
    nii = nb.load(volume)
    hdr = nii.get_header()
    datadims = hdr.get_data_shape()
    return [int(datadims[0]), int(datadims[1]), int(datadims[2])]

def get_affine(volume):
    import nibabel as nb
    nii = nb.load(volume)
    return nii.get_affine()

def get_nsubs(group_list):
    nsubs = 0
    for grp in group_list.keys():
        nsubs += len(group_list[grp])
    return nsubs

def make_inlist(n, from_node):
    inlist = list()
    connections = list()
    for i in range(1,n+1):
        inlist = (from_node,str('in{num}'.format(num=i)))
        connections.append(inlist)
    return inlist, connections

fsl.FSLCommand.set_default_output_type('NIFTI')

def select_aparc(list_of_files):
    for in_file in list_of_files:
        if 'aparc+aseg.mgz' in in_file:
            idx = list_of_files.index(in_file)
    return list_of_files[idx]

def select_aparc_annot(list_of_files):
    for in_file in list_of_files:
        if '.aparc.annot' in in_file:
            idx = list_of_files.index(in_file)
    return list_of_files[idx]

def get_subj_in_group(group_id):
    global group_list
    return group_list[group_id]

def getoutdir(group_id, output_dir):
    import os
    return op.join(op.join(output_dir, 'workingdir'),'%s' % group_id)

def get_nsubs(group_list):
    nsubs = 0
    for grp in group_list.keys():
        nsubs += len(group_list[grp])
    return nsubs

def create_group_cff_pipeline_part1(group_list, group_id, data_dir, subjects_dir, output_dir, template_args_dict=0):
    """Creates a group-level pipeline that does the same connectivity processing as in the
    connectivity_tutorial example script and the camino create_connectivity_pipeline workflow. 

    Given a subject id (and completed Freesurfer reconstruction), diffusion-weighted image,
    b-values, and b-vectors, the workflow will return the subject's connectome
    as a Connectome File Format (CFF) file for use in Connectome Viewer (http://www.cmtk.org)
    as well as the outputs of many other stages of the processing.

    Example
    -------

    >>> import os.path as op
    >>> import nipype.interfaces.freesurfer as fs
    >>> from nipype.workflows.mrtrix import create_connectivity_pipeline
    >>> subjects_dir = op.abspath('freesurfer')
    >>> fs.FSCommand.set_default_subjects_dir(subjects_dir)
    >>> cff = cmonwk.create_connectivity_pipeline("mrtrix_cmtk")
    >>> cff.inputs.inputnode.subjects_dir = subjects_dir
    >>> cff.inputs.inputnode.subject_id = 'subj1'
    >>> cff.inputs.inputnode.dwi = op.abspath('fsl_course_data/fdt/subj1/data.nii.gz')
    >>> cff.inputs.inputnode.bvecs = op.abspath('fsl_course_data/fdt/subj1/bvecs')
    >>> cff.inputs.inputnode.bvals = op.abspath('fsl_course_data/fdt/subj1/bvals')
    >>> cff.run()                 # doctest: +SKIP

    Inputs::

        inputnode.subject_id
        inputnode.subjects_dir
        inputnode.dwi
        inputnode.bvecs
        inputnode.bvals

    Outputs::

        outputnode.connectome
        outputnode.cmatrix
        outputnode.gpickled_network
        outputnode.fa
        outputnode.struct
        outputnode.trace
        outputnode.tracts
        outputnode.tensors

    """
    group_infosource = pe.Node(interface=util.IdentityInterface(fields=['group_id']), name="group_infosource")
    group_infosource.inputs.group_id = group_id
    subject_list = group_list[group_id]
    subj_infosource = pe.Node(interface=util.IdentityInterface(fields=['subject_id']), name="subj_infosource")
    subj_infosource.iterables = ('subject_id', subject_list)
    
    if template_args_dict == 0:
        info = dict(dwi=[['subject_id', 'dwi']],
                    bvecs=[['subject_id','bvecs']],
                    bvals=[['subject_id','bvals']])
    else:
        info = template_args_dict
        
    datasource = pe.Node(interface=nio.DataGrabber(infields=['subject_id'],
                                                   outfields=info.keys()),
                         name = 'datasource')

    datasource.inputs.template = "%s/%s"
    datasource.inputs.base_directory = data_dir
    datasource.inputs.field_template = dict(dwi='%s/%s.nii')
    datasource.inputs.template_args = info

    """
    Create a connectivity mapping workflow
    """
    conmapper = create_connectivity_pipeline("nipype_conmap")
    conmapper.inputs.inputnode.subjects_dir = subjects_dir
    conmapper.base_dir = op.abspath('conmapper')

    datasink = pe.Node(interface=nio.DataSink(), name="datasink")
    datasink.inputs.base_directory = output_dir
    datasink.inputs.container = group_id
    datasink.inputs.cff_dir = getoutdir(group_id, output_dir)

    l1pipeline = pe.Workflow(name="l1pipeline")
    l1pipeline.base_dir = output_dir
    l1pipeline.base_output_dir = group_id
    l1pipeline.connect([(subj_infosource, conmapper,[('subject_id', 'inputnode.subject_id')])])
    l1pipeline.connect([(subj_infosource, datasource,[('subject_id', 'subject_id')])])
    l1pipeline.connect([(datasource, conmapper, [("dwi", "inputnode.dwi"),
                                              ("bvals", "inputnode.bvals"),
                                              ("bvecs", "inputnode.bvecs"),
                                              ])])
    l1pipeline.connect([(conmapper, datasink, [("outputnode.connectome", "@l1output.cff"),
                                              ("outputnode.fa", "@l1output.fa"),
                                              ("outputnode.tracts", "@l1output.tracts"),
                                              ("outputnode.trace", "@l1output.trace"),
                                              ("outputnode.cmatrix", "@l1output.cmatrix"),
                                              ("outputnode.rois", "@l1output.rois"),
                                              ("outputnode.struct", "@l1output.struct"),
                                              ("outputnode.gpickled_network", "@l1output.gpickled_network"),
                                              ("outputnode.mean_fiber_length", "@l1output.mean_fiber_length"),
                                              ("outputnode.fiber_length_std", "@l1output.fiber_length_std"),
                                              ])])
    l1pipeline.connect([(group_infosource, datasink,[('group_id','@group_id')])])
    return l1pipeline

def create_group_cff_pipeline_part2(group_list, group_id, data_dir, subjects_dir, output_dir):
    """
    Level 2 pipeline starts here
    """
    group_infosource = pe.Node(interface=util.IdentityInterface(fields=['group_id']), name="group_infosource")
    group_infosource.inputs.group_id = group_id

    l2infosource = pe.Node(interface=util.IdentityInterface(fields=['group_id']), name='l2infosource')

    l2source = pe.Node(nio.DataGrabber(infields=['group_id'], outfields=['CFFfiles']), name='l2source')
    l2source.inputs.template_args = dict(CFFfiles=[['group_id']])
    l2source.inputs.template=op.join(output_dir,'%s/cff/*/connectome.cff')
    l2source.inputs.base_directory = data_dir

    l2inputnode = pe.Node(interface=util.IdentityInterface(fields=['CFFfiles']), name='l2inputnode')
    MergeCNetworks = pe.Node(interface=cmtk.MergeCNetworks(), name="MergeCNetworks")

    l2datasink = pe.Node(interface=nio.DataSink(), name="l2datasink")
    l2datasink.inputs.base_directory = output_dir
    l2datasink.inputs.container = group_id
    l2datasink.inputs.cff_dir = getoutdir(group_id, output_dir)

    l2pipeline = pe.Workflow(name="l2output")
    l2pipeline.base_dir = op.join(output_dir, 'l2output')
    l2pipeline.connect([(group_infosource, l2infosource,[('group_id','group_id')])])

    l2pipeline.connect([
                        (l2infosource,l2source,[('group_id', 'group_id')]),
                        (l2source,l2inputnode,[('CFFfiles','CFFfiles')]),
                    ])

    l2pipeline.connect([(l2inputnode,MergeCNetworks,[('CFFfiles','in_files')])])
    l2pipeline.connect([(group_infosource,MergeCNetworks,[('group_id','out_file')])])
    l2pipeline.connect([(MergeCNetworks, l2datasink, [('connectome_file', '@l2output')])])
    l2pipeline.connect([(group_infosource, l2datasink,[('group_id','@group_id')])])
    return l2pipeline

def create_group_cff_pipeline_part3(group_list, data_dir ,subjects_dir, output_dir, title='group'):
    """
    Next the groups are combined in the 3rd level pipeline.
    """
    l3infosource = pe.Node(interface=util.IdentityInterface(fields=['group_id']), name='l3infosource')
    l3infosource.inputs.group_id = group_list.keys()
    
    l3source = pe.Node(nio.DataGrabber(infields=['group_id'], outfields=['CFFfiles']), name='l3source')
    l3source.inputs.template_args = dict(CFFfiles=[['group_id','group_id']])
    l3source.inputs.template=op.join(output_dir,'%s/%s.cff')
    
    l3inputnode = pe.Node(interface=util.IdentityInterface(fields=['Group_CFFs']), name='l3inputnode')
    
    MergeCNetworks_grp = pe.Node(interface=cmtk.MergeCNetworks(), name="MergeCNetworks_grp")
    MergeCNetworks_grp.inputs.out_file = title
    
    l3datasink = pe.Node(interface=nio.DataSink(), name="l3datasink")
    l3datasink.inputs.base_directory = output_dir
    
    l3pipeline = pe.Workflow(name="l3output")
    l3pipeline.base_dir = output_dir
    l3pipeline.connect([
                        (l3infosource,l3source,[('group_id', 'group_id')]),
                        (l3source,l3inputnode,[('CFFfiles','Group_CFFs')]),
                    ])

    l3pipeline.connect([(l3inputnode,MergeCNetworks_grp,[('Group_CFFs','in_files')])])
    l3pipeline.connect([(MergeCNetworks_grp, l3datasink, [('connectome_file', '@l3output')])])
    return l3pipeline

def create_group_cff_pipeline_part4(group_list, data_dir, subjects_dir, output_dir, title='group'):
    """
    Level 4 pipeline starts here
    """
    l4infosource = pe.Node(interface=util.IdentityInterface(fields=['group_id1', 'group_id2']), name='l4infosource')
    l4infosource.inputs.group_id1 = group_list.keys()[0]
    l4infosource.inputs.group_id2 = group_list.keys()[1]

    l4info = dict(networks=[['group_id', '']], CMatrices=[['group_id', '']], fibmean=[['group_id', 'mean_fiber_length']],
        fibdev=[['group_id', 'fiber_length_std']])

    l4source_grp1 = pe.Node(nio.DataGrabber(infields=['group_id'], outfields=l4info.keys()), name='l4source_grp1')
    l4source_grp1.inputs.template = '%s/%s'
    l4source_grp1.inputs.field_template=dict(networks=op.join(output_dir,'%s/gpickled_network/*/*%s*.pck'), CMatrices=op.join(output_dir,'%s/cmatrix/*/*%s*.mat'),
        fibmean=op.join(output_dir,'%s/mean_fiber_length/*/*%s*.mat'), fibdev=op.join(output_dir,'%s/fiber_length_std/*/*%s*.mat'))
    l4source_grp1.inputs.base_directory = output_dir
    l4source_grp1.inputs.template_args = l4info

    l4source_grp2 = l4source_grp1.clone(name='l4source_grp2')

    l4inputnode = pe.Node(interface=util.IdentityInterface(fields=['networks_grp1','networks_grp2','CMatrices_grp1','CMatrices_grp2',
        'fibmean_grp1','fibmean_grp2','fibdev_grp1','fibdev_grp2']), name='l4inputnode')

    average_networks_grp1 = pe.Node(interface=cmtk.AverageNetworks(), name='average_networks_grp1')
    average_networks_grp2 = average_networks_grp1.clone('average_networks_grp2')
        
    averagecff = pe.Node(interface=cmtk.CFFConverter(), name="averagecff")
    averagecff.inputs.out_file = title + '_average'

    merge_gpickled_averages = pe.Node(interface=util.Merge(2), name='merge_gpickled_averages')
    merge_gexf_averages = merge_gpickled_averages.clone('merge_gexf_averages')
    
    l4datasink = pe.Node(interface=nio.DataSink(), name="l4datasink")
    l4datasink.inputs.base_directory = output_dir
    
    l4pipeline = pe.Workflow(name="l4output")
    l4pipeline.base_dir = output_dir
    l4pipeline.connect([
                        (l4infosource,l4source_grp1,[('group_id1', 'group_id')]),
                        (l4infosource,l4source_grp2,[('group_id2', 'group_id')]),
                        (l4source_grp1,l4inputnode,[('CMatrices','CMatrices_grp1')]),
                        (l4source_grp2,l4inputnode,[('CMatrices','CMatrices_grp2')]),
                        (l4source_grp1,l4inputnode,[('networks','networks_grp1')]),
                        (l4source_grp2,l4inputnode,[('networks','networks_grp2')]),
                        (l4source_grp1,l4inputnode,[('fibmean','fibmean_grp1')]),
                        (l4source_grp2,l4inputnode,[('fibmean','fibmean_grp2')]),
                        (l4source_grp1,l4inputnode,[('fibdev','fibdev_grp1')]),
                        (l4source_grp2,l4inputnode,[('fibdev','fibdev_grp2')]),
                    ])

    l4pipeline.connect([(l4inputnode, average_networks_grp1,[('networks_grp1','in_files')])])
    l4pipeline.connect([(l4infosource, average_networks_grp1,[('group_id1','group_id')])])
    
    l4pipeline.connect([(l4inputnode, average_networks_grp2,[('networks_grp2','in_files')])])
    l4pipeline.connect([(l4infosource, average_networks_grp2,[('group_id2','group_id')])])
    
    l4pipeline.connect([(average_networks_grp1, merge_gpickled_averages,[('out_gpickled_groupavg','in1')])])
    l4pipeline.connect([(average_networks_grp2, merge_gpickled_averages,[('out_gpickled_groupavg','in2')])])

    l4pipeline.connect([(average_networks_grp1, merge_gexf_averages,[('out_gexf_groupavg','in1')])])
    l4pipeline.connect([(average_networks_grp2, merge_gexf_averages,[('out_gexf_groupavg','in2')])])
    
    l4pipeline.connect([(merge_gpickled_averages, l4datasink, [('out', '@l4output.gpickled')])])
    l4pipeline.connect([(merge_gpickled_averages, averagecff, [('out', 'gpickled_networks')])])
    l4pipeline.connect([(averagecff, l4datasink, [('connectome_file', '@l4output.averagecff')])])

    l4pipeline.connect([(merge_gexf_averages, l4datasink, [('out', '@l4output.gexf')])])
    return l4pipeline