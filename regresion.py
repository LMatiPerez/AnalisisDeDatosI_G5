import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import seaborn as sns 
import matplotlib.pyplot as plt

def linear(x, a, b):
    return a*x+b

def quadratic(x, a, b, c):
    return a*x**2+b*x+c

def cubic(x, a, b, c, d):
    return a*x**3+b*x**2+c*x+d

def rcuadrado(ys, fn, xi, params):
    residuos = ys - fn(xi, *params)
    ss_res = np.sum(residuos**2)
    ss_tot = np.sum((ys-np.mean(ys))**2)
    return 1-ss_res/ss_tot

class RegresionMediaIngresosEdad:
    def __init__(self, personas):
        base = (personas
            .edad_mayor_o_igual_a(18)
            .ingresos_individuales_mayor_a(0)
            .region("Pampeana")
            .ingresos_sin_atipicos()
            .aplicar())
        media_por_genero = base.groupby(["CH06", "genero_nombre"], as_index=False)["P47T"].mean()
        media_general = base.groupby(["CH06"], as_index=False)["P47T"].mean()
        media_general["genero_nombre"] = "Todos"
        self.df = pd.concat([media_por_genero, media_general])

    def ajuste_lineal(self):
        return self._ajuste(linear, *self._dfs(), title="Ajuste lineal edad vs media ingresos")
    
    def ajuste_lineal_residuos(self):
        self._residuos(linear, *self._dfs(), title="Residuos del ajuste lineal edad vs media ingresos" )

    def ajuste_cuadratico(self):
        return self._ajuste(quadratic, *self._dfs(), title="Ajuste cuadrático edad vs media ingresos")
    
    def ajuste_cuadratico_residuos(self):
        self._residuos(quadratic, *self._dfs(), title="Residuos del ajuste cuadrático edad vs media ingresos")

    def ajuste_cubico(self):
        return self._ajuste(cubic, *self._dfs(), title="Ajuste cúbico edad vs media ingresos")
    
    def ajuste_cubic_residuos(self):
        self._residuos(cubic, *self._dfs(), title="Residuos del ajuste cúbico edad vs media ingresos")

    def _ajuste(self, fn, *dfs, ax=None, title=None):
        r2s = []
        colors = self._colors()
        for i, (etiqueta, df) in enumerate(dfs):
            params, _ = curve_fit(fn, df["CH06"], df["P47T"])    
            xi = df["CH06"]
            yi = np.array([fn(x, *params) for x in xi])
            r2 = rcuadrado(df["P47T"], fn, df["CH06"], params)
            sns.scatterplot(df, x="CH06", y="P47T", ax=ax)
            sns.lineplot(data=None, x=xi, y=yi, ax=ax, label=f"{etiqueta} R²={r2:.3f}", color=colors[i])
            r2s.append(r2)

        plt.title(title)
        plt.xlabel("Edad")
        plt.ylabel("Media ingresos")
        return r2s    

    def _residuos(self, fn, *dfs, ax=None, title=None):
        referencias = []
        colors = self._colors()
        for i, (etiqueta, df) in enumerate(dfs):
            referencias.append(etiqueta)
            params, _ = curve_fit(fn, df["CH06"], df["P47T"])    
            xi = df["CH06"]
            yi = df["P47T"] - np.array([fn(x, *params) for x in xi])
            sns.scatterplot(x=xi, y=yi, ax=ax, color=colors[i])
        plt.legend(referencias)
        plt.title(title)
        plt.xlabel("Edad")
        plt.ylabel("Media ingresos")

    def _dfs(self):
        return (("Mujer", self.df[self.df["genero_nombre"]=="Mujer"]),
                ("Varón", self.df[self.df["genero_nombre"]=="Varón"]),
                ("Todos", self.df[self.df["genero_nombre"]=="Todos"]))
    
    def _colors(self):
        palette = sns.color_palette("tab10")
        return [palette[1], palette[0], palette[2]]