import pandas as pd

# Diccionario actualizado de LADAS por estado
ladas_por_estado = {
    "Aguascalientes": [449], "Baja California": [664, 686, 653], "Baja California Sur": [612, 624],
    "Campeche": [981, 938], "Chiapas": [961, 962, 963, 964, 967], "Chihuahua": [614, 656, 625, 627, 639],
    "CDMX": [55, 56], "Coahuila": [844, 871, 878, 866], "Colima": [312, 313, 314],
    "Durango": [618, 671, 672], "Estado de México": [722, 729, 721, 715, 563, 712, 720],
    "Guanajuato": [477, 462, 464, 445, 415, 461], "Guerrero": [747, 755, 744, 762, 757],
    "Hidalgo": [771, 774, 775], "Jalisco": [33, 341, 342, 343, 375, 322],
    "Michoacán": [443, 351, 353, 354, 434], "Morelos": [777, 735], "Nayarit": [311, 323],
    "Nuevo León": [81, 826, 821], "Oaxaca": [951, 953, 954, 958], "Puebla": [222, 231, 232, 221, 223, 225, 749],
    "Querétaro": [442, 441, 427], "Quintana Roo": [998, 987, 983, 984],
    "San Luis Potosí": [444, 487], "Sinaloa": [667, 669, 687], "Sonora": [662, 631, 647, 644],
    "Tabasco": [993, 917], "Tamaulipas": [834, 868, 899, 833], "Tlaxcala": [246, 241],
    "Veracruz": [229, 271, 272, 228, 285, 296, 921], "Yucatán": [999, 997, 988], "Zacatecas": [492, 493]
}

def clasificar_numeros(ruta_ods):
    """
    Clasifica los números de teléfono por LADA, agrega el prefijo +521 y los separa por estado en hojas distintas.
    
    Parámetros:
        ruta_ods (str): Ruta del archivo ODS que contiene los números en una columna llamada 'Numero'.
    """
    try:
        # Cargar el archivo ODS
        df = pd.read_excel(ruta_ods, engine="odf")
        
        # Asegurar que la columna de números es de tipo texto
        df['Numero'] = df['Numero'].astype(str).str.strip()
        
        # Diccionario para almacenar los números clasificados
        numeros_clasificados = {estado: [] for estado in ladas_por_estado}
        numeros_clasificados["No identificado"] = []  # Para LADAS no encontradas

        for numero in df['Numero']:
            lada_encontrada = False

            for estado, ladas in ladas_por_estado.items():
                if any(numero.startswith(str(lada)) for lada in ladas):
                    numeros_clasificados[estado].append(f"+521{numero}")
                    lada_encontrada = True
                    break
            
            if not lada_encontrada:
                numeros_clasificados["No identificado"].append(f"+521{numero}")

        # Guardar los resultados en hojas separadas en un nuevo archivo ODS
        resultado_ods = "numeros_clasificados_separados.ods"
        with pd.ExcelWriter(resultado_ods, engine="odf") as writer:
            for estado, numeros in numeros_clasificados.items():
                if numeros:  # Solo crear hojas con datos
                    pd.DataFrame(numeros, columns=["Numero"]).to_excel(writer, sheet_name=estado, index=False)

        print(f"Archivo '{resultado_ods}' generado correctamente en hojas separadas.")
        return resultado_ods

    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return None

# Uso: Ejecutar con la ruta correcta del archivo ODS
resultado = clasificar_numeros("/home/jonatan/Documentos/prueba1.ods")
if resultado:
    print(f"Archivo generado: {resultado}")
