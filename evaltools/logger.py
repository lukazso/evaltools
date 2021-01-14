import pandas as pd


class PerformanceLogger(object):
    def __init__(self, parameters):
        self.df = pd.DataFrame(columns=parameters)

    def add(self, **kwargs):
        self.df = self.df.append(kwargs)

    def save(self, path):
        self.df.to_csv(path)