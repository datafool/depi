
import matplotlib.pyplot as plt
import numpy as np 

class VisualizeMRI:
    def __init__(self, image_list):
        """ Class to visulaize set of MRI images. As this class is intended to be used in jupyter notebook,
            so maximum of 4 MRI images can be visualized and compared at a time. Just instantiate the class with 
            a single or list of MRI images. MRI images should be numpy array.
            Example:
            To visualize one image: VisualizeMRI([img1])
            To visualize more than one image: Visulaize([img1, img2,])

        """
        if not isinstance(image_list, list):
            image_list = list(image_list)
            
        if len(image_list) > 4:
            raise ValueError("Maximum of 4 images can be analyzed in 1 step")
        if len(image_list) == 0:
            raise ValueError("Provide atleast 1 image for visualization")
            
        self.fig_size = [(6, 2), (6, 4), (6, 6), (6,8)]
            
        self.image_list = image_list
        self.keys = list('qwertyuiopas')
        self.ind = [0, 1, 2]*4
        self.keys_mapping = {k: self.ind[i] for i, k in enumerate(self.keys)}
        self.remove_keymap_conflicts(set(self.keys))
        self.multi_slice_viwer()
        
    def remove_keymap_conflicts(self, new_keys):
        for prop in plt.rcParams:
            if prop.startswith('keymap.'):
                keys = plt.rcParams[prop]
                remove_list = set(keys) & new_keys
                for key in remove_list:
                    keys.remove(key)
                    
    def multi_slice_viwer(self):
        image_mapper = {0: 'saggital', 1:'coronal', 2: 'transverse'}
        fig, ax = plt.subplots(ncols=3, 
                               nrows=len(self.image_list), 
                               figsize=self.fig_size[len(self.image_list) - 1],
                              )

        
        for i, image in enumerate(self.image_list):
            for k in range(3):
                if len(self.image_list) > 1:
                    ax_current = ax[i][k]
                else:
                    ax_current = ax[k]
                ax_current.volume = image
                ax_current.index = image.shape[k]//2
                # ax_current.index = 0
                image_slice = image.take(indices=ax_current.index, axis=k)
                ax_current.imshow(image_slice,  aspect='auto')
                ax_current.set_xticks([])
                ax_current.set_yticks([])
                ax_current.set_title("img{}: {}".format(i + 1, image_mapper[k]))
                
                
            fig.canvas.mpl_connect('key_press_event', self.process_key) 
        
    def process_key(self, event):

        keys_allowed = self.keys[:len(self.image_list)*3-1]
        # if event.key not in keys_allowed:
        #     print("Invalid Key")
        
        fig = event.canvas.figure
        key_index = self.keys.index(event.key)
        
        ax = fig.axes[key_index]
        i = self.keys_mapping[event.key]
        self.next_slice(ax, i)
        fig.canvas.draw()



    def next_slice(self, ax, i):

        image = ax.volume
        ax.index = (ax.index + 1) % image.shape[i]
        print(ax.index)
        
        image_slice = image.take(indices=ax.index, axis=i) 
        ax.images[0].set_array(image_slice)




