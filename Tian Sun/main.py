#Tian Sun
#57749958


from usage import PM, Virtual_address, bitmap, TLBMiss, TLB, TLB_entry,Pagefault,Invalidaddrse
from sys import argv

class Shell:
    def __init__(self, init_path, input_path,output_path):
        with open(init_path, "r") as init:
            seg_line = init.readline()
            page_line = init.readline()
        
        self.output_path = output_path

        self.mem = PM(seg_line,page_line);
        self.TLB = TLB()

        with open(input_path, "r") as input_file:
            self.commands = input_file.readline().split()
        self.tlb = False
        self.run_commands()
        self.tlb = True
        self.mem = PM(seg_line, page_line);
        self.TLB = TLB()
        self.run_commands(self.tlb)





    def run_commands(self,tlb=False):
        result = []

        for i in range(0,len(self.commands),2):
            hit = False
            command = int(self.commands[i])
            va = Virtual_address(int(self.commands[i+1]))

            if tlb:
                try:
                    addr = self.TLB.find(va)
                    result.append("h ")
                    hit = True
                    result.append(str(addr)+" ")
                except TLBMiss:
                    result.append("m ")
            try:
                if command == 1:
                    addr = self.mem.write(va)
                    if not hit:
                        result.append(str(addr)+" ")
                else:
                    addr = self.mem.read(va)
                    if not hit:
                        result.append(str(addr)+" ")
                if tlb:
                    self.TLB.update(va.sp,addr-va.w)
            except Pagefault:
                result.append("pf ")
            except Invalidaddrse:
                result.append("err ")
        if not tlb:
            output_path_n = self.output_path + "/57749958.txt"
            with open(output_path_n,"w") as output_file:
                output_str = "".join(result)
                output_file.write(output_str)
        else:
            output_path_n = self.output_path + "/57749958_tlb.txt"
            with open(output_path_n,"w") as output_file:
                output_str = "".join(result)
                output_file.write(output_str)



if __name__ == "__main__":
    init_path = argv[1]
    input_path = argv[2]
    output_path = argv[3]

    shell = Shell(init_path,input_path,output_path)





