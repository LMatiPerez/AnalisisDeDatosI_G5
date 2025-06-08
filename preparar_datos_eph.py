import pandas as pd
import numpy as np
from datetime import datetime

def es_fecha(valor):
    """
    Verifica si un valor es una fecha en formato string
    """
    return isinstance(valor, str) and ('00:00:00' in valor or isinstance(valor, datetime.date))

def limpiar_columna_numerica(serie):
    """
    Limpia una columna numérica, convirtiendo fechas y otros valores no válidos a NaN
    """
    return pd.to_numeric(serie.apply(lambda x: np.nan if es_fecha(x) else x), errors='coerce')

def cargar_datos():
    """
    Carga y prepara los datos de la EPH combinando las bases de hogares e individuos
    """
    # Cargar las bases
    print("Cargando bases de datos...")
    personas = pd.read_excel('usu_individual_T324.xlsx')
    
    # Preparar variables para el análisis
    print("Preparando variables...")
    
    # 1. Nivel educativo
    nivel_educ = {
        1: 'Primario incompleto',
        2: 'Primario completo',
        3: 'Secundario incompleto',
        4: 'Secundario completo',
        5: 'Superior universitario incompleto',
        6: 'Superior universitario completo',
        7: 'Sin instrucción',
        9: 'Ns/Nr'
    }
    personas['nivel_educativo'] = personas['nivel_educativo'].apply(
        lambda x: nivel_educ.get(x) if not es_fecha(x) else np.nan
    )
    
    # 2. Ingresos (limpiar valores negativos y missing)
    personas['ingresos'] = limpiar_columna_numerica(personas['ingreso'])
    personas.loc[personas['ingresos'] < 0, 'ingresos'] = np.nan
    
    # 3. Estado de actividad
    estado_act = {
        1: 'Ocupado',
        2: 'Desocupado',
        3: 'Inactivo',
        4: 'Menor de 10 años'
    }
    personas['estado_actividad'] = personas['estado_actividad'].apply(
        lambda x: estado_act.get(x) if not es_fecha(x) else np.nan
    )
    personas['desocupado'] = (personas['estado_actividad'] == 'Desocupado').astype(int)
    
    # 4. Sexo (1 = Varón, 2 = Mujer)
    personas['sexo'] = personas['sexo'].apply(
        lambda x: 'Varón' if x == 1 else ('Mujer' if x == 2 else np.nan)
    )
    
    # 5. Edad (limpiar valores no válidos)
    personas['edad'] = limpiar_columna_numerica(personas['edad'])
    personas.loc[personas['edad'] < 0, 'edad'] = np.nan
    
    # 6. Variables binarias (Sí/No)
    for col in ['compra_cuotas', 'prestamo_personas', 'prestamo_banco']:
        personas[col] = personas[col].apply(
            lambda x: 'Sí' if x == 1 else ('No' if x == 2 else np.nan)
        )
    
    # 7. Ocupados por hogar
    personas['ocupados_hogar'] = personas.groupby(['id_vivienda', 'id_hogar']).apply(
        lambda x: (x['estado_actividad'] == 'Ocupado').sum()
    ).reset_index(level=[0,1], drop=True)
    
    # 8. Región
    regiones = {
        1: 'Gran Buenos Aires',
        40: 'NOA',
        41: 'NEA',
        42: 'Cuyo',
        43: 'Pampeana',
        44: 'Patagonia'
    }
    personas['region'] = personas['region'].apply(
        lambda x: regiones.get(x) if not es_fecha(x) else np.nan
    )
    
    # Limpiar datos
    print("Limpiando datos...")
    variables_necesarias = [
        'nivel_educativo', 'ingresos', 'desocupado', 'sexo', 
        'edad', 'compra_cuotas', 'ocupados_hogar', 'region',
        'prestamo_personas', 'prestamo_banco', 'estado_actividad'
    ]
    
    datos = personas[variables_necesarias].copy()
    
    # Eliminar registros con valores faltantes en variables clave
    variables_requeridas = [
        'nivel_educativo', 'ingresos', 'estado_actividad',
        'sexo', 'edad', 'region'
    ]
    datos = datos.dropna(subset=variables_requeridas)
    
    print(f"Datos preparados. Dimensiones finales: {datos.shape}")
    
    # Guardar datos procesados
    datos.to_pickle('datos_procesados.pkl')
    print("Datos guardados en 'datos_procesados.pkl'")
    
    # Mostrar resumen de valores únicos por variable
    print("\nValores únicos por variable:")
    for col in datos.columns:
        print(f"\n{col}:")
        print(datos[col].value_counts().head())
    
    return datos

if __name__ == "__main__":
    try:
        datos = cargar_datos()
        print("\nResumen estadístico de variables numéricas:")
        print(datos[['edad', 'ingresos', 'ocupados_hogar']].describe())
    except Exception as e:
        print(f"Error al procesar los datos: {str(e)}") 