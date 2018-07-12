

class PM:
    def  __init__(self,seg_line, page_line):
        self.bitmap = bitmap()
        self.mem = [0]*524288

        self.bitmap.edit(0)
        self.set_seg(seg_line)
        self.set_page(page_line)

    def set_seg(self,seg_line):
        line = seg_line.split()
        for i in range(0,len(line),2):
            s = int(line[i])
            f = int(line[i+1])

            self.mem[s] = f


            if f >= 0:
                frame = f//512
                self.bitmap.edit(frame)
                self.bitmap.edit(frame+1)



    def set_page(self,page_line):
        line = page_line.split()
        for i in range(0, len(line), 3):
            p = int(line[i])
            s = int(line[i+1])
            f = int(line[i+2])

            self.mem[self.mem[s]+p] = f

            if f >= 0:
                frame = f//512
                self.bitmap.edit(frame)


    def read(self,va): ## va:virtual mem items
        s = self.mem[va.s]
        p = self.mem[s+va.p]
        w = p+va.w

        for entry in [s, p]:
            if entry == -1:
                raise Pagefault
            elif entry == 0:
                raise Invalidaddrse
        return w

    def write(self,va):
        seg = self.mem[va.s]

        if seg == 0:
            f = self.bitmap.find_empty(2)
            self.mem[va.s] = f * 512
            self.bitmap.edit(f)
            self.bitmap.edit(f + 1)
            seg = self.mem[va.s]
        elif seg == -1:
            raise Pagefault

        page = self.mem[seg + va.p]
        if page == 0:
            empty_frame = self.bitmap.find_empty(1)
            self.mem[seg + va.p] = empty_frame * 512
            self.bitmap.edit(empty_frame)
            page = self.mem[seg + va.p]
        elif page == -1:
            raise Pagefault

        return page + va.w


class Virtual_address:
    def __init__(self,va_input):
        self.va = va_input & 2**28-1
        self.s = (va_input >> 19) & 2**9 - 1
        self.p = (va_input >> 9) & 2**10 - 1
        self.w = va_input & 2 ** 9 - 1
        self.sp = va_input >> 9


class bitmap:
    def __init__(self):
        self.map = [0]*32
        self.mask = [0] * 32

        self.mask[31] = 1
        for i in range(30, -1, -1):
            self.mask[i] = self.mask[i+1]<<1

    def edit(self,f):
        assert(f < 1024)

        self.map[f // 32] = self.map[f // 32] | self.mask[f % 32]

    def find_empty(self,size):
        for i in range(len(self.map)):
            for j in range(0, 32):
                test1 = self.map[i] & self.mask[j]
                if test1 == 0:
                    if size == 2 and not self.isEmpty(i * 32 + j + 1):
                        continue
                    return i * 32 + j
        return None

    def isEmpty(self, f):
        if f >= 1024:
            return False

        index = f//32
        bit = f%32

        return (self.map[index] & self.mask[bit]) == 0


class TLB:
    def __init__(self):
        self.buffer = []

        self.buffer.append(TLB_entry(0, None, None))
        self.buffer.append(TLB_entry(1, None, None))
        self.buffer.append(TLB_entry(2, None, None))
        self.buffer.append(TLB_entry(3, None, None))

    def update(self,sp,page):
        for entry in self.buffer:
            if entry.LRU == 0:
                entry.sp = sp
                entry.page = page
                entry.LRU = 3

            else:
                entry.LRU -= 1

    def find(self,va): #va: also va items
        sp = va.sp
        w =va.w

        for entry in self.buffer:
            if entry.sp == sp:
                for k in self.buffer:
                    if k.LRU > entry.LRU:
                        k.LRU -= 1
                entry.LRU = 3
                return entry.page + w
        raise TLBMiss


class TLB_entry:
    def __init__(self, LRU, sp, page):
        self.LRU = LRU
        self.sp = sp
        self.page = page


class TLBMiss(Exception):
    pass


class Pagefault(Exception):
    pass


class Invalidaddrse(Exception):
    pass