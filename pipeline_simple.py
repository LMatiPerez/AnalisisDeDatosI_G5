import pandas as pd
import numpy as np

def construir_base_limpia(path_personas, path_hogares,
                          out_csv_completo="base_completa_personas_hogares.csv",
                          out_csv_filtrado="base_pampeana_analizada.csv"):

    # 1. Cargar las bases originales
    personas = pd.read_excel(path_personas)
    hogares = pd.read_excel(path_hogares)

    # 2. Renombrar columnas principales
    personas = personas.rename(columns={
        "CH04": "sexo", "CH05": "fecha_nacimiento", "CH06": "edad",
        "P47T": "ingreso", "NIVEL_ED": "nivel_educativo", "ESTADO": "estado_actividad",
        "CODUSU": "id_vivienda", "NRO_HOGAR": "id_hogar", "REGION": "region"
    })

    hogares = hogares.rename(columns={
        "V14": "prestamo_personas", "V15": "prestamo_banco", "V16": "compra_cuotas",
        "CODUSU": "id_vivienda", "NRO_HOGAR": "id_hogar", "REGION": "region"
    })

    # 3. Seleccionar solo columnas necesarias
    personas = personas[["id_vivienda", "id_hogar", "region", "sexo", "fecha_nacimiento", "edad",
                         "estado_actividad", "nivel_educativo", "ingreso"]]
    hogares = hogares[["id_vivienda", "id_hogar", "prestamo_personas", "prestamo_banco", "compra_cuotas"]]

    # 4. Combinar personas y hogares
    df_completo = pd.merge(personas, hogares, on=["id_vivienda", "id_hogar"], how="inner")

    # --- Guardar versión completa para análisis generales ---
    df_completo.to_csv(out_csv_completo, index=False)
    print(f"[OK] Base combinada exportada a {out_csv_completo} con {len(df_completo)} filas.")

    # 5. Filtrar región Pampeana
    df_filtrado = df_completo[df_completo["region"] == 43].copy()

    # 6. Filtrar mayores de 18 años
    df_filtrado = df_filtrado[df_filtrado["edad"] >= 18]

    # 7. Filtrar personas con ingreso positivo
    df_filtrado = df_filtrado[df_filtrado["ingreso"] > 0]


    # Guardar versión filtrada final
    df_filtrado.to_csv(out_csv_filtrado, index=False)
    print(f"[OK] Base filtrada exportada a {out_csv_filtrado} con {len(df_filtrado)} filas.")

    return df_completo, df_filtrado


# Ejecución directa para probar
if __name__ == "__main__":
    construir_base_limpia(
        path_personas="usu_individual_T324.xlsx",
        path_hogares="usu_hogar_T324.xlsx",
        out_csv_completo="base_completa_personas_hogares.csv",
        out_csv_filtrado="base_pampeana_analizada.csv"
    )
