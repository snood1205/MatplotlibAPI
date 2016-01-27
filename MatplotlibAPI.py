# -*- coding: utf-8 -*-
# Disclaimer: All code contained belongs to Nathaniel Starkman. Do not distribute.

import numpy as np
import matplotlib.pyplot as plt


"""
line = gca().get_lines()[n]
xd = line.get_xdata()
yd = line.get_ydata()
"""


class Object(object):
    """This is the main class for all objects which are to be plotted
    Plot Items:
    name, args, xaxis

    Errors:
    xerr, yerr, ecolor
        - xerr  : x error [list]
        - yerr  : y error [list]
        - ecolor: [ None | mpl color ]
        - elinewidth: [ None | scalar ]
        - barsabove: [ True | False ]
        - errorevery: [positive int]
        # - capsize: [ None | scalar ]  # can't get built-in default

    Marker Properties:
    fmt, marker, mfc, mec, mew, ms
        - fmt   : plot format string [ '', None, 'ro', 'g-', etc]
        - marker: the shape ['.':dot, 's':square ]
        - mfc   : markerfacecolor ['red', 'green', etc]
        - mec   : markeredgecolor ['red', 'green', etc]
        - mew   : markeredgewith  ['red', 'green', etc]
        - ms    : markersize [any float. defaults to 3]
        - alpha : opacity [float (0.0 trans to 1.0 opaque)]
        - ls    : line style ['-' | '--' | '-.' | ':' | 'None' | ' ' | '']
        - lw    : line width [float value in points]
        # - color : ['color']  # can't get built-in default
    """

    def __init__(self, name, *args, **kw):
        super(Object, self).__init__()
        self.name = name
        self.args = args

        self.xaxis = kw.get('xaxis')  # defaults to None if not given

        self.marker = self.Marker(kw)
        self.err = self.Errors(kw)

    class Marker(object):
        """docstring for Marker"""
        def __init__(self, kw):
            self.mfc = kw.get("mfc")
            self.mec = kw.get("mec")
            self.mew = kw.get("mew")
            try:  # marker
                kw["marker"]
            except:
                self.marker = '.'
            else:
                self.marker = kw.get("marker")
            try:   # markersize
                kw["ms"]
            except:
                self.ms = 4.
            else:
                self.ms = kw.get("ms")
            try:
                kw['fmt']
            except:
                self.fmt = ''
            else:
                self.fmt = kw.get("fmt")
            try:
                kw["alpha"]
            except:
                self.alpha = 1.0
            else:
                self.alpha = kw.get("alpha")
            # try:
            #     kw["color"]
            # except:
            #     self.color = 'b'
            # else:
            #     self.alpha = kw.get("color")
            try:
                kw["ls"]
            except:
                self.ls = 'None'
            else:
                self.ls = kw.get("ls")
            try:
                kw["lw"]
            except:
                self.lw = 1.
            else:
                self.lw = kw.get("lw")

    class Errors(object):
        """docstring for Errors"""
        def __init__(self, kw):
            self.yerr = kw.get('yerr')  # defaults to None if not given
            self.xerr = kw.get('xerr')
            self.ecolor = kw.get("ecolor")
            self.elinewidth = kw.get("elinewidth")
            try:
                kw["barsabove"]
            except:
                self.barsabove = False
            else:
                self.barsabove = kw.get("barsabove")
            try:
                kw["errorevery"]
            except:
                self.errorevery = 1
            else:
                self.errorevery = kw.get("errorevery")

    def _plot(self, fig=None, ax=None, xaxis=None, **kw):
        # what to do
        if fig is None:                     # no figure given
            fig, ax = plt.subplots(1, 1)
        elif isinstance(ax, (int, float)):  # figure given
            ax = fig.add_subplot(ax)
        else:                               # figure and axis give
            pass

        if 'name' in kw:  # object label
            name = kw.get('name')
        else:
            name = self.name
        if xaxis is None:  # other xaxis
            try:
                self.xaxis[0]
            except:
                pass  # *** figure out how to gett current xaxis
            else:
                xaxis = self.xaxis

        for arg in self.args:
            ax.errorbar(xaxis, arg,
                        label=name,
                        yerr=self.err.yerr,
                        xerr=self.err.xerr,
                        ecolor=self.err.ecolor,
                        elinewidth=self.err.elinewidth,
                        barsabove=self.err.barsabove,
                        errorevery=self.err.errorevery,
                        # capsize=self.err.capsize

                        fmt=self.marker.fmt,
                        marker=self.marker.marker,
                        mfc=self.marker.mfc,
                        mec=self.marker.mec,
                        ms=self.marker.ms,
                        alpha=self.marker.alpha,
                        ls=self.marker.ls,
                        lw=self.marker.lw
                        # color=self.marker.color,
                        )
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, loc='best')
        return fig, ax


class Plot(object):
    """docstring for Plot"""
    def __init__(self, xaxis=None, *args, **kw):
        super(Plot, self).__init__()
        self.args = args
        self.xaxis = xaxis
        self.xlabel = self.XLabel(kw)
        self.ylabel = self.YLabel(kw)
        self.title = self.Title(kw)

    class XLabel(object):
        """docstring for xlabel"""
        def __init__(self, kw):
            if "xlabel" in kw:
                self.xlabel = kw.get("xlabel")

    class YLabel(object):
        """docstring for YLabel"""
        def __init__(self, kw):
            if "ylabel" in kw:
                self.ylabel = kw.get("ylabel")

    class Title(object):
        """docstring for Title"""
        def __init__(self, kw):
            self.title = kw.get("title")

    @staticmethod
    def makePlot(xaxis=None, *args, **kw):  # make more sophisticated
        fig, ax = plt.subplots(1, 1)
        title = ''
        for i, val in enumerate(args):
            val._plot(fig, ax, xaxis)
            title += '{}, '.format(val.name)

        if "axhline" in kw:
            axhline = kw.get("axhline")
            for line in axhline:
                try:
                    ax.axhline(line[0], color=line[1])
                except IndexError:
                    ax.axhline(line)

        if "xlabel" in kw:
            ax.set_xlabel(kw.get("xlabel"))
        if "ylabel" in kw:
            ax.set_ylabel(kw.get("ylabel"))
        if 'title' in kw:
            title = kw.get('title')
        ax.set_title(title)

        if "minorticks" in kw:
            minorticks = kw.get("minorticks")
            if minorticks is True:
                ax.minorticks_on()
            else:
                pass
        if "invert_yaxis" in kw:
            invert_yaxis = kw.get("invert_yaxis")
            if invert_yaxis is True:
                ax.invert_yaxis()
            else:
                pass
        if "invert_xaxis" in kw:
            invert_xaxis = kw.get("invert_xaxis")
            if invert_xaxis is True:
                ax.invert_xaxis()
            else:
                pass
        if "xlim" in kw:
            xlims = kw.get("xlim")
            ax.set_xlim(xlims[0], xlims[1])
        if "ylim" in kw:
            ylims = kw.get("ylim")
            ax.set_ylim(ylims[0], ylims[1])

        ax.legend(loc="best")
        if "save" in kw:
            plt.savefig(kw.get("save"))

        return fig, ax



#####################################################################
#                     some astronomy functions

def absMag(appMag, parallax):  # *** is it parallax/2?
    d = 1./parallax
    absMag = -5.*np.log10(d) + 5 + appMag
    return absMag


def d_absMag(parallax, d_parallax):
    d = 1./parallax
    d_absMag = 5.*d*d_parallax/np.log(10)
    return d_absMag
