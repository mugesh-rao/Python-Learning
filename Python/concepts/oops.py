class person :
    def __init__(self,name,sex,profession):
        # data Members
        self.name = name
        self.sex = sex
        self.profession = profession

    # Classes define functions called methods
    def show(self):
        print('Name:',self.name ,'sex:' , self.sex ,' profession:', self.profession)

    #behaviour (method)
    def work(self):
         print(self.name,"working as a " , self.profession)


rao = person('Rao Ji' ,'male' ,'Writer')

rao.show()
rao.work()