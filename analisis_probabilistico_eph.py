import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Configuración de visualización
plt.style.use('seaborn')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)

# 1. Probabilidades empíricas simples
def calcular_probabilidades_simples(datos):
    """
    Calcula probabilidades simples para eventos de interés
    """
    print("\n1. PROBABILIDADES SIMPLES")
    print("-" * 50)
    
    # P(Educación universitaria)
    p_univ = (datos['nivel_educativo'] == 'Universitario completo').mean()
    print(f"P(Universitario completo) = {p_univ:.3f}")
    print("→ Interpretación: Solo {:.1f}% de la población tiene estudios universitarios completos".format(p_univ*100))
    
    # P(Desocupado)
    p_desoc = datos['desocupado'].mean()
    print(f"\nP(Desocupado) = {p_desoc:.3f}")
    print("→ Interpretación: La tasa de desocupación es del {:.1f}%".format(p_desoc*100))
    
    # P(Sin baño)
    p_sin_banio = (datos['baño'] == 0).mean()
    print(f"\nP(Sin baño) = {p_sin_banio:.3f}")
    print("→ Interpretación: El {:.1f}% de la población no tiene baño en su vivienda".format(p_sin_banio*100))
    
    # P(Universitario Y Desocupado) - Intersección
    p_univ_desoc = ((datos['nivel_educativo'] == 'Universitario completo') & 
                    (datos['desocupado'] == 1)).mean()
    print(f"\nP(Universitario ∩ Desocupado) = {p_univ_desoc:.3f}")
    
    # P(Universitario O Desocupado) - Unión
    p_univ_o_desoc = ((datos['nivel_educativo'] == 'Universitario completo') | 
                      (datos['desocupado'] == 1)).mean()
    print(f"\nP(Universitario ∪ Desocupado) = {p_univ_o_desoc:.3f}")
    
    return p_univ, p_desoc, p_univ_desoc

# 2. Probabilidades condicionales
def calcular_probabilidades_condicionales(datos):
    """
    Calcula probabilidades condicionales relevantes
    """
    print("\n2. PROBABILIDADES CONDICIONALES")
    print("-" * 50)
    
    # P(Desocupado | Universitario)
    p_desoc_dado_univ = datos[datos['nivel_educativo'] == 'Universitario completo']['desocupado'].mean()
    print(f"P(Desocupado | Universitario) = {p_desoc_dado_univ:.3f}")
    print("→ Interpretación: Entre las personas con título universitario, "
          f"el {p_desoc_dado_univ*100:.1f}% está desocupado")
    
    # P(Desocupado | Sin Universidad)
    p_desoc_dado_no_univ = datos[datos['nivel_educativo'] != 'Universitario completo']['desocupado'].mean()
    print(f"\nP(Desocupado | No Universitario) = {p_desoc_dado_no_univ:.3f}")
    print("→ Interpretación: La tasa de desocupación es "
          f"{'mayor' if p_desoc_dado_no_univ > p_desoc_dado_univ else 'menor'} "
          "en personas sin título universitario")
    
    return p_desoc_dado_univ, p_desoc_dado_no_univ

# 3. Verificación de independencia
def verificar_independencia(datos):
    """
    Verifica la independencia entre pares de variables
    """
    print("\n3. VERIFICACIÓN DE INDEPENDENCIA")
    print("-" * 50)
    
    # Educación universitaria y desocupación
    univ = (datos['nivel_educativo'] == 'Universitario completo')
    desoc = (datos['desocupado'] == 1)
    
    p_univ = univ.mean()
    p_desoc = desoc.mean()
    p_univ_desoc = (univ & desoc).mean()
    
    print("Test de independencia entre educación universitaria y desocupación:")
    print(f"P(U ∩ D) = {p_univ_desoc:.3f}")
    print(f"P(U) * P(D) = {(p_univ * p_desoc):.3f}")
    print("→ Interpretación: Los eventos", 
          "son independientes" if np.abs(p_univ_desoc - (p_univ * p_desoc)) < 0.01 
          else "no son independientes")

# 4. Teorema de Bayes
def aplicar_teorema_bayes(datos):
    """
    Aplica el teorema de Bayes para calcular probabilidades condicionales inversas
    """
    print("\n4. TEOREMA DE BAYES")
    print("-" * 50)
    
    # P(Universitario | Desocupado) = P(Desocupado | Universitario) * P(Universitario) / P(Desocupado)
    univ = (datos['nivel_educativo'] == 'Universitario completo')
    desoc = (datos['desocupado'] == 1)
    
    p_univ = univ.mean()
    p_desoc = desoc.mean()
    p_desoc_dado_univ = datos[univ]['desocupado'].mean()
    
    p_univ_dado_desoc = (p_desoc_dado_univ * p_univ) / p_desoc
    
    print(f"P(Universitario | Desocupado) = {p_univ_dado_desoc:.3f}")
    print("→ Interpretación: Entre los desocupados, "
          f"el {p_univ_dado_desoc*100:.1f}% tiene título universitario")

# 5 y 6. Modelado con distribuciones de probabilidad
def modelar_distribuciones(datos):
    """
    Modela variables con distribuciones teóricas y calcula probabilidades
    """
    print("\n5 y 6. MODELADO CON DISTRIBUCIONES")
    print("-" * 50)
    
    # Modelado de ocupados por hogar (Poisson)
    lambda_ocupados = datos['ocupados_hogar'].mean()
    poisson_ocupados = stats.poisson(lambda_ocupados)
    
    # P(Ocupados > 2)
    p_mas_2_ocupados = 1 - poisson_ocupados.cdf(2)
    print(f"P(Ocupados > 2) según Poisson = {p_mas_2_ocupados:.3f}")
    print("→ Interpretación: La probabilidad de que un hogar tenga más de 2 personas ocupadas "
          f"es del {p_mas_2_ocupados*100:.1f}%")
    
    # Modelado de ingresos (Normal)
    mu_ingresos = datos['ingresos'].mean()
    sigma_ingresos = datos['ingresos'].std()
    normal_ingresos = stats.norm(mu_ingresos, sigma_ingresos)
    
    # P(Ingreso > promedio + 1 desv. est.)
    umbral_alto = mu_ingresos + sigma_ingresos
    p_ingreso_alto = 1 - normal_ingresos.cdf(umbral_alto)
    print(f"\nP(Ingreso > μ + σ) según Normal = {p_ingreso_alto:.3f}")
    print("→ Interpretación: Aproximadamente el {:.1f}% de la población tiene ingresos "
          "superiores a 1 desviación estándar sobre la media".format(p_ingreso_alto*100))

# 7. Visualización de distribuciones
def visualizar_distribuciones(datos):
    """
    Crea gráficos comparando distribuciones empíricas vs teóricas
    """
    # Distribución de ocupados por hogar
    plt.figure(figsize=(15, 5))
    
    # Subplot 1: Ocupados por hogar (empírico vs Poisson)
    plt.subplot(1, 2, 1)
    sns.histplot(data=datos, x='ocupados_hogar', stat='probability', discrete=True, label='Empírico')
    
    lambda_ocupados = datos['ocupados_hogar'].mean()
    x = np.arange(0, datos['ocupados_hogar'].max() + 1)
    poisson_pmf = stats.poisson.pmf(x, lambda_ocupados)
    plt.plot(x, poisson_pmf, 'r-', label='Poisson teórica')
    
    plt.title('Distribución de ocupados por hogar')
    plt.xlabel('Número de ocupados')
    plt.ylabel('Probabilidad')
    plt.legend()
    
    # Subplot 2: Ingresos (empírico vs Normal)
    plt.subplot(1, 2, 2)
    sns.histplot(data=datos, x='ingresos', stat='density', label='Empírico')
    
    x = np.linspace(datos['ingresos'].min(), datos['ingresos'].max(), 100)
    normal_pdf = stats.norm.pdf(x, datos['ingresos'].mean(), datos['ingresos'].std())
    plt.plot(x, normal_pdf, 'r-', label='Normal teórica')
    
    plt.title('Distribución de ingresos')
    plt.xlabel('Ingreso')
    plt.ylabel('Densidad')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('distribuciones.png')
    plt.close()

def main(datos):
    """
    Función principal que ejecuta todos los análisis
    """
    print("ANÁLISIS PROBABILÍSTICO DE DATOS DE LA EPH")
    print("=" * 50)
    
    # Ejecutar todos los análisis
    p_univ, p_desoc, p_univ_desoc = calcular_probabilidades_simples(datos)
    calcular_probabilidades_condicionales(datos)
    verificar_independencia(datos)
    aplicar_teorema_bayes(datos)
    modelar_distribuciones(datos)
    visualizar_distribuciones(datos)

if __name__ == "__main__":
    try:
        # Intentar cargar datos procesados
        try:
            print("Intentando cargar datos procesados...")
            datos = pd.read_pickle('datos_procesados.pkl')
        except FileNotFoundError:
            print("Datos procesados no encontrados. Procesando datos desde archivos originales...")
            from preparar_datos_eph import cargar_datos
            datos = cargar_datos()
        
        # Ejecutar análisis
        main(datos)
        
    except Exception as e:
        print(f"Error durante el análisis: {str(e)}")
        print("Asegúrate de que los archivos de datos estén en el directorio correcto:") 