
import pandas as pd
import numpy as np
from djsurfer.datainterface import DataInterface

#%%
class MeasTextObject_SY(DataInterface):       
    """
    A class representing a text object to access cylinder measured data in a text file.

    Args:
        path (str): The path to the text file.
        name (str, optional): The name of the text object. Defaults to None.
        comment (str, optional): Any additional comment about the text object. Defaults to None.
        config (dict, optional): Configuration parameters for the data interface. Defaults to None. 
    """

    def __init__(self, path, name=None, comment=None, delimiter=' '):
        import os
        import re
        
        # Initialize the text interface object, passing the path, name, and comment to the base class.
        super().__init__(path=path, name=name, comment=comment)
        
        # Default delimiter is a white space.
        self.delimiter = delimiter
        
        # Attributes of cylinder measurement
        if self.name is None:
            file_name_with_extension = os.path.basename(path)
            self.name = file_name_with_extension.split('.')[0]
        
        self.dirname = os.path.basename(os.path.dirname(path))
        self.path = path
        
		# Cylinder parameters from file name: model type, measure type and norminal radius
        pattern_FDR = """
        (Kr_)                   # indicator of measure data
        (?P<diameter>\d+)       # cylinder diameter"
        (H\w+?)                 # indicator of tolerance
        (?P<meas_type>(FR|DR))  # cylinder measure type
        (.*)                    # indicator of Z value
        """
        
        pattern_EZ = """
        (Kr_)                   # indicator of measure data
        (?P<diameter>\d+)       # cylinder diameter"
        (H\w+?)                 # indicator of tolerance
        (?P<meas_type>[L|S]\d+$)  # cylinder measure type
        """
        
        match = re.search(pattern_FDR, self.name, re.VERBOSE)
        if match:
            self.model_type = 'FDR'
            self.meas_type = match.groupdict()['meas_type']
            self.radius_norm = float(match.groupdict()['diameter'])/2
        else: 
            match = re.search(pattern_EZ, self.name, re.VERBOSE)
            if match:
                self.model_type = 'EZ'
                self.meas_type = match.groupdict()['meas_type']
                self.radius_norm = float(match.groupdict()['diameter'])/2
            else:
                self.model_type = None
                self.meas_type = None
                self.radius_norm = None

        # Total measured angle
        self.total_angle = 380     
    
    def get_df(self):
        """
        Read the measure data in txt format and return its contents as a pandas DataFrame.

        Returns:
            pandas.DataFrame: The contents of the measure data as a DataFrame.
        """
        with open(self.path, 'r') as f:
            lines = f.readlines()
       
       # read first 3 columns as X, Y and Z input
        data = []
        for line in lines:
            line_data = line.strip().split(self.delimiter)
            x, y, z = line_data[:3]
            data.append({'X': x, 'Y': y, 'Z': z})
        df = pd.DataFrame(data)

        # clean up data, replace ',' with '.' if any
        for col in df.columns:
            if any(',' in value for value in df[col]):
                df[col] = df[col].str.replace(',', '.')
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # find the most frequent value in column 'Z' to prevent multiple Z value due to rounding tolerance
        df['Z'] = abs(round(df['Z'], 1))
        Z_shall_value = df['Z'].mode()[0]

        # calculate measured angle in degree
        df.index.name = 'angle_idx'
        df['angle'] = df.index.values * self.total_angle / df.shape[0]
        
        for grid_angle in [0, 90, 180, 270, 360]:
            nearst_mp = (df['angle'] - grid_angle).abs().idxmin()
            df.loc[nearst_mp, 'angle'] = grid_angle

        # calculate measured radius, theta
        df['theta'] = np.deg2rad(df['angle'])
        df['radius'] = (df['X'] ** 2 + df['Y'] ** 2) ** 0.5
        
        # remove unnecessary columns and reindex columns with MultiIndex 5 level:
        # directory, model type, measure type, Z value and data (includes angle, theta, radius)
        df.drop(columns=['X', 'Y', 'Z'], inplace=True)
        df.columns = pd.MultiIndex.from_product([[self.dirname], [self.model_type], [self.meas_type], [Z_shall_value], df.columns], 
                                                    names=['data_dir', 'model_type', 'meas_type', 'Z', 'data'])
        
        return df

class MeasObject_SY(DataInterface):
    """
    A class representing a object of serie of cylinder measure data as pandas DataFrame.

    Args:
        path (str): The path to the text file.
        name (str, optional): The name of the text object. Defaults to None.
        comment (str, optional): Any additional comment about the text object. Defaults to None.
        config (dict, optional): Configuration parameters for the data interface. Defaults to None. 
    """
    def __init__(self, path, name=None, comment=None, config={}):
        from djsurfer.datapool import DataPool as dp        

        # Initialize the measure data interface object, passing the path, name, comment and config to the base class.
        super().__init__(path=path, name=name, comment=comment, config=config)
        pattern = config.pop('pattern', r'Kr.*')
        file_extension = config.pop('file_extension', '.txt')
        self.meas_type = config.pop('meas_type', None)
        self.pos_set = config.pop('pos_set', None)
        
        # Pre-defined measured position set, to be moved to class MeasObject
        self.meas_FR_pos_sets = {
            'pos1': (65, 66, 67, 68, 69, 70),
            'pos2n': (54.5, 55.5, 56.5, 57.5),
            'pos2p': (45.5, 46.5, 47.5, 48.5, 49.5),
            'pos3': (33, 34, 35, 36, 37, 38),
            'pos4': (26, 27, 28, 29, 30)            
        }
        self.meas_DR_pos_sets = {
            'pos5': (74, 75, 76, 77, 78),
            'pos6n': (64.5, 65, 65.5, 66),
            'pos6p': (55, 56, 57, 58, 59),
            'pos7': (45.3, 46, 47, 48, 49),
            'pos8': (36, 37, 38, 38.5)            
        }
        self.meas_EZ_pos_sets = {
            'pos1': (25, 26, 27, 28, 29),
            'pos2n': (35.2, 35.5, 35.8),
            'pos2p': (38, 39, 40),
            'pos3': (44, 45, 46),
            'pos4': (51.2, 51.9, 52.6)            
        }
        self.meas_types_EZ = ('L6', 'L7', 'L8', 'L9', 'L10', 'S1', 'S2', 'S3', 'S4', 'S5')
        self.meas_types_FDR = ('FR', 'DR')
        
        self.meas_datapool = dp(path, interface=MeasTextObject_SY, pattern=pattern, ftype=file_extension)
        self.df_list = []

    def get_df(self):
        """
        Read serie of dataframe of measure files and return a merged pandas DataFrame.

        Returns:
            pandas.DataFrame: The merged measure files as a DataFrame.
        """
        for obj in self.meas_datapool.objs:
            df = obj.dataframe
            self.df_list.append(df)

        df_merged = pd.concat(self.df_list, axis=1)


        return df_merged

    def plot_data(self, inp_path = None, outp_path = None, type_req = None, pos_req = None, z_req = None, color = 'blue'):
        """
        plot data/data set to png file.

        Args:
            inp_path (str): The path of measure data to be plotted. If not given the root path of measure data is used. 
            outp_path (str): The path to save the png file. If not given the root path of measure data is used. 
            type_req (str): The measure type to be plotted. Default is None.
                            [FR, DR] for model type FDR
                            [L6, L7, L8, L9, L10, S1, S2, S3, S4, S5] for model type EZ
            pos_req(str): The pre-defined position set to be plotted. Default is None.
                          FR = [pos1, pos2n, pos2p, pos3, pos4]
                          DR = [pos5, pos6n, pos6p, pos7, pos8]
                          EZ = [pos1, pos2n, pos2p, pos3, pos4]
            z_req(tuple): The customized Z position tuple to be plotted. Default is None.
			color(str): The plot color. Default is blue.
        """        
        import os        

        z_set = set()
        
        # validate input path, if not given set it to measure data root path 
        if inp_path is None:
            inp_path = self.path
        else:
            abs_inp_path = os.path.abspath(inp_path)
            abs_data_path = os.path.abspath(self.path)
            if abs_inp_path != abs_data_path and not abs_inp_path.startswith(abs_data_path + os.sep):
                print("Given path is not matching measure data input path, or subpath of it. Plot aborted.")
                return
        
        # create _out folder under measure data root path if output path is not given
        if outp_path is None:
            outp_path = os.path.join(self.path, '_out')
            if not os.path.exists(outp_path):
                os.mkdir(outp_path)
                print(f"No output folder specified. Default folder {outp_path} is created/used.")
        
        # validate measure type and set corresponding cylinder model type
        if (type_req is None) and (self.meas_type is None):
            print("No measure type is given. Plot aborted.")
            return
        elif (type_req is None) and (self.meas_type is not None):
            type_req = self.meas_type
        
        if type_req in self.meas_types_EZ:
            model_req = 'EZ'
        elif type_req in self.meas_types_FDR:
            model_req = 'FDR'
        else:
            print("Wrong measure type is given. Plot aborted.")
            return
        
        # validate predefined/customized Z position set
        if pos_req is None and z_req is None and self.pos_set is None:
            print("No Z position is given. Plot aborted.")
            return
        elif pos_req is not None and z_req is not None:
            print("Only predefined position set or customized Z positions to be given. Plot aborted.")
            return
        if pos_req is not None:
            if (pos_req in self.meas_FR_pos_sets.keys() and type_req == 'FR'):
                z_set = self.meas_FR_pos_sets[pos_req]
            elif (pos_req in self.meas_DR_pos_sets.keys() and type_req == 'DR'):
                z_set = self.meas_DR_pos_sets[pos_req]
            elif (pos_req in self.meas_EZ_pos_sets.keys() and type_req in self.meas_types_EZ):
                z_set = self.meas_EZ_pos_sets[pos_req]
            else:
                print(f"Wrong pre-defined position set is given. Plot aborted.")
                return
        
        # validate customized Z position set
        elif z_req is not None:
            z_full_set = set(self.dataframe.columns.levels[3])
            if isinstance(z_req, int):
                z_req = [z_req]
            if all(elem in z_full_set for elem in z_req):
                z_set = set(z_req) # shall use deepcopy()
            else:
                print(f"The given Z set belongs not to the measure data. Plot aborted.")
                return

        # iterate all combinations of given arguments and plot data set if available
        from itertools import product

        def get_dirname(base_path):
            dirnames = []
            for root, dirs, files in os.walk(base_path):
                if not dirs:
                    dirnames.append(os.path.basename(root))
            return dirnames
        
        def arg_combinations(dirnames, meas_model, meas_type):
            combinations = []
            for dirname in dirnames:
                for combination in product([meas_model], [meas_type]):
                    combinations.append((dirname,) + combination)
            return combinations
        
        plot_data_dirnames = get_dirname(inp_path)
        plot_data_columns_combinations = arg_combinations(plot_data_dirnames, model_req, type_req)
        
        for elem in plot_data_columns_combinations:
            try:
                idx = pd.IndexSlice
                df_plot = self.dataframe.loc[:, idx[elem[0], elem[1], elem[2], list(z_set), :]]
                self.plot_data_set(outp_path, df_plot, color)
            except KeyError:
                    pass

    def plot_data_set(self, outp_path, df_plot, color = 'blue'):
        """
        plot single data set to a png file.

        Args:
            outp_path (str): The path to save the png file.

            df_plot: The dataframe of measure data to be plotted.
            color(str): The plot color
        """	
        import matplotlib.pyplot as plt
        import os

        # fetch measure data details to create output file name
        dirname = '_'.join(df_plot.columns.get_level_values(0).unique())
        meas_type = '_'.join(df_plot.columns.get_level_values(2).unique())
        data_set = df_plot.columns.get_level_values(3).unique().tolist()
        plot_set_name = '_'.join(str(z) for z in data_set)

        # set output png file path
        outp_name = dirname + '_' + meas_type + '_' + plot_set_name
        outp_filetype = '.png'
        outp_full_path = os.path.join(outp_path, outp_name + outp_filetype)

        # set plot label, alpha, axis min/max  
        z_labels = [f'Z={z}' for z in data_set]
        n = len(data_set)
        alphas = np.linspace(0.1, 1, n)

        radius_data = df_plot.xs('radius', level='data', axis=1)
        radius_ref = round(radius_data.mean().mean(), 1)
        ax_min = round(radius_data.min().min(), 2) - 0.01
        ax_max = round(radius_data.max().max(), 2) + 0.01

        data_min = round(radius_data.min().min(), 3)
        data_max = round(radius_data.max().max(), 3)

        # configure figure and axes
        fig = plt.figure(figsize=(16, 8), dpi=100)
        # plot first figure on position (1,1) of 2x1 in polor coordinates
        ax1 = plt.subplot(211,projection='polar')
        # plot second figure on position (2,1) of 2x1 in orthogonal coordinates 
        ax2 = plt.subplot(212)

        ax1.set_rlim(ax_min, ax_max)
        ax1.set_thetagrids(np.arange(0.0, 360.0, 90.0))
        ax1.set_rlabel_position(90)

        ax2.set_xlim(0, 360)
        ax2.set_ylim(ax_min, ax_max)
        ax2.set_xticks([0, 90, 180, 270, 360])
        ax2.set_xticklabels(['0°', '90°', '180°', '270°', '360°'])
        ax2.tick_params(axis='y', which='both', length=6, labelsize=8)

        # plot only measure points with angle within [0,360] degree
        theta_360_mask = df_plot.xs('angle', level='data', axis=1) <= 360
        df_cut = df_plot[theta_360_mask.any(axis=1)]

        for z, alpha in zip(data_set, alphas):
            for idx, row in df_cut.iterrows():
                radius = row.loc[(slice(None), slice(None), slice(None), z, 'radius')].values[0]
                theta = row.loc[(slice(None), slice(None), slice(None), z, 'theta')].values[0]
                angle = row.loc[(slice(None), slice(None), slice(None), z, 'angle')].values[0]
                ax1.scatter(theta, radius, color=color, alpha=alpha, edgecolors='white', linewidths=0)
                ax2.scatter(angle, radius, color=color, alpha=alpha, edgecolors='white', linewidths=0)

        # set figure subtile, comment, legend
        fig.suptitle(f'Cylinder r = {radius_ref} mm, {meas_type}, Z = {data_set}\n from {dirname}')
        plt.figtext(0.9, 0.95, f'r_max = {data_max}\nr_min = {data_min}', ha='right', va='top', bbox=None)
        data_legend = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, alpha=alpha, markersize=5, label=label) for alpha, label in zip(alphas,z_labels)]
        plt.legend(handles=data_legend, loc='upper center', bbox_to_anchor=(0.85, 0.9), fontsize=8, bbox_transform=plt.gcf().transFigure)

        plt.savefig(outp_full_path)
        plt.show()


if __name__ == '__main__':
    
    from pathlib import Path
    obj = MeasTextObject_SY(Path(__file__).parent / r'..\..\tests\demo_data\Zyl_7H6_vo_FR_X.txt')

