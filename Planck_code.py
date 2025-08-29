import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import holoviews as hv

def get_app():
    pn.extension(sizing_mode="scale_both")
    pn.extension('tabulator')
    pn.extension('katex', 'mathjax')
    
    pars = pd.DataFrame(
        {"Color": ["Rojo", "Amarillo", "Verde", "Azul"], "Frecuencia": [4.54, 5.08, 5.31, 6.38], "Voltaje": [0., 0., 0., 0.]}
    )
    
    #"Voltaje": [1.43, 1.58, 1.62, 2.29]
    
    def compute_plot(value):
        my_plot = value.hvplot.scatter(x="Frecuencia", y="Voltaje", grid=True, height=540,
                                       s=300)
        my_plot.opts(fontscale=2)
        #line_plot = fit(value)
        return my_plot#*line_plot
    
    stylesheet = """
      .tabulator-cell {
        font-size: 28px;  // change font size
      }
      .tabulator-col-title {
        font-size: 28px;
    }
    """
    def fit(df):
        f = df["Frecuencia"].to_numpy()
        V = df["Voltaje"].to_numpy()
        a, b = np.polyfit(f, V, 1)
        x = np.linspace(min(f), max(f))
        g = lambda x: a*x+b
        e = 1.6e-19 #Coulomb
        #e = 1
        h = a*10**(-14)*e
        continous_df = pd.DataFrame({'x': x, 'g(x)': g(x)})
        line_plot = continous_df.hvplot.line(x="x", y="g(x)", line_width=12)
        return line_plot, h
    
    def compute_plot_with_fit(value):
        my_plot = compute_plot(value)
        line_plot, h = fit(value)
        exponente = int(np.floor(np.log10(abs(h))))
        mantisa = h / 10**exponente
        text = hv.Text(value["Frecuencia"].mean(), value["Voltaje"].mean(), f"h ≈ {mantisa:.2f} × 10^{exponente} Js",
                       fontsize=40)
        return my_plot * line_plot * text
    
    tabedit = pn.widgets.Tabulator(
        value=pars, show_index=False, selectable=True, theme="default", disabled=False,
                                    stylesheets=[stylesheet])
    #plot = pn.bind(compute_plot, value=tabedit)
    table_value_rx = pn.rx(tabedit.param.value)
    plot = pn.rx(compute_plot)(table_value_rx)
    hv_pane = pn.pane.HoloViews(plot, sizing_mode="scale_both")
    
    button = pn.widgets.Button(name="Calcular constante de Planck", button_type="primary")
    def b(event):
        full_plot = compute_plot_with_fit(tabedit.value)
        hv_pane.object = full_plot
    
    button.on_click(b)
    dash = pn.Row(pn.Column(tabedit, button), hv_pane)
    return dash