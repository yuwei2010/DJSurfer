
import pandas as pd
import numpy as np
from djsurfer.datainterface import DataInterface
import os
import re
import matplotlib.pyplot as plt

#%%
class TextObject_SY(DataInterface):
    """
    A class representing a text object to access zylinder measured data in a text file.

    Args:
        path (str): The path to the text file.
        name (str, optional): The name of the text object. Defaults to None.
        comment (str, optional): Any additional comment about the text object. Defaults to None.
        config (dict, optional): Configuration parameters for the data interface. Defaults to None. 
    """

    def __init__(self, path, name=None, comment=None, delimiter=' '):
        
        # Initialize the text interface object, passing the path, name, and comment to the base class.
        super().__init__(path=path, name=name, comment=comment)
        
        # Default delimiter is a white space.
        self.delimiter = delimiter
        
        # Attributes of zylinder measurement
        if self.name is None:
            file_name_with_extension = os.path.basename(path)
            self.name = file_name_with_extension.split('.')[0]
        
        # Zylinder measure type
        pattern = r'(FR|DR)'
        match = re.search(pattern, self.name)
        if match:
            self.meas_type = match.group(0)
        
        # Zylinder radius
        pattern = r'(\d+)H\d+'
        match = re.search(pattern, self.name)
        if match:
            self.radius_ref = float(match.group(1))/2

        # Total measured angle
        self.total_angle = 380
        
        # Pre-defined measured position set
        self.meas_FR_pos_sets = {
            'pos1': [65, 66, 67, 68, 69, 70],
            'pos2n': [54.5, 55.5, 56.5, 57.5],
            'pos2p': [45.5, 46.5, 47.5, 48.5, 49.5],
            'pos3': [33, 34, 35, 36, 37, 38],
            'pos4': [26, 27, 28, 29, 30]            
        }
        self.meas_DR_pos_sets = {
            'pos5': [74, 75, 76, 77, 78],
            'pos6n': [64.5, 65, 65.5, 66],
            'pos6p': [55, 56, 57, 58, 59],
            'pos7': [45.3, 46, 47, 48, 49],
            'pos8': [36, 37, 38, 38.5]            
        }
        

    def get_df(self):
        """
        Read the text file and return its contents as a pandas DataFrame.

        Returns:
            pandas.DataFrame: The contents of the text file as a DataFrame.
        """
        with open(self.path, 'r') as f:
            lines = f.readlines()
       
        df = pd.DataFrame([l.strip().split(self.delimiter) for l in lines], columns=['X','Y','Z'])

        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['meas_type'] = self.meas_type
        df['Z'] = abs(round(df['Z'], 1))

        # calculate measured angle in degree
        mp_num = df.groupby('Z').size()
        df['mp_unit_angle'] = df['Z'].map(self.total_angle/mp_num)
        df['angle_idx'] = df.groupby('Z').cumcount()
        df['angle'] = df['angle_idx'] * df['mp_unit_angle']

        df.loc[df['angle_idx'] == 0, 'angle'] = 0
        for grid_angle in [90, 180, 270, 360]:
            nearst_mp = df.loc[(df.groupby('Z')['angle'].apply(lambda x: abs(x - grid_angle).idxmin())), 'angle_idx']
            df.loc[df.index.isin(nearst_mp.index), 'angle'] = grid_angle

        # fetch measured data from 0 to 360 degrees
        begin_index = df.loc[df['angle'] == 0].index.to_list()
        end_index = df.loc[df['angle'] == 360].index.to_list()
        subset_dfs = [df.loc[start:end] for start, end in zip(begin_index, end_index)]
        df_cut = pd.concat(subset_dfs, axis=0)
        
        # calculate measured radius and deviation from the reference
        df_cut['radius'] = (df_cut['X'] ** 2 + df_cut['Y'] ** 2) ** 0.5
        df_cut['dev'] = df_cut['radius'] - self.radius_ref

        df_z = df_cut.set_index('Z', inplace=False)
        
        return df_z
    
    def plot_data(self, path, pos_req = None, z_req = None, color = 'blue'):
        """
        plot data/data set to a png file.

        Args:
            path (str): The path to save the png file.
            pos_req(str): The pre-defined position set to be plotted. Defaults to None.
                          FR = [pos1, pos2n, pos2p, pos3, pos4]
                          DR = [pos5, pos6n, pos6p, pos7, pos8]
            z_req(list): The Z position list to be plotted. Defaults to None.
        """
        # validate given z-position set to be plotted
        z_set = []
        if pos_req is None and z_req is None:
            print("No Z set or position set is given. Please try again.")
        elif pos_req is not None and z_req is not None:
                print("Only one Z set, or one position set is accepted. Please try again.")
        elif pos_req is not None:
            plot_set_name = pos_req
            if (pos_req in self.meas_FR_pos_sets.keys() and self.meas_type == 'FR'):
                z_set = self.meas_FR_pos_sets[pos_req]
            elif (pos_req in self.meas_DR_pos_sets.keys() and self.meas_type == 'DR'):
                z_set = self.meas_DR_pos_sets[pos_req]
            else:
                print("The given position set belongs not to the measure data. Please try again.")
        else:
            z_full_set = set(self.dataframe.index)
            if all(elem in z_full_set for elem in z_req):
                z_set = z_req
                plot_set_name = '_'.join(str(x) for x in z_set)
            else:
                print("The given Z set belongs not to the measure data. Please try again.")
        
        if len(z_set) != 0:
            # fetch dataframe to be plotted
            df_plot = self.dataframe.loc[z_set]

            # set output png file path
            outp_name = self.name + '_' + plot_set_name
            outp_filetype = '.png'
            outp_full_path = path + outp_name + outp_filetype

            # set plot label, color, alpha, axis min/max  
            z_labels = [f'Z={z}' for z in z_set]
            n = len(z_set)
            alphas = np.linspace(0.1, 1, n)
            color = 'blue'

            ax_min = round(df_plot['radius'].min(), 2) - 0.01
            ax_max = round(df_plot['radius'].max(), 2) + 0.01

            data_min = round(df_plot['radius'].min(), 3)
            data_max = round(df_plot['radius'].max(), 3)

            fig = plt.figure(figsize=(16, 8), dpi=100)# 创建一个新的图形窗口，设置其大小为23x10英寸，分辨率为100dpi
            # 在当前的图形窗口上创建一个极坐标子图，并返回子图的引用，位置为2行1列的第1个位置, 开启极坐标
            ax1 = plt.subplot(211,projection='polar')
            # 在当前的图形窗口上创建一个极坐标子图，并返回子图的引用，位置为2行1列的第2个位置
            ax2 = plt.subplot(212)

            ax1.set_rlim(ax_min, ax_max)
            ax1.set_thetagrids(np.arange(0.0, 360.0, 90.0))
            ax1.set_rlabel_position(90)

            ax2.set_xlim(0, 360)
            ax2.set_ylim(ax_min, ax_max)
            ax2.set_xticks([0, 90, 180, 270, 360])
            ax2.set_xticklabels(['0°', '90°', '180°', '270°', '360°'])
            ax2.tick_params(axis='y', which='both', length=6, labelsize=8)

            for z_value, alpha in zip(z_set, alphas):
                group = df_plot[df_plot.index == z_value]
                # 为每组数据设置深浅不同的蓝色
                for idx, row in group.iterrows():
                    radius = row['radius']
                    angle = row['angle']
                    theta = np.deg2rad(row['angle'])
        
                    ax1.scatter(theta, radius, color=color, alpha=alpha, edgecolors='white', linewidths=0)
                    ax2.scatter(angle, radius, color=color, alpha=alpha, edgecolors='white', linewidths=0)

            # 设置图形的标题
            fig.suptitle(f'Zylinder r = {self.radius_ref} mm, {self.meas_type}, Z = {plot_set_name}')

            # 在右上角显示注释
            plt.figtext(0.9, 0.95, f'r_max = {data_max}\nr_min = {data_min}', ha='right', va='top', bbox=None)

            # 显示图例
            data_legend = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, alpha=alpha, markersize=5, label=label) for alpha, label in zip(alphas,z_labels)]
            plt.legend(handles=data_legend, loc='upper center', bbox_to_anchor=(0.85, 0.9), fontsize=8, bbox_transform=plt.gcf().transFigure)

            plt.savefig(outp_full_path)
            plt.show()

if __name__ == '__main__':
    
    from pathlib import Path
    obj = TextObject_SY(Path(__file__).parent / r'..\..\tests\demo_data\Zyl_7H6_vo_FR_X.txt')

