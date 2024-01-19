import cv2, os
import numpy as np

class Watermark:
    sig_size = 100

    @staticmethod
    def __gene_signature(wm, size):
        wm = cv2.resize(wm, (size, size))
        wm = np.where(wm < np.mean(wm), 0, 1)
        return wm

    def inner_embed(self, B, signature):
        pass

    def inner_extract(self, B):
        pass

    def embed(self, cover, wm):
        B = None
        img = None
        signature = None

        if len(cover.shape) > 2:
            img = cv2.cvtColor(cover, cv2.COLOR_BGR2YUV)
            signature = self.__gene_signature(wm, self.sig_size).flatten()
            B = img[:, :, 0]

        if len(cover.shape) > 2:
            img[:, :, 0] = self.inner_embed(B, signature)
            cover = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
        else:
            cover = B
        return cover

    def embed_detail(self, cover, wm):
        B = None
        img = None
        signature = None
        embed_pos = None
        itx = None
        ity = None
        v_1 = None
        v_2 = None
        v_3 = None
        v_4 = None
        res = None

        if len(cover.shape) > 2:
            img_ori = cover
            img = cv2.cvtColor(cover, cv2.COLOR_BGR2YUV)
            signature = self.__gene_signature(wm, self.sig_size).flatten()
            B = img[:, :, 0]
            img_yuv, sign_flat, res_b = img, signature, B
            ww, wh = B.shape[:2]
            # img_p, sign_p, B_p = img, signature, B
        if len(cover.shape) > 2:
            process = self.inner_embed_detail(B, signature)
            img[:, :, 0] = process[0]
            embed_pos = process[1]
            itx = process[2]
            ity = process[3]
            v_1 = process[4]
            v_2 = process[5]
            v_3 = process[6]
            v_4 = process[7]
            res = process[8]
            cover = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
            img_a, cov_a = img, cover
        else:
            cover = B
        return img_ori, img_yuv, sign_flat, res_b, ww, wh, embed_pos, itx, ity, v_1, v_2, v_3, v_4, res

    def extract(self, wmimg):
        B = None
        if len(wmimg.shape) > 2:
            (B, G, R) = cv2.split(cv2.cvtColor(wmimg, cv2.COLOR_BGR2YUV))
        else:
            B = wmimg
        ext_sig = self.inner_extract(B)[0]
        ext_sig = np.array(ext_sig).reshape((self.sig_size, self.sig_size))
        ext_sig = np.where(ext_sig == 1, 255, 0)
        return ext_sig