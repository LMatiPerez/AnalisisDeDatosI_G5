import pandas as pd
import logging

logger = logging.getLogger(__name__)

COLUMNAS_HOGARES = ['CODUSU', 'ANO4', 'TRIMESTRE', 'NRO_HOGAR', 'REALIZADA', 'REGION', 'MAS_500', 'AGLOMERADO', 'PONDERA', 'IV1', 'IV1_ESP', 'IV2', 'IV3', 'IV3_ESP', 'IV4', 'IV5', 'IV6', 'IV7', 'IV7_ESP', 'IV8', 'IV9', 'IV10', 'IV11', 'IV12_1', 'IV12_2', 'IV12_3', 'II1', 'II2', 'II3', 'II3_1', 'II4_1', 'II4_2', 'II4_3', 'II5', 'II5_1', 'II6', 'II6_1', 'II7', 'II7_ESP', 'II8', 'II8_ESP', 'II9', 'V1', 'V2', 'V21', 'V22', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16', 'V17', 'V18', 'V19_A', 'V19_B', 'IX_TOT', 'IX_MEN10','IX_MAYEQ10', 'ITF', 'DECIFR', 'IDECIFR', 'RDECIFR', 'GDECIFR', 'PDECIFR', 'ADECIFR', 'IPCF', 'DECCFR', 'IDECCFR', 'RDECCFR', 'GDECCFR', 'PDECCFR', 'ADECCFR', 'PONDIH', 'VII1_1', 'VII1_2', 'VII2_1', 'VII2_2','VII2_3', 'VII2_4']
COLUMNAS_PERSONAS =['CODUSU', 'ANO4', 'TRIMESTRE', 'NRO_HOGAR', 'COMPONENTE', 'H15', 'REGION', 'MAS_500', 'AGLOMERADO', 'PONDERA', 'CH03', 'CH04', 'CH05', 'CH06', 'CH07', 'CH08', 'CH09', 'CH10', 'CH11', 'CH12', 'CH13', 'CH14', 'CH15', 'CH15_COD', 'CH16', 'CH16_COD', 'NIVEL_ED', 'ESTADO', 'CAT_OCUP', 'CAT_INAC', 'IMPUTA', 'PP02C1', 'PP02C2', 'PP02C3', 'PP02C4', 'PP02C5', 'PP02C6', 'PP02C7', 'PP02C8', 'PP02E', 'PP02H', 'PP02I', 'PP03C', 'PP03D', 'PP3E_TOT', 'PP3F_TOT', 'PP03G', 'PP03H', 'PP03I', 'PP03J', 'INTENSI', 'PP04A', 'PP04B_COD', 'PP04B1', 'PP04B2', 'PP04B3_MES', 'PP04B3_ANO', 'PP04B3_DIA', 'PP04C', 'PP04C99', 'PP04D_COD', 'PP04G', 'PP05B2_MES', 'PP05B2_ANO', 'PP05B2_DIA', 'PP05C_1', 'PP05C_2', 'PP05C_3', 'PP05E', 'PP05F', 'PP05H', 'PP06A', 'PP06C', 'PP06D', 'PP06E', 'PP06H', 'PP07A', 'PP07C', 'PP07D', 'PP07E', 'PP07F1', 'PP07F2', 'PP07F3', 'PP07F4', 'PP07F5', 'PP07G1', 'PP07G2', 'PP07G3', 'PP07G4', 'PP07G_59', 'PP07H', 'PP07I', 'PP07J', 'PP07K', 'PP08D1', 'PP08D4', 'PP08F1', 'PP08F2', 'PP08J1', 'PP08J2', 'PP08J3', 'PP09A', 'PP09A_ESP', 'PP09B', 'PP09C', 'PP09C_ESP', 'PP10A', 'PP10C', 'PP10D', 'PP10E', 'PP11A', 'PP11B_COD', 'PP11B1', 'PP11B2_MES', 'PP11B2_ANO', 'PP11B2_DIA', 'PP11C', 'PP11C99', 'PP11D_COD', 'PP11G_ANO', 'PP11G_MES', 'PP11G_DIA', 'PP11L', 'PP11L1', 'PP11M', 'PP11N', 'PP11O', 'PP11P', 'PP11Q', 'PP11R', 'PP11S', 'PP11T', 'P21', 'DECOCUR', 'IDECOCUR', 'RDECOCUR', 'GDECOCUR', 'PDECOCUR', 'ADECOCUR', 'PONDIIO', 'TOT_P12', 'P47T', 'DECINDR', 'IDECINDR', 'RDECINDR', 'GDECINDR', 'PDECINDR', 'ADECINDR', 'PONDII', 'V2_M', 'V3_M', 'V4_M', 'V5_M', 'V8_M', 'V9_M', 'V10_M', 'V11_M', 'V12_M', 'V18_M', 'V19_AM', 'V21_M', 'T_VI', 'ITF', 'DECIFR', 'IDECIFR', 'RDECIFR', 'GDECIFR', 'PDECIFR', 'ADECIFR', 'IPCF', 'DECCFR', 'IDECCFR', 'RDECCFR', 'GDECCFR', 'PDECCFR', 'ADECCFR', 'PONDIH']

ESTADO = pd.DataFrame([
    (0, "Encuesta no realizada"),
    (1, "Ocupado"),
    (2, "Desocupado"),
    (3, "Inactivo"),
    (4, "Menor de 10 años")
], columns=["estado_actividad", "estado_nombre"])

GENERO = pd.DataFrame([
    (1, "Varón"),
    (2, "Mujer")
], columns=["genero", "genero_nombre"])

NIVEL_EDUCATIVO = pd.DataFrame([
    (1, "Primario incompleto (incluye educación especial)", 1),
    (2, "Primario completo", 2),
    (3, "Secundario incompleto", 3),
    (4, "Secundario completo", 4),
    (5, "Superior universitario incompleto", 5),
    (6, "Superior universitario completo", 6),
    (7, "Sin instrucción", 0),
    (9, "Ns/Nr", 9),
    ], columns=["nivel_educativo", "nivel_educativo_nombre", "nivel_educativo_orden"])

REGION = pd.DataFrame([
    (1, "Gran Buenos Aires"),
    (40, "Noroeste"),
    (41, "Noreste"),
    (42, "Cuyo"),
    (43, "Pampeana"),
    (44, "Patagonia")], columns=("region", "region_nombre"))

class EPH:
    def __init__(self, archivo_hogares: str, archivo_personas: str):
        logger.info("Cargando hogares...")
        self.hogares = (pd.read_excel(archivo_hogares)
            .merge(REGION, left_on="REGION", right_on="region", how="inner"))
        logger.info("Hogares finalizado %d unidades.", len(self.hogares))
        logger.info("Cargando personas...")
        self.personas = (pd.read_excel(archivo_personas)
            .merge(REGION, left_on="REGION", right_on="region", how="inner")
            .merge(NIVEL_EDUCATIVO, left_on="NIVEL_ED", right_on="nivel_educativo", how="inner")
            .merge(ESTADO, left_on="ESTADO", right_on="estado_actividad", how="inner")
            .merge(GENERO, left_on="CH04", right_on="genero", how="inner"))
        logger.info("Personas finalizado %d unidades.", len(self.personas))
        
class Personas:
    def __init__(self, personas):
        self.personas = personas
        self.filtros = []
    
    def region(self, region_nombre):
        self.filtros.append((f"Personas con region={region_nombre}", lambda df: df[df["region_nombre"]==region_nombre]))
        return self
    
    def edad_mayor_o_igual_a(self, edad):
        self.filtros.append((f"Personas con edad>={edad}", lambda df: df[df["CH06"]>=edad]))
        return self

    def edad_menor_o_igual_a(self, edad):
        self.filtros.append((f"Personas con edad<={edad}", lambda df: df[df["CH06"]<=edad]))
        return self

    def nivel_educativo(self, *nivel_educativo_nombre):
        self.filtros.append((f"Personas con nivel educativo={nivel_educativo_nombre}", lambda df: df[df["nivel_educativo_nombre"].isin(nivel_educativo_nombre)]))
        return self

    def ingresos_individuales_mayor_a(self, ingresos):
        self.filtros.append((f"Personas con ingresos > {ingresos}", lambda df: df[df["P47T"]>ingresos]))
        return self
    
    def ingresos_atipicos(self):
        self.filtros.append(("Personas con ingresos <= Q3 + 1.5 IQR",lambda df: df[df["P47T"]>self._limite_superior_ingreso_individual(df)]))
        return self

    def ingresos_sin_atipicos(self):
        self.filtros.append(("Personas con ingresos [Q1 - 1.5 IQR, Q3 + 1.5 IQR]",lambda df: df[(df["P47T"]<=self._limite_superior_ingreso_individual(df))&(df["P47T"]>=self._limite_inferior_ingreso_individual(df))]))
        return self


    def ingresos_sin_atipicos_superior(self):
        self.filtros.append(("Personas con ingresos <= Q3 + 1.5 IQR",lambda df: df[df["P47T"]<=self._limite_superior_ingreso_individual(df)]))
        return self

    def ingresos_sin_atipicos_inferior(self):
        self.filtros.append(("Personas con ingresos >= Q1 - 1.5 IQR",lambda df: df[df["P47T"]>=self._limite_inferior_ingreso_individual(df)]))
        return self

    def estado_ocupacion(self, estado_nombre):
        self.filtros.append((f"Personas con estado ocupación = {estado_nombre}",lambda df: df[df["estado_nombre"]==estado_nombre]))
        return self
    
    def genero(self, genero_nombre):
        self.filtros.append((f"Personas con género = {genero_nombre}",lambda df: df[df["genero_nombre"]==genero_nombre]))
        return self

    def aplicar(self):
        df = self.personas
        for descripcion, filtro in self.filtros:
            logger.info("\t%s", descripcion)
            df = filtro(df)
        return df

    def _limite_superior_ingreso_individual(self, df):
        [q1, q3] = df["P47T"].quantile([0.25,0.75]).to_list()
        iqr = q3 - q1
        res = q3 + 1.5 * iqr
        logger.info("_limite_superior_ingreso_individual: $ %.2f", res)
        return res 

    def _limite_inferior_ingreso_individual(self, df):
        [q1, q3] = df["P47T"].quantile([0.25,0.75]).to_list()
        iqr = q3 - q1
        res= q1 - 1.5 * iqr
        logger.info("_limite_inferior_ingreso_individual: $ %.2f", res)
        return res

class Hogares:
    def __init__(self, hogares):
        self.hogares = hogares
        self.filtros = []

    def con_personas_en(self, personas):
        self.filtros.append(("Hogares con personas", lambda df: df[df.set_index(["CODUSU", "NRO_HOGAR"]).index.isin(personas.set_index(["CODUSU", "NRO_HOGAR"]).index)]))
        return self
    
    def con_prestamo_formal(self, tiene=True):
        self.filtros.append((f"Con préstamo formal", lambda df: df[df["V15"]==1 if tiene else 2]))
        return self
    
    def con_cuotas_o_fiado(self, tiene=True):
        self.filtros.append((f"Con cuotas o fiado", lambda df: df[df["V16"]==1 if tiene else 2]))
        return self

    def con_prestamo_de_conocidos(self, tiene=True):
        self.filtros.append((f"Con préstamo de conocidos", lambda df: df[df["V14"]==1 if tiene else 2]))
        return self

    def con_region(self, region_nombre):
        self.filtros.append((f"Con region {region_nombre}", lambda df: df[df["region_nombre"]==region_nombre]))
        return self

    def aplicar(self):
        df = self.hogares
        for descripcion, filtro in self.filtros:
            logger.info("\t%s", descripcion)
            df = filtro(df)
        return df
