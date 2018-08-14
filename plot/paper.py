import matplotlib.pyplot as plt

class Paper:
    def __init__(self,size = 'A4',orientation ='portrait',suptitle='' ):
        self.suptitle = suptitle
        self.size = size
        self.orientation = orientation
        self.suptitle = suptitle

    def get_a_figure(self):
        size = self.size; orientation = self.orientation;
        suptitle = self.suptitle
        if size == 'A4' and orientation == 'portrait':
            fig = plt.figure(figsize=(8.27,11.65))
        elif size=='A3' and orientation =='portrait':
            fig = plt.figure(figsize=(11.69,16.53))
        elif size == 'A4' and orientation == 'landscape':
            fig = plt.figure(figsize=(11.65,8.27))
        elif size=='A3' and orientation =='landscape':
            fig = plt.figure(figsize=(16.53,11.69))
        else:
            ValueError('A very specific bad thing happened.')
        return fig


