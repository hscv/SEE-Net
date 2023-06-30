import numpy as np
import cv2

def pos_s_2_bbox(pos, s):
    return [pos[0]-s/2, pos[1]-s/2, pos[0]+s/2, pos[1]+s/2]

def crop_hwc(image, bbox, out_sz, padding=(0, 0, 0)):
    a = (out_sz-1) / (bbox[2]-bbox[0])
    b = (out_sz-1) / (bbox[3]-bbox[1])
    c = -a * bbox[0]
    d = -b * bbox[1]
    mapping = np.array([[a, 0, c],
                        [0, b, d]]).astype(np.float)
    # print ('mapping = ',mapping)
    # mapping =  [[   3.15098484    0.         -641.24511099]
    #  [   0.            3.15098484 -162.29541582]]
    # 3.150985 3.150985 -641.245111 -162.295416 
    # print ('%f %f %f %f' % (a,b,c,d))
    crop = cv2.warpAffine(image, mapping, (out_sz, out_sz), borderMode=cv2.BORDER_CONSTANT) # , borderValue=padding
    return crop

def crop_like_SiamFC(image, bbox, context_amount=0.5, exemplar_size=127, instanc_size=255, padding=(0, 0, 0)):
    target_pos = [(bbox[2]+bbox[0])/2., (bbox[3]+bbox[1])/2.]
    target_size = [bbox[2]-bbox[0], bbox[3]-bbox[1]]
    wc_z = target_size[1] + context_amount * sum(target_size)
    hc_z = target_size[0] + context_amount * sum(target_size)
    s_z = np.sqrt(wc_z * hc_z)
    scale_z = exemplar_size / s_z
    d_search = (instanc_size - exemplar_size) / 2
    pad = d_search / scale_z
    s_x = s_z + 2 * pad

    # center_pos = np.array([bbox[0]+(bbox[2]-1)/2,bbox[1]+(bbox[3]-1)/2])
    # z = get_subwindow(image, center_pos, 127, s_z, padding)
    # x = get_subwindow(image, center_pos, 127, s_x, padding)
    z = crop_hwc(image, pos_s_2_bbox(target_pos, s_z), exemplar_size, padding)
    x = crop_hwc(image, pos_s_2_bbox(target_pos, s_x), instanc_size, padding)
    return z, x

def X2Cube(img, cellNum=4):
    B = [cellNum, cellNum]
    skip = [cellNum, cellNum]
    # Parameters
    M, N = img.shape
    col_extent = N - B[1] + 1
    row_extent = M - B[0] + 1

    # Get Starting block indices
    start_idx = np.arange(B[0])[:, None] * N + np.arange(B[1])

    # Generate Depth indeces
    didx = M * N * np.arange(1)
    start_idx = (didx[:, None] + start_idx.ravel()).reshape((-1, B[0], B[1]))

    # Get offsetted indices across the height and width of input array
    offset_idx = np.arange(row_extent)[:, None] * N + np.arange(col_extent)

    # Get all actual indices & index into input array for final output
    out = np.take(img, start_idx.ravel()[:, None] + offset_idx[::skip[0], ::skip[1]].ravel())
    out = np.transpose(out)
    img = out.reshape(M//cellNum, N//cellNum, cellNum*cellNum)
    return img


def ImagePreDeal_HSI(template,search,template_bbox,search_bbox,cellNum=4):
    frame_HSI = cv2.imread(template, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    im = X2Cube(frame_HSI, cellNum) # (207, 471, 16)
    avg_chans = np.mean(im, axis=(0, 1))
    _, template_image = crop_like_SiamFC(im, template_bbox, instanc_size=511, padding=avg_chans)

    frame_HSI = cv2.imread(search, cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
    im = X2Cube(frame_HSI, cellNum) # (207, 471, 16)
    avg_chans = np.mean(im, axis=(0, 1))
    _, search_image = crop_like_SiamFC(im, search_bbox, instanc_size=511, padding=avg_chans)

    return template_image, search_image


def ImagePreDeal_FC(template_fc,search_fc,template_bbox,search_bbox):
    im = cv2.imread(template_fc)
    avg_chans = np.mean(im, axis=(0, 1))
    _, template_image_FC = crop_like_SiamFC(im, template_bbox, instanc_size=511, padding=avg_chans)

    im = cv2.imread(search_fc)
    avg_chans = np.mean(im, axis=(0, 1))
    _, search_image_FC = crop_like_SiamFC(im, search_bbox, instanc_size=511, padding=avg_chans)

    return template_image_FC, search_image_FC