import pandas as pd

class EncuestaHogares:
    SELECCION_HOGARES = {
            "V14": "prestamo_personas",
            "V15": "prestamo_banco",
            "V16": "compra_cuotas",
            "CODUSU": "id_vivienda",
            "NRO_HOGAR": "id_hogar",
            "REGION": "region"
        }
    SELECCION_PERSONAS = {
            "CH04": "sexo",
            "CH06": "edad",
            "P47T": "ingreso",
            "PONDII": "ingreso_ponderado",
            "NIVEL_ED": "nivel_educativo",
            "ESTADO": "estado_actividad",
            "CODUSU": "id_vivienda",
            "NRO_HOGAR": "id_hogar",
            "REGION": "region"
        }
    
    def __init__(self, archivo_hogares, archivo_personas):
        self.archivo_hogares = archivo_hogares
        self.archivo_personas = archivo_personas

    def memoria(self):
        return (self._columnas_renombradas(pd.read_excel(self.archivo_hogares), self.SELECCION_HOGARES), 
                self._columnas_renombradas(pd.read_excel(self.archivo_personas), self.SELECCION_PERSONAS))
    
    def subconjunto_columnas(self, hogares, personas):
        return (hogares[list(self.SELECCION_HOGARES.values())],
                personas[list(self.SELECCION_PERSONAS.values())])
    
    def filtrados_por_region(self, region, hogares, personas):
        return hogares[hogares['region'] == region], personas[personas['region'] == region]        
    
    def df_hogares_personas(self, hogares, personas):
        return pd.merge(personas, hogares, on=['id_vivienda', 'id_hogar'], how='inner')

    @staticmethod
    def _columnas_renombradas(df, mapeo):
        return df.rename(columns=mapeo)
    
