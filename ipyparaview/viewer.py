from ipywidgets import interact
import ipywidgets as widgets


from .widgets import VTKDisplay


class PVTimeDisplay(object):
    """An extension of the VTKDisplay to also yeild GUI controls for ParaView.

    This is a helper class for our demos. It takse a single dataset on the
    paraview pipeline, renders it, creates the view, then shows an interactive
    widget with controls for scalar mapping, etc.

    The mesh must have cell data - if not, many errors will arise.

    Note: this is SUPER hacked together... simply a proof of concept
    """
    def __init__(self, data, runAsync=True, compressFrames=False, ren_size=(400, 400), **kwargs):
        try:
            from paraview import simple as pvs
        except:
            raise ImportError("Trouble import paraview.simple")

        pvs.Show(data)
        self._view = pvs.GetActiveView()
        self._view.ViewSize = ren_size
        self.vtk_display = VTKDisplay(self._view,
                                      runAsync=runAsync,
                                      compressFrames=compressFrames,
                                      **kwargs,
                                      )

        data_display = pvs.GetDisplayProperties(data, view=self._view)
        data_display.SetScalarBarVisibility(self._view, True)
        timer = pvs.GetTimeKeeper()
        anno = pvs.AnnotateTime()
        pvs.Show(anno)

        def set_time(change):
            step = change["new"]
            if step < 0:
                step = 0
            if step >= len(timer.TimestepValues):
                step = len(timer.TimestepValues) - 1
            timer.Time = timer.TimestepValues[step]
            return

        play = widgets.Play(
            value=0,
            min=0,
            max=len(timer.TimestepValues),
            step=1,
            description="Time Step",
        )

        play.observe(set_time, "value")

        slider = widgets.IntSlider(min=0, max=len(timer.TimestepValues), continuous_update=True)
        widgets.jslink((play, 'value'), (slider, 'value'))

        cmin = widgets.FloatText(
            value=0.0,
            description='Min:',
            disabled=False
        )
        cmax = widgets.FloatText(
            value=1.0,
            description='Max:',
            disabled=False
        )

        def set_clim(*args):
            tf = pvs.GetColorTransferFunction(data_display.ColorArrayName[1])
            tf.RescaleTransferFunction(cmin.value, cmax.value)
            return

        cmin.observe(set_clim, "value")
        cmax.observe(set_clim, "value")

        log_ = widgets.Checkbox(
            value=False,
            description='Use Log scale:',
            disabled=False
        )

        def reset_colors(*args):
            vmin, vmax = data.CellData[data_display.ColorArrayName[1]].GetRange()
            cmin.value = vmin
            cmax.value = vmax
            tf = pvs.GetColorTransferFunction(data_display.ColorArrayName[1])
            vmin, _ = data.CellData[data_display.ColorArrayName[1]].GetRange()
            if tf.UseLogScale == 1 and vmin <= 1.0:
                cmin.value = 1.0

        def toggle_log(change):
            flag = change["new"]
            tf = pvs.GetColorTransferFunction(data_display.ColorArrayName[1])
            if flag:
                tf.MapControlPointsToLogSpace()
                tf.UseLogScale = 1
            else:
                tf.MapControlPointsToLinearSpace()
                tf.UseLogScale = 0
            # The log call can adjust the min, so update widgets to current values
            vmin, _ = data.CellData[data_display.ColorArrayName[1]].GetRange()
            if flag and vmin <= 1.0:
                cmin.value = 1.0
            return

        log_.observe(toggle_log, "value")


        reset = widgets.Button(
            description='Reset clim',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click me',
        )
        reset.on_click(reset_colors)

        scalars = widgets.Dropdown(
            options=list(data.CellData.keys()),
        #                      range(len(data.CellData.keys())))),
            value=data_display.ColorArrayName[1],
            description='Scalars:',
        )

        def set_active_scalars(change):
            # Clean up old scalars display to default
            toggle_log({"new": False})
            data_display.SetScalarBarVisibility(self._view, False)

            # Apply the change
            name = change["new"]
            pvs.ColorBy(data_display, ('CELLS', name))
            data_display.SetScalarBarVisibility(self._view, True)
            reset_colors()
            toggle_log({"new": False})
            log_.value = False
            return

        scalars.observe(set_active_scalars, 'value')

        self.layout = widgets.VBox([widgets.HBox([play, slider, scalars]),
              widgets.HBox([cmin, cmax, reset, log_]),
              self.vtk_display])
        #

    @property
    def frame(self):
        return self.layout

    def display(self):
        return self.frame
