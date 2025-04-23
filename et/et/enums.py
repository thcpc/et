class Status:
    class __Document_:
        @property
        def Draft(self): return 0

        @property
        def Submit(self): return 1

    class __TaskNode_:
        @property
        def Start(self): return -1

        @property
        def End(self): return -1

    class __Task_:
        @property
        def Todo(self): return 0

        @property
        def Doing(self): return 4

        @property
        def InActive(self): return 1

        @property
        def Terminate(self): return 2

        @property
        def Finished(self): return 3

        @property
        def TransferToOther(self): return 5

    class __Business_:
        @property
        def Pass(self): return 101

        @property
        def Fail(self): return 102

        @property
        def Block(self): return 103

        @property
        def Ignore(self): return 104

    Document = __Document_()
    Task = __Task_()
    TaskNode = __TaskNode_()
    Business = __Business_()


class Name:
    class __DocumentType_:
        @property
        def Auto(self): return "AutoTest"

        @property
        def AutoZh(self): return "自动化用例"

        @property
        def Regression(self): return "RegressionTest"

        @property
        def RegressionZh(self): return "回归用例"

    class __TaskType_:
        @property
        def AssignAutoTask(self): return 0

        @property
        def LinkAutoTask(self): return 1

        @property
        def ExecuteAutoTask(self): return 2

        @property
        def ExecuteRegressionTask(self): return 3

    class __Dispatcher_:
        @property
        def New(self): return "new"

        @property
        def Transfer(self): return "transfer"

        @property
        def Rollback(self): return "roll_back"

    DocumentType = __DocumentType_()
    TaskType = __TaskType_()
    Dispatcher = __Dispatcher_()
