class Descriptions:
    @staticmethod
    def graph_one():
        description = "This graph displays energy consumption data from 81 locations across the UNCG campus. " \
                      "Choose to compare actual data between multiple locations or compare the predicted values " \
                      "with the actual for a single meter."
        return description

    @staticmethod
    def graph_two():
        description = "Using data from 2015 to 2019, models were generated to predict energy consumption in " \
                      "2020. This graph allows you compare the predictions with the observed values to gauge our " \
                      "models' accuracy."
        return description

    @staticmethod
    def map():
        description = "Hovering over a building on this map allows you to view its average energy consumption over " \
                      "the last 24 hours of recorded data. It also displays the predicted consumption."
        return description
