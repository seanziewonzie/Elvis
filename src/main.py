from sage.all import *
from SpaceDecomp import *

class Elvis:
        def main():
                response=SaveOrCreateSpaceDecomp()
                SpaceDecompBranch(response)

        def SaveOrCreateSpaceDecomp()
                reponse =raw_input('Do you want to use a saved space decomposition?')
                return response

        def SpaceDecompBranch(response):
                while reponse !='y' or reponse !='n':
                        print('This is not a valid input. Please type y/n: ')
                        response=SaveOrCreateSpaceDecomp()
                if reponse == 'y':
                        chooseSpaceDecomp()
                if response =='n'
                        createSpaceDecomp()


        if __name__ == "__main__":
                main()


