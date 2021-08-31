# dataset settings
dataset_type = 'CocoPanopticDataset'
data_root = 'data/coco/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='LoadPanopticAnnotations',
        with_bbox=True,
        with_mask=True,
        with_seg=True),
    dict(type='Resize', img_scale=(1333, 800), keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='SegRescale', scale_factor=1 / 4),
    dict(type='DefaultFormatBundle'),
    dict(
        type='Collect',
        keys=['img', 'gt_bboxes', 'gt_labels', 'gt_masks', 'gt_semantic_seg']),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1333, 800),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]
data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        ann_file=['../fold/annotation_1.json', '../fold/annotation_2.json', '../fold/annotation_3.json'],
        img_prefix='../fold/train/',
        seg_prefix=['../fold/train_label/fold1/', '../fold/train_label/fold2/', '../fold/train_label/fold3/'],
        pipeline=train_pipeline),
    val=dict(
        type=dataset_type,
        ann_file='../fold/annotation_0.json',
        img_prefix='../fold/train/',
        seg_prefix='../fold/train_label/fold0/',
        pipeline=test_pipeline),
    test=dict(
        type=dataset_type,
        ann_file='../fold/annotation_0.json',
        img_prefix='../fold/train/',
        seg_prefix='../fold/train_label/fold0/',
        pipeline=test_pipeline))
evaluation = dict(interval=1, metric=['pq'])
