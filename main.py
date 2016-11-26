from preProcess import PreProcess
from model import Model

def main():
    # print "start running preProcessing.run()"
    # PreProcess().run()
    model = Model()
    model.initData()
    # model.trainModel()
    # model.saveModel()
    # model.gridSearch()
    model.test()

if __name__ == '__main__':
    main()
