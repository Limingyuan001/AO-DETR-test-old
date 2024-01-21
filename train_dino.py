# Copyright (c) OpenMMLab. All rights reserved.
import argparse
import logging
import os
import os.path as osp

from mmengine.config import Config, DictAction
from mmengine.logging import print_log
from mmengine.registry import RUNNERS
from mmengine.runner import Runner

from mmdet.utils import setup_cache_size_limit_of_dynamo


def parse_args():
    parser = argparse.ArgumentParser(description='Train a detector')
    # parser.add_argument('--config', default='../configs/dino/dino-4scale_r50_8xb2-12e_pixray_mine.py', help='train config file path')
    # parser.add_argument('--work-dir', default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dino/swinL_pixray/test', help='the dir to save logs and models')

    # r50 coco
    # parser.add_argument('--config', default='../configs/dino/dino-4scale_r50_8xb2-12e_coco_mine.py', help='train config file path')
    # parser.add_argument('--work-dir', default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dino/r50_coco/01', help='the dir to save logs and models')

    # r50 pixray
    # parser.add_argument('--config', default='../configs/dino/dino-4scale_r50_8xb2-12e_pixray_mine.py', help='train config file path')
    # parser.add_argument('--work-dir', default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dino/r50_pixray/01', help='the dir to save logs and models')

    # swin-L pixray DINO
    # parser.add_argument('--config', default='../configs/dino/dino-5scale_swin-l_8xb2-12e_pixray_mine_q900.py', help='train config file path')
    # parser.add_argument('--work-dir', default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dino/swinL_pixray_q900/debug', help='the dir to save logs and models')

    # swin-L pixray DINOv2
    # parser.add_argument('--config', default='../configs/dino/dinov2-5scale_swin-l_8xb2-12e_pixray_mine_q900.py',
    #                     help='train config file path')
    # parser.add_argument('--work-dir', default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dinov2/swinL_pixray_q900/65',
    #                     help='the dir to save logs and models')
    # # r50 coco mine2 scale=(1333, 800)
    # parser.add_argument('--config', default='../configs/dino/dino-4scale_r50_8xb2-12e_coco_mine2_all.py', help='train config file path')
    # parser.add_argument('--work-dir', default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dino/swinL_coco_mine2/64', help='the dir to save logs and models')
    # swin-L coco mine2 scale=(1333, 800)
    # parser.add_argument('--config', default='../configs/dino/dino-5scale_swin-l_8xb2-12e_coco_mine2.py',
    #                     help='train config file path')
    # parser.add_argument('--work-dir',
    #                     default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dino/r50_coco_mine2/baseline_backbone',
    #                     help='the dir to save logs and models')
    # swin-L pixray DINOv2 backbone
    # parser.add_argument('--config', default='../configs/dino/dinov2-5scale_swin-l_8xb2-12e_pixray_mine_q900_backbone.py',
    #                     help='train config file path')
    # parser.add_argument('--work-dir', default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dinov2/swinL_pixray_q900/66',
    #                     help='the dir to save logs and models')
    # # r50 coco mine2 scale=(1333, 800)
    # parser.add_argument('--config', default='../configs/dino/dino-4scale_r50_8xb2-12e_coco_mine2.py', help='train config file path')
    # parser.add_argument('--work-dir', default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dinov2/r50_coco/124', help='the dir to save logs and models')
    # r50 pixray backbone
    # parser.add_argument('--config', default='../configs/dino/dino-4scale_r50_8xb2-12e_pixray_mine68.py', help='train config file path')
    # parser.add_argument('--work-dir', default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dino/r50_pixray/debug', help='the dir to save logs and models')
    # swin-l pixray backbone 测swinl的ao-detr pixray config文件命名错误了，虽然写的是coco但是就是pixray
    parser.add_argument('--config', default='../configs/dino/dino-5scale_swin-l_8xb2-12e_coco_mine68.py', help='train config file path')
    # parser.add_argument('--work-dir', default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dino/baseline/AO-DETR-swin-l04', help='the dir to save logs and models')
    parser.add_argument('--work-dir', default='E:\D2E\Projects\DINO_mmdet3\checkpoint/dino/swinl_pixray/138', help='the dir to save logs and models')

    parser.add_argument(
        '--amp',
        action='store_true',
        default=False,
        # default=True,
        help='enable automatic-mixed-precision training')
    parser.add_argument(
        '--auto-scale-lr',
        action='store_true',
        help='enable automatically scaling LR.')
    parser.add_argument(
        '--resume',
        nargs='?',
        type=str,
        const='auto',
        help='If specify checkpoint path, resume from it, while if not '
        'specify, try to auto resume from the latest checkpoint '
        'in the work directory.')
    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.')
    parser.add_argument(
        '--launcher',
        choices=['none', 'pytorch', 'slurm', 'mpi'],
        default='none',
        help='job launcher')
    # When using PyTorch version >= 2.0.0, the `torch.distributed.launch`
    # will pass the `--local-rank` parameter to `tools/train.py` instead
    # of `--local_rank`.
    parser.add_argument('--local_rank', '--local-rank', type=int, default=0)
    args = parser.parse_args()
    if 'LOCAL_RANK' not in os.environ:
        os.environ['LOCAL_RANK'] = str(args.local_rank)

    return args


def main():
    args = parse_args()

    # Reduce the number of repeated compilations and improve
    # training speed.
    setup_cache_size_limit_of_dynamo()

    # load config
    cfg = Config.fromfile(args.config)
    cfg.launcher = args.launcher
    if args.cfg_options is not None:
        cfg.merge_from_dict(args.cfg_options)

    # work_dir is determined in this priority: CLI > segment in file > filename
    if args.work_dir is not None:
        # update configs according to CLI args if args.work_dir is not None
        cfg.work_dir = args.work_dir
    elif cfg.get('work_dir', None) is None:
        # use config filename as default work_dir if cfg.work_dir is None
        cfg.work_dir = osp.join('./work_dirs',
                                osp.splitext(osp.basename(args.config))[0])

    # enable automatic-mixed-precision training
    if args.amp is True:
        optim_wrapper = cfg.optim_wrapper.type
        if optim_wrapper == 'AmpOptimWrapper':
            print_log(
                'AMP training is already enabled in your config.',
                logger='current',
                level=logging.WARNING)
        else:
            assert optim_wrapper == 'OptimWrapper', (
                '`--amp` is only supported when the optimizer wrapper type is '
                f'`OptimWrapper` but got {optim_wrapper}.')
            cfg.optim_wrapper.type = 'AmpOptimWrapper'
            cfg.optim_wrapper.loss_scale = 'dynamic'

    # enable automatically scaling LR
    if args.auto_scale_lr:
        if 'auto_scale_lr' in cfg and \
                'enable' in cfg.auto_scale_lr and \
                'base_batch_size' in cfg.auto_scale_lr:
            cfg.auto_scale_lr.enable = True
        else:
            raise RuntimeError('Can not find "auto_scale_lr" or '
                               '"auto_scale_lr.enable" or '
                               '"auto_scale_lr.base_batch_size" in your'
                               ' configuration file.')

    # resume is determined in this priority: resume from > auto_resume
    if args.resume == 'auto':
        cfg.resume = True
        cfg.load_from = None
    elif args.resume is not None:
        cfg.resume = True
        cfg.load_from = args.resume

    # build the runner from config
    if 'runner_type' not in cfg:
        # build the default runner
        runner = Runner.from_cfg(cfg)
    else:
        # build customized runner from the registry
        # if 'runner_type' is set in the cfg
        runner = RUNNERS.build(cfg)

    # start training
    runner.train()


if __name__ == '__main__':
    main()
