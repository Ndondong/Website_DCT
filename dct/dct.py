import cv2
import numpy as np

from .watermark import Watermark

class DCT_Watermark(Watermark):
    def __init__(self):
        self.Q = 10 
        self.size = 2

    def inner_embed(self, B: np.ndarray, signature):
        sig_size = self.sig_size
        size = self.size

        w, h = B.shape[:2]
        embed_pos = [(0, 0)]
        if w > 2 * sig_size * size:
            embed_pos.append((w-sig_size*size, 0))
        if h > 2 * sig_size * size:
            embed_pos.append((0, h-sig_size*size))
        if len(embed_pos) == 3:
            embed_pos.append((w-sig_size*size, h-sig_size*size))

        print(embed_pos)

        for x, y in embed_pos:
            for i in range(x, x+sig_size * size, size):
                for j in range(y, y+sig_size*size, size):
                    v = np.float32(B[i:i + size, j:j + size])
                    v = cv2.dct(v)

                    v[size-1, size-1] = self.Q * \
                        signature[((i-x)//size) * sig_size + (j-y)//size]
                    v = cv2.idct(v)

                    maximum = max(v.flatten())
                    minimum = min(v.flatten())
                    if maximum > 255:
                        v = v - (maximum - 255)
                    if minimum < 0:
                        v = v - minimum
                    B[i:i+size, j:j+size] = v
        print(embed_pos)
        return B

    def inner_embed_detail(self, B: np.ndarray, signature):
        sig_size = self.sig_size
        size = self.size

        w, h = B.shape[:2]
        embed_pos = [(0, 0)]
        if w > 2 * sig_size * size:
            embed_pos.append((w-sig_size*size, 0))
        if h > 2 * sig_size * size:
            embed_pos.append((0, h-sig_size*size))
        if len(embed_pos) == 3:
            embed_pos.append((w-sig_size*size, h-sig_size*size))

        iterate_x = []
        iterate_y = []
        v_1 = []
        v_2 = []
        v_3 = []
        v_4 = []
        res = []

        for x, y in embed_pos:
            for i in range(x, x+sig_size * size, size):
                iterate_x.append(x+sig_size * size)
                for j in range(y, y+sig_size*size, size):
                    iterate_y.append(y+sig_size*size)
                    v = np.float32(B[i:i + size, j:j + size])
                    v_1.append(v)
                    v = cv2.dct(v)
                    v_2.append(v)
                    v[size-1, size-1] = self.Q * \
                        signature[((i-x)//size) * sig_size + (j-y)//size]
                    v_3.append(v)
                    v = cv2.idct(v)
                    v_4.append(v)
                    maximum = max(v.flatten())
                    minimum = min(v.flatten())
                    if maximum > 255:
                        v = v - (maximum - 255)
                    if minimum < 0:
                        v = v - minimum
                    B[i:i+size, j:j+size] = v
                    res.append(B[i:i+size, j:j+size])
            # print('x {}; y {}'.format(x,y), file=sys.stderr)
        return B, embed_pos, iterate_x, iterate_y, v_1[:10], v_2[:10], v_3[:10], v_4[:10], res[:10]

    def inner_extract(self, B):
        sig_size = 100
        size = self.size

        ext_sig = np.zeros(sig_size**2, dtype=int)

        for i in range(0, sig_size * size, size):
            for j in range(0, sig_size * size, size):
                v = cv2.dct(np.float32(B[i:i+size, j:j+size]))
                if v[size-1, size-1] > self.Q / 2:
                    ext_sig[(i//size) * sig_size + j//size] = 1

        print(ext_sig)
        return [ext_sig]