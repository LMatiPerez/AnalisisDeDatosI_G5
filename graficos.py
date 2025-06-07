from scipy.stats import poisson
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class GraficoPrestamo:
    def __init__(self, nombre, probabilidad, n):
        
        self.nombre = nombre
        self.probabilidad = probabilidad
        self.n = n

    def etiqueta(self):
        return self.nombre
    
    def max(self):
        return poisson.ppf(0.99, self.probabilidad * self.n)
    
    def mu(self):
        return self.probabilidad * self.n

class GraficosProbabilidad:
    PRESTAMOS_FORMALES = 0
    PRESTAMOS_PERSONAS = 1
    CUOTAS_FIADO = 2

    CONFIGURACION_PRESTAMOS = {
        PRESTAMOS_FORMALES: (5, "Ha usado préstamos de financieras o bancos en el último mes"),
        PRESTAMOS_PERSONAS: (5, "Ha usado préstamos de familiares o amigos en el último mes"),
        CUOTAS_FIADO: (10, "Ha usado cuotas o fiado en el último mes"),
    }

    def graficos_prestamos(self, tabla, tipo_prestamo=PRESTAMOS_FORMALES):        
        graficos = self._datos_grafico_prestamos(tabla)
        plot_ = sns.pointplot(graficos[tipo_prestamo], x="x", y="p(x)", hue="Región", linestyles=":")
        for ind, label in enumerate(plot_.get_xticklabels()):
            if ind % self.CONFIGURACION_PRESTAMOS[tipo_prestamo][0] == 0:  
                label.set_visible(True)
            else:
                label.set_visible(False)
        plt.title(self.CONFIGURACION_PRESTAMOS[tipo_prestamo][1])

    def _datos_grafico_prestamos(self, tabla):      
        distribuciones = [[], [], []]
        for [etiqueta, _, _, _, _, p_prestamo_formal, p_prestamo_conocidos, p_fiado_cuotas] in tabla:
            distribuciones[0].append(GraficoPrestamo(etiqueta, p_prestamo_formal, 100))
            distribuciones[1].append(GraficoPrestamo(etiqueta, p_prestamo_conocidos, 100))
            distribuciones[2].append(GraficoPrestamo(etiqueta, p_fiado_cuotas, 100))

        return [self._dataframe_grafico(distribucioni) for distribucioni in distribuciones]    
        
    def _dataframe_grafico(self, distribuciones):
        xmax = max(dist.max() for dist in distribuciones)
        x = np.arange(0, xmax)
        data = []
        for i, distribucion in enumerate(distribuciones):
            for xi in x:
                data.append((distribucion.etiqueta(), xi, poisson.pmf(xi, distribucion.mu())))        
            
        return pd.DataFrame(data=data, columns=["Región", "x", "p(x)"])

class GraficosRegresion:
    def __init__(self, personas):
        self.personas = personas

    def correlacion_edad_ingresos(self):
        return self._personas()[["CH06", "P47T"]].corr()
    
    def correlacion_edad_log_ingresos(self):
        return self._ingresos_log10()[["CH06", "LOGP47T"]].corr()

    def correlacion_edad_media_ingresos(self):
        return self._ingresos_medios()[["CH06", "P47T"]].corr()

    def edad_ingresos(self):
        self._scatterplot(self._personas(), etiquetay="Ingresos en pesos", titulo="Ingresos de personas mayores de 18 años")

    def edad_log_ingresos(self):
        self._scatterplot(self._ingresos_log10(), var_y="LOGP47T", etiquetay="Log10 ingresos en pesos", titulo="Logaritmo de ingresos de personas mayores de 18 años")

    def edad_media_ingresos(self):
        self._scatterplot(self._ingresos_medios(), 
                          etiquetay="Media ingresos en pesos", 
                          titulo="Media ingresos de personas mayores de 18 años",
                          palette=["C1", "C0", "C2"])

    def _personas(self):
        return (self.personas
            .edad_mayor_o_igual_a(18)
            .ingresos_individuales_mayor_a(0)
            .region("Pampeana")
            .ingresos_sin_atipicos()
            .aplicar())

    def _ingresos_log10(self):
        df = self._personas()
        df["LOGP47T"] = np.log10(df["P47T"])
        return df
    
    def _ingresos_medios(self):
        media_general = self._personas().groupby(["CH06"], as_index=False)["P47T"].mean()
        media_general["genero_nombre"] = "Todos"
        return pd.concat([self._personas().groupby(["CH06", "genero_nombre"], as_index=False)["P47T"].mean(), media_general])

    def _scatterplot(self, 
                    df, 
                    var_y="P47T", 
                    titulo_ref="Género", 
                    etiquetax="Edad", 
                    etiquetay="Ingresos", 
                    titulo="Edad vs Ingresos",
                    palette=None):
        palette = palette or ["C1", "C0"]
        sns.scatterplot(df, x="CH06", y=var_y, hue="genero_nombre", palette=palette)
        plt.xlabel(etiquetax)
        plt.ylabel(etiquetay)
        plt.title(titulo)
        plt.legend(title=titulo_ref)
