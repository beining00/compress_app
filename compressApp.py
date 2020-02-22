
import argparse
"""
lowercase, all letters
no space
"""
class myList(list):
    def get(self, index):
        if index >= len(self):
            return -1
        else:
            return self[index]

class CompressApp:

    def __init__(self):

        self.parser = argparse.ArgumentParser(description='File compression program', add_help=True)
        option = self.parser.add_mutually_exclusive_group(required=True)
        option.add_argument("-compress", dest="compress", help="compress a file", action="store")
        option.add_argument("-decompress", dest="decompress", help="decompress a file", action="store")

    def prompt(self):
        """
        receive the command line inputs
        pass the inputs to main to be processed
        """
        args = self.parser.parse_args()
        return self.main(args)

    def main(self,args):
        print("run main")
        print(args)
        if args.compress is not None:
            filename = args.compress
            fp = open(filename, mode="r")
            tobecompressed = fp.readlines()[0]
            fp.close()

            res = self.compress(tobecompressed)

            self.output_2_file([res],   filename + "_c")
        else:
            filename = args.decompress
            fp = open(filename, mode="r")
            tobedecompressed = fp.readlines()[0]
            fp.close()

            res =self.decompress(tobedecompressed)
            self.output_2_file([res], "n_" + filename)




    def output_2_file(self,an_array, filename):
        """
        :param an_array: require each line as an string element of the array
        :param filename: name of the file to be outputed
        """

        # output file
        f = open(filename, "w+")
        for i in range(len(an_array)):
            f.write("%s" % (an_array[i]))

        f.close()
        print("file: " + filename + ' is generated')



    def compress(self, s):
        my_s = s + "$"
        rank = [ord(my_s[i]) for i in range(len(my_s))]
        rank = myList(rank)
        SA = [i for i in range(len(my_s))]

        i = 0.5
        while i <= len(rank):

            i = i * 2
            rank = self.sort_rank(rank, SA,int(i))



        BWT = [None] * len(my_s)

        for i in range(len(BWT)):

            BWT[i]= my_s[SA[i]-1]
        res = self.shrink("".join(BWT))

        return res

    def decompress(self,shrinked_BWT):
        BWT = self.expend(shrinked_BWT)
        count = [0] * 27
        occ = [None] * len(BWT)
        rank =[None] * 27
        res = ""
        for i in range(len(BWT)):

            index = self.get_idx(BWT[i])

            #update occ
            occ[i] = count[index]

            #update count
            count[index] += 1

        # rank of letter in first column
        rank[0] = 0
        for i in range(1,len(rank)):
            rank[i] = count[i-1] + rank[i-1]


        cur_idx = 0
        while True:
            if BWT[cur_idx] == "$":
                break
            ord_index = self.get_idx(BWT[cur_idx])
            res = BWT[cur_idx] + res
            cur_idx= occ[cur_idx] + rank[ord_index]


        return res


    def get_idx(self, letter):
        index = ord(letter) - 96

        if index < 0:
            return 0
        else:
            return index

    def shrink(self, BWT):
        res = ""
        pre = None
        count = 0
        for i in range(len(BWT)):
            if BWT[i] == pre:
                count += 1
            else:
                if count > 0:
                    res += str(count) + pre
                pre = BWT[i]
                count = 1
        if count > 0:
            res += str(count) + pre
        return res

    def expend(self, shrinked_BWT):
        res = ""
        for i in range(0,len(shrinked_BWT),2):

            res += int(shrinked_BWT[i]) * shrinked_BWT[i+1]
        return res


    def sort_rank(self, rank,SA,k):
        SA.sort(key=lambda x:(rank.get(x),rank.get(x+k)))
        tmp = [1] * len(SA)
        for i in range(1,len(SA)):
            if rank[SA[i]] > rank[SA[i-1]]:
                tmp[SA[i]] = tmp[SA[i-1]] + 1
            else:
                if SA[i]+k >= len(rank):
                    this = -1
                else:
                    this = rank[SA[i]+k]

                if SA[i - 1] + k >= len(rank):
                    other = -1
                else:
                    other = rank[SA[i - 1] + k]

                if this > other:
                    tmp[SA[i]] = tmp[SA[i - 1]] + 1
                else:
                    tmp[SA[i]] = tmp[SA[i - 1]]


        return myList(tmp)



if __name__ == "__main__":
    myApp = CompressApp()
    myApp.prompt()
    #args = myApp.parser.parse_args(["-compress", "test"])
    #myApp.main(args)