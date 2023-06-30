# Copyright (c) SenseTime. All Rights Reserved.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import torch
import torch.nn as nn
import torch.nn.functional as F

from siamban.core.config import cfg
from siamban.models.loss import select_cross_entropy_loss, select_iou_loss
from siamban.models.backbone import get_backbone
from siamban.models.head import get_ban_head
from siamban.models.neck import get_neck

splitNum = 8
class Channel_attention_net_pre(nn.Module): # get initial w0
    def __init__(self, channel=25, reduction=4,train=False):
        super(Channel_attention_net_pre, self).__init__()
        self.encoder = nn.Sequential(nn.Linear(channel, channel//2,bias=True),
                                     nn.ReLU(inplace=False),
                                     nn.Linear(channel//2, channel//4,bias=True))

        self.decoder = nn.Sequential(nn.Linear(channel//4, channel//2,bias=True),
                                     nn.ReLU(inplace=False),
                                     nn.Linear(channel//2, channel,bias=True)
                                     )
        self.soft = nn.Softmax(dim=-1)

    def forward(self, x):
        b, c, w, h = x.size()
        c1 = x.view(b,c,-1)
        c2 = c1.permute(0,2,1)
        res1 = self.encoder(c2)
        res2 = self.decoder(res1)
        res2 = res2 / res2.max()
        res2 = self.soft(res2)
        res = res2.permute(0,2,1)
        att = res.view(b,c,w,h)
        y = res.mean(dim=2)
        y = y.view(b,c,1)
        ty = y.permute(0,2,1)
        w = torch.bmm(y,ty)
        return w

class Channel_attention_net(nn.Module):

    def __init__(self, channel=25, reduction=4):
        super(Channel_attention_net, self).__init__()

        self.encoder = nn.Sequential(nn.Linear(channel, channel*2,bias=True),
                                     nn.ReLU(inplace=False),
                                     nn.Linear(channel*2, channel*4,bias=True)
                                     )

        self.decoder = nn.Sequential(nn.Linear(channel*4, channel*2,bias=True),
                                     nn.ReLU(inplace=False),
                                     nn.Linear(channel*2, channel,bias=True)
                                     )
        self.soft = nn.Softmax(dim=-1)

        self.pre_channel_model = Channel_attention_net_pre()

    def get_channel_fea(self, w):
        w1 = self.encoder(w)
        w2 = self.decoder(w1)
        return w2

    def forward(self, x):
        b, c, w, h = x.size()

        tx = x.view(b,c,-1)
        tx_t = tx.permute(0,2,1)

        w0 = self.pre_channel_model(x)
        for i in range(c):
            w0[:,i,i] = 0.0
        w0 = w0/w0.max()

        tt = self.get_channel_fea(w0)
        if tt.max() > 0:
            tt = (tt - tt.min()) / tt.max()
        else:
            tt = (tt.min() - tt) / tt.max()
        w1 = w0 + tt
        for i in range(c):
            w1[:,i,i] = 0.0
        w1 = w1 / w1.max()

        tt = self.get_channel_fea(w1)
        if tt.max() > 0:
            tt = (tt - tt.min()) / tt.max()
        else:
            tt = (tt.min() - tt) / tt.max()
        w2 = w1 + tt
        for i in range(c):
            w2[:,i,i] = 0.0
        w2 = w2 / w2.max()

        tt = self.get_channel_fea(w2)
        if tt.max() > 0:
            tt = (tt - tt.min()) / tt.max()
        else:
            tt = (tt.min() - tt) / tt.max()
        w3 = w2 + tt 
        for i in range(c):
            w3[:,i,i] = 0.0
        w3 = w3 / w3.max()
        y = w3.mean(dim=-1)
        orderY = torch.sort(y, dim=-1, descending=True, out=None)
        res = x
        return res,w3,orderY


class ModelBuilder(nn.Module):
    def __init__(self):
        super(ModelBuilder, self).__init__()

        # build backbone
        self.backbone = get_backbone(cfg.BACKBONE.TYPE,
                                     **cfg.BACKBONE.KWARGS)

        # build adjust layer
        if cfg.ADJUST.ADJUST:
            self.neck = get_neck(cfg.ADJUST.TYPE,
                                 **cfg.ADJUST.KWARGS)

        # build ban head
        if cfg.BAN.BAN:
            self.head = get_ban_head(cfg.BAN.TYPE,
                                     **cfg.BAN.KWARGS)
        if True:
            self.chanModel = Channel_attention_net().cuda()

    def _split_Channel(self,feat_channel,order):
        res = []
        b = feat_channel.size()[0]
        for i in range(splitNum):
            gg = feat_channel[None,0,order[0,i*3:i*3+3],:,:]
            for k in range(1,b):
                gg = torch.cat((gg,feat_channel[None,k,order[k,i*3:i*3+3],:,:]),dim=0)
            res.append(gg)
        return res

    def template(self, z):
        falseColor = False
        if falseColor:
            zf = self.backbone(z)
            if cfg.ADJUST.ADJUST:
                zf = self.neck(zf)
            self.zf = zf
        else:
            res, w3, orderY = self.chanModel(z)
            order = orderY[1]
            zArr = self._split_Channel(res,order)
            zfArr = [self.backbone(z) for z in zArr]
            self.zfArr = []
            if cfg.ADJUST.ADJUST:
                for zf in zfArr:
                    zf = self.neck(zf)
                    self.zfArr.append(zf)
            else:
                self.zfArr = zfArr
        

    def track(self, x):
        falseColor = False
        if falseColor:
            xf = self.backbone(x)
            if cfg.ADJUST.ADJUST:
                xf = self.neck(xf)
            clsArr = []
            locArr = []
            cls, loc = self.head(self.zf, xf)
            clsArr.append(cls)
            locArr.append(loc)
            return {
                    'cls': clsArr,
                    'loc': locArr
                   }
        else:
            res, w, orderY = self.chanModel(x)
            order = orderY[1]
            xArr = self._split_Channel(res,order)

            xfArr = [self.backbone(x) for x in xArr]
            if cfg.ADJUST.ADJUST:
                xfArr = [self.neck(xf) for xf in xfArr]
            clsArr = []
            locArr = []
            for i in range(8):
                cls, loc = self.head(self.zfArr[i], xfArr[i])
                clsArr.append(cls)
                locArr.append(loc)
            return {
                    'cls': clsArr,
                    'loc': locArr,
                    'order': orderY
                   }


    def log_softmax(self, cls):
        if cfg.BAN.BAN:
            cls = cls.permute(0, 2, 3, 1).contiguous()
            cls = F.log_softmax(cls, dim=3)
        return cls

    def forward(self, data):
        """ only used in training
        """
        template = data['template'].cuda()
        search = data['search'].cuda()
        label_cls = data['label_cls'].cuda()
        label_loc = data['label_loc'].cuda()

        # get feature
        res_template, w, orderY_template = self.chanModel(template) 
        b,c,width,height = res_template.size()
        tx_template = res_template.view(b,c,-1)
        wx_template = torch.bmm(w,tx_template)
        rect_loss_template = F.mse_loss(wx_template, tx_template)
        rect_loss_template = rect_loss_template / (width*height)
        order_template = orderY_template[1]
        templateArr = self._split_Channel(res_template,order_template)
        
        res_search, w, orderY_search = self.chanModel(search)
        b,c,width,height = res_search.size()
        tx_search = res_search.view(b,c,-1)
        wx_search = torch.bmm(w,tx_search)
        rect_loss_search = F.mse_loss(wx_search, tx_search)
        rect_loss_search = rect_loss_search / (width*height)
        order_search = orderY_search[1]
        searchArr = self._split_Channel(res_search,order_search)

        penalty = orderY_search[0].sum(dim=0) * 1.0 / order_search.size()[0]
        pe_arr = []
        for k in range(splitNum):
            pe_arr.append(penalty[k*3:(k+1)*3].sum())

        clsArr = []
        locArr = []
        for i in range(splitNum):
            z = templateArr[i]
            x = searchArr[i]
            zf = self.backbone(z)
            xf = self.backbone(x)
            if cfg.ADJUST.ADJUST:
                zf = self.neck(zf)
                xf = self.neck(xf)
            cls, loc = self.head(zf, xf)
            clsArr.append(cls)
            locArr.append(loc)

        # get loss

        # cls loss with cross entropy loss
        for i in range(splitNum):
            cls = clsArr[i]
            loc = locArr[i]

            cls = self.log_softmax(cls)
            if i == 0:
                cls_loss = select_cross_entropy_loss(cls, label_cls) * pe_arr[i]
                loc_loss = select_iou_loss(loc, label_loc, label_cls) * pe_arr[i]
            else:
                cls_loss += select_cross_entropy_loss(cls, label_cls) * pe_arr[i]
                loc_loss += select_iou_loss(loc, label_loc, label_cls) * pe_arr[i]

        sum_pe_arr = 0
        for i in range(splitNum):
            sum_pe_arr += pe_arr[i]
        cls_loss = cls_loss / sum_pe_arr
        loc_loss = loc_loss / sum_pe_arr
        outputs = {}
        outputs['total_loss'] = cfg.TRAIN.CLS_WEIGHT * cls_loss + \
            cfg.TRAIN.LOC_WEIGHT * loc_loss + 0.014*(rect_loss_search+rect_loss_template)
        outputs['cls_loss'] = cls_loss
        outputs['loc_loss'] = loc_loss
        outputs['rec_loss'] = rect_loss_search+rect_loss_template

        return outputs

