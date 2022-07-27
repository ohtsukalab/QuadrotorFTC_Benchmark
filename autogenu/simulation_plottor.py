import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

from autogenu import simulation_conditions as simcon


class SimulationPlottor(object):
    """ Plots the simulation results.

        Attributes: 
            set_scales(figure_scale, font_scale, space_scale): Sets scales 
                about the graphs to adjust its size. 
            show_plots(): Shows the graph of the simulation results.
            save_plots(): Saves the graph of the simulation results as a .pdf
                file.
    """

    def __init__(self, ocp_name):
        """ Inits SimulationPlotter with loading the simulation results. """
        # Load the data of the simulation results. 
        self.__save_dir = 'generated/' + ocp_name + '/simulation_result/'
        self.__file_header = self.__save_dir + ocp_name
        self.__x_data = np.genfromtxt(
            self.__file_header+'_x'+'.log'
        )
        self.__u_data = np.genfromtxt(
            self.__file_header+'_u'+'.log'
        )
        self.__opterr_data = np.genfromtxt(
            self.__file_header+'_opterr'+'.log'
        )
        self.__sim_conditions = simcon.SimulationConditions(
            self.__file_header
        )
        self.__time_sequence = np.linspace(
            0, 
            self.__sim_conditions.simulation_time(), 
            self.__x_data.shape[0]
        )
        # Replace NaN with 0.
        self.__x_data[np.isnan(self.__x_data)] = 0
        self.__u_data[np.isnan(self.__u_data)] = 0
        self.__opterr_data[np.isnan(self.__opterr_data)] = 0
        # Set dimensions of the state and the control input.
        if self.__x_data.shape[0] == self.__x_data.size:
            self.__dim_x= 1
        else:
            self.__dim_x = self.__x_data.shape[1]
        if self.__u_data.shape[0] == self.__u_data.size:
            self.__dim_u = 1
        else:
            self.__dim_u = self.__u_data.shape[1]
        # Set the layout of the graphs.
        self.__num_plots = self.__dim_x + self.__dim_u + 1
        self.__num_plot_x = int(np.floor(
            self.__num_plots/np.sqrt(self.__num_plots)
        ))
        self.__num_plot_y = int(np.ceil(
            self.__num_plots/self.__num_plot_x
        ))
        # Set default figure scales. 
        self.__figure_scale = 1
        self.__font_scale = 1
        self.__space_scale = 1
        # Set format of the graphs.
        sns.set_style("ticks")
        sns.set_palette("deep") 
        sns.set_context("paper")
        plt.rc('mathtext', 
            **{'rm':'serif', 
            'it':'serif:itelic', 
            'bf':'serif:bold', 
            'fontset':'cm'}
        )
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['pdf.fonttype'] = 42
        plt.rcParams['ps.fonttype'] = 42
        # Set the width of lines and axes.
        plt.rcParams['lines.linewidth'] = 1
        plt.rcParams['axes.linewidth'] = 0.5

    def set_scales(self, figure_scale, font_scale, space_scale):
        """ Set parameters for the scales of the graph.

            Args:
                figure_scale: The scale of the entire graph.
                font_scale: The scale of the font in the graph. 
                space_scale: The scale of the spaces in the graph. 
        """
        self.__figure_scale = figure_scale
        self.__font_scale = font_scale
        self.__space_scale = space_scale

    def show_plots(self):
        """ Show the graphs of the simulation results. """
        self.__plot_graphs()
        plt.show()

    def save_plots(self):
        """ Save the graphs of the simulation results. """
        self.__plot_graphs()
        plt.savefig(
            self.__file_header+'.pdf', 
            bbox_inches="tight", 
            pad_inches=0.1
        )
        print(
            'The graph of the simlation results is generated at '
            +self.__file_header
            +'.pdf\n'
        )

    def __plot_graphs(self):
        """ Plots the simulation results in figure object. """
        # Sets the figure size.
        plt.figure(figsize=(
            2.5*self.__num_plot_x*self.__figure_scale, 
            self.__num_plot_y*self.__figure_scale
        )) 
        # Sets the font size.
        plt.rcParams['font.size'] = self.__font_scale*10/self.__num_plots 
        # Sets the space between the graphs.
        plt.subplots_adjust(
            wspace=self.__space_scale/self.__num_plots, 
            hspace=2*self.__space_scale/self.__num_plots
        ) 
        if self.__dim_x > 1:
            for i in range(self.__dim_x):
                plt.subplot(self.__num_plot_y, self.__num_plot_x, i+1)
                plt.plot(self.__time_sequence, self.__x_data[:, i])
                plt.xlabel(r'${\rm Time}$ $[s]$')
                plt.ylabel(r'$x_{}$'.format(i+1))
                plt.xlim(0, self.__sim_conditions.simulation_time())
        else:
            plt.subplot(
                self.__num_plot_y, 
                self.__num_plot_x, 
                1
            )
            plt.plot(self.__time_sequence, self.__x_data)
            plt.xlabel(r'${\rm Time}$ $[s]$')
            plt.ylabel(r'$x$')
            plt.xlim(0, self.__sim_conditions.simulation_time())
        if self.__dim_u > 1:
            for i in range(self.__dim_u):
                plt.subplot(
                    self.__num_plot_y, 
                    self.__num_plot_x, 
                    i+self.__dim_x+1
                )
                plt.plot(self.__time_sequence, self.__u_data[:, i])
                plt.xlabel(r'${\rm Time}$ $[s]$')
                plt.ylabel(r'$u_{}$'.format(i+1))
                plt.xlim(0, self.__sim_conditions.simulation_time())
        else:
            plt.subplot(
                self.__num_plot_y, 
                self.__num_plot_x, 
                self.__dim_x+1
            )
            plt.plot(self.__time_sequence, self.__u_data)
            plt.xlabel(r'${\rm Time}$ $[s]$')
            plt.ylabel(r'$u$')
            plt.xlim(0, self.__sim_conditions.simulation_time())
        plt.subplot(
            self.__num_plot_y, 
            self.__num_plot_x, 
            self.__dim_x+self.__dim_u+1
        )
        plt.plot(self.__time_sequence, np.log10(self.__opterr_data))
        plt.xlabel(r'${\rm Time}$ $[s]$')
        plt.ylabel(r'$\log_{10} \| {\rm Opt \; Error} \|$')
        plt.xlim(0, self.__sim_conditions.simulation_time())