from .deeplab_multi_TM import DeeplabMulti


def get_model(cfg):
    if cfg.model.backbone == "deeplabv2_multi":
        cfg=cfg
        num_target=cfg.NUM_TARGET
        eval_target=cfg.EVAL_TARGET
        from_scratch=cfg.FROM_SCRATCH
        tm=cfg.TM
        model = DeeplabMulti(num_classes=cfg.data.num_classes, init=cfg.model.imagenet_pretrained,tm=tm,num_target=num_target,eval_target=eval_target,from_scratch=from_scratch,cfg=cfg)
        #model = DeeplabMulti(num_classes=cfg.data.num_classes, init=cfg.model.imagenet_pretrained)
        params = model.optim_parameters(lr=cfg.opt.lr)
    else:
        raise NotImplementedError()
    return model, params
