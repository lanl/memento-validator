from mementoweb.validator.pipelines import TimeGate


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    t = TimeGate()
    print(t.validate('http://webarchive.bac-lac.gc.ca:8080/wayback/http://acst-ccst.gc.ca/'))