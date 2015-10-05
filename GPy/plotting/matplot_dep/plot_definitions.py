#===============================================================================
# Copyright (c) 2015, Max Zwiessele
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# 
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# * Neither the name of GPy.plotting.matplot_dep.plot_definitions nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#===============================================================================
import numpy as np
from matplotlib import pyplot as plt
from ..abstract_plotting_library import AbstractPlottingLibrary
from .. import Tango
from . import defaults
from matplotlib.colors import LinearSegmentedColormap
from .controllers.imshow_controller import ImshowController

class MatplotlibPlots(AbstractPlottingLibrary):
    def __init__(self):
        super(MatplotlibPlots, self).__init__()
        self._defaults = defaults.__dict__
    
    def get_new_canvas(self, xlabel=None, ylabel=None, zlabel=None, title=None, projection='2d', **kwargs):
        if projection == '3d':
            from mpl_toolkits.mplot3d import Axes3D
        elif projection == '2d':
            projection = None
        if 'ax' in kwargs:
            ax = kwargs.pop('ax')
        elif 'num' in kwargs and 'figsize' in kwargs:
            ax = plt.figure(num=kwargs.pop('num'), figsize=kwargs.pop('figsize')).add_subplot(111, projection=projection) 
        elif 'num' in kwargs:
            ax = plt.figure(num=kwargs.pop('num')).add_subplot(111, projection=projection)
        elif 'figsize' in kwargs:
            ax = plt.figure(figsize=kwargs.pop('figsize')).add_subplot(111, projection=projection)
        else:
            ax = plt.figure().add_subplot(111, projection=projection)
            
        if xlabel is not None: ax.set_xlabel(xlabel)
        if ylabel is not None: ax.set_ylabel(ylabel)
        if zlabel is not None: ax.set_zlabel(zlabel)
        if title is not None: ax.set_title(title)
        return ax, kwargs
    
    def show_canvas(self, ax, plots, xlim=None, ylim=None, zlim=None, legend=True, **kwargs):
        try:
            ax.autoscale_view()
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
            if legend:
                ax.legend()
            if zlim is not None:
                ax.set_zlim(zlim)
            ax.figure.canvas.draw()
        except:
            pass
        return plots
    
    def scatter(self, ax, X, Y, Z=None, color=Tango.colorsHex['mediumBlue'], label=None, marker='o', **kwargs):
        if Z is not None:
            return ax.scatter(X, Y, c=color, zs=Z, label=label, marker=marker, **kwargs)
        return ax.scatter(X, Y, c=color, label=label, **kwargs)
    
    def plot(self, ax, X, Y, color=None, label=None, **kwargs):
        return ax.plot(X, Y, color=color, label=label, **kwargs)

    def plot_axis_lines(self, ax, X, color=Tango.colorsHex['mediumBlue'], label=None, **kwargs):
        from matplotlib import transforms
        from matplotlib.path import Path
        if 'marker' not in kwargs:
            kwargs['marker'] = Path([[-.2,0.],    [-.2,.5],    [0.,1.],    [.2,.5],     [.2,0.],     [-.2,0.]],
                                    [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
        if 'transform' not in kwargs:
            if X.shape[1] == 1:
                kwargs['transform'] = transforms.blended_transform_factory(ax.transData, ax.transAxes)
        if X.shape[1] == 2:
            return ax.scatter(X[:,0], X[:,1], ax.get_zlim()[0], c=color, label=label, **kwargs)
        return ax.scatter(X, np.zeros_like(X), c=color, label=label, **kwargs)

    def barplot(self, ax, x, height, width=0.8, bottom=0, color=Tango.colorsHex['mediumBlue'], label=None, **kwargs):
        if 'align' not in kwargs:
            kwargs['align'] = 'center'
        return ax.bar(left=x, height=height, width=width,
               bottom=bottom, label=label, color=color,  
               **kwargs)
        
    def xerrorbar(self, ax, X, Y, error, Z=None, color=Tango.colorsHex['mediumBlue'], label=None, **kwargs):
        if not('linestyle' in kwargs or 'ls' in kwargs):
            kwargs['ls'] = 'none'
        if Z is not None:
            return ax.errorbar(X, Y, Z, xerr=error, ecolor=color, label=label, **kwargs)
        return ax.errorbar(X, Y, xerr=error, ecolor=color, label=label, **kwargs)
    
    def yerrorbar(self, ax, X, Y, error, Z=None, color=Tango.colorsHex['mediumBlue'], label=None, **kwargs):
        if not('linestyle' in kwargs or 'ls' in kwargs):
            kwargs['ls'] = 'none'
        if Z is not None:
            return ax.errorbar(X, Y, Z, yerr=error, ecolor=color, label=label, **kwargs)
        return ax.errorbar(X, Y, yerr=error, ecolor=color, label=label, **kwargs)
    
    def imshow(self, ax, X, extent=None, label=None, plot_function=None, resolution=None, vmin=None, vmax=None, **kwargs):
        if plot_function is not None:
            self.controller = ImshowController(ax, plot_function, extent, resolution=resolution, vmin=vmin, vmax=vmax, **kwargs)
            return self.controller
        return ax.imshow(X, label=label, extent=extent, vmin=vmin, vmax=vmax, **kwargs)
    
    def contour(self, ax, X, Y, C, levels=20, label=None, **kwargs):
        return ax.contour(X, Y, C, levels=np.linspace(C.min(), C.max(), levels), label=label, **kwargs)

    def surface(self, ax, X, Y, Z, color=None, label=None, **kwargs):
        return ax.plot_surface(X, Y, Z, label=label, **kwargs)

    def fill_between(self, ax, X, lower, upper, color=Tango.colorsHex['mediumBlue'], label=None, **kwargs):
        return ax.fill_between(X, lower, upper, facecolor=color, label=label, **kwargs)

    def fill_gradient(self, canvas, X, percentiles, color=Tango.colorsHex['mediumBlue'], label=None, **kwargs):
        ax = canvas
        plots = []
        
        if 'edgecolors' not in kwargs:
            kwargs['edgecolors'] = 'none'
        
        if 'facecolors' in kwargs:
            color = kwargs.pop('facecolors')
            
        if 'array' in kwargs:
            array = kwargs.pop('array')
        else:
            array = 1.-np.abs(np.linspace(-.97, .97, len(percentiles)-1))

        if 'alpha' in kwargs:
            alpha = kwargs.pop('alpha')
        else:
            alpha = .8

        if 'cmap' in kwargs:
            cmap = kwargs.pop('cmap')
        else:
            cmap = LinearSegmentedColormap.from_list('WhToColor', (color, color), N=array.size)
        cmap._init()
        cmap._lut[:-3, -1] = alpha*array

        kwargs['facecolors'] = [cmap(i) for i in np.linspace(0,1,cmap.N)]

        # pop where from kwargs
        where = kwargs.pop('where') if 'where' in kwargs else None
        # pop interpolate, which we actually do not do here!
        if 'interpolate' in kwargs: kwargs.pop('interpolate')

        from itertools import tee
        try:
            from itertools import izip as zip
        except ImportError:
            # python 3 already is izip
            pass
        
        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            a, b = tee(iterable)
            next(b, None)
            return zip(a, b)            
            
        polycol = []
        for y1, y2 in pairwise(percentiles):
            import matplotlib.mlab as mlab
            # Handle united data, such as dates
            ax._process_unit_info(xdata=X, ydata=y1)
            ax._process_unit_info(ydata=y2)
            # Convert the arrays so we can work with them
            from numpy import ma
            x = ma.masked_invalid(ax.convert_xunits(X))
            y1 = ma.masked_invalid(ax.convert_yunits(y1))
            y2 = ma.masked_invalid(ax.convert_yunits(y2))
        
            if y1.ndim == 0:
                y1 = np.ones_like(x) * y1
            if y2.ndim == 0:
                y2 = np.ones_like(x) * y2
        
            if where is None:
                where = np.ones(len(x), np.bool)
            else:
                where = np.asarray(where, np.bool)
        
            if not (x.shape == y1.shape == y2.shape == where.shape):
                raise ValueError("Argument dimensions are incompatible")
        
            mask = reduce(ma.mask_or, [ma.getmask(a) for a in (x, y1, y2)])
            if mask is not ma.nomask:
                where &= ~mask
            
            polys = []
            for ind0, ind1 in mlab.contiguous_regions(where):
                xslice = x[ind0:ind1]
                y1slice = y1[ind0:ind1]
                y2slice = y2[ind0:ind1]
        
                if not len(xslice):
                    continue
        
                N = len(xslice)
                p = np.zeros((2 * N + 2, 2), np.float)
        
                # the purpose of the next two lines is for when y2 is a
                # scalar like 0 and we want the fill to go all the way
                # down to 0 even if none of the y1 sample points do
                start = xslice[0], y2slice[0]
                end = xslice[-1], y2slice[-1]
        
                p[0] = start
                p[N + 1] = end
        
                p[1:N + 1, 0] = xslice
                p[1:N + 1, 1] = y1slice
                p[N + 2:, 0] = xslice[::-1]
                p[N + 2:, 1] = y2slice[::-1]
        
                polys.append(p)
            polycol.extend(polys)
        from matplotlib.collections import PolyCollection
        if 'zorder' not in kwargs:
            kwargs['zorder'] = 0
        plots.append(PolyCollection(polycol, **kwargs))
        ax.add_collection(plots[-1], autolim=True)
        ax.autoscale_view()
        return plots
