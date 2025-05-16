import pandas as pd
from cassandra.cluster import Cluster

# Leer y limpiar el Excel
df = pd.read_excel("postulaciones.xlsx")
df.columns = df.columns.str.strip().str.upper()

# Conexión a Cassandra
cluster = Cluster(["127.0.0.1"], port=7001)
session = cluster.connect("universia")

# Funciones auxiliares
def safe_int(val): 
    try: return int(val)
    except: return 0

def safe_float(val): 
    try: return float(val)
    except: return 0.0

def clean_str(val): 
    if isinstance(val, str):
        return val.replace('%', '').strip()
    return val

for _, row in df.iterrows():
    try:
        cedula = safe_int(row["CEDULA"])
        periodo = safe_int(row["PERIODO"])
        sexo = clean_str(row["SEXO"])
        preferencia = safe_int(row["PREFERENCIA"])
        carrera = clean_str(row["CARRERA"])
        facultad = clean_str(row["FACULTAD"])
        puntaje = safe_int(row["PUNTAJE"])
        grupo = clean_str(row["GRUPO_DEPEN"])
        region = clean_str(row["REGION"])
        lat = safe_float(row["LATITUD"])
        lon = safe_float(row["LONGITUD"])
        ptje_nem = safe_int(row["PTJE_NEM"])
        psu_promlm = safe_int(row["PSU_PROMLM"])
        pace = clean_str(row["PACE"]) if pd.notna(row["PACE"]) else "Blanco"
        gratuidad = clean_str(row["GRATUIDAD"]) if pd.notna(row["GRATUIDAD"]) else "NO"
        matriculado = clean_str(row["MATRICULADO"])

        # Insertar en las 3 tablas sin filtro
        session.execute(
            "INSERT INTO medicina_ordenada_por_periodo (carrera, periodo, cedula, facultad, gratuidad, grupo_depen, latitud, longitud, pace, preferencia, psu_promlm, ptje_nem, puntaje, region, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (carrera, periodo, cedula, facultad, gratuidad, grupo, lat, lon, pace, preferencia, psu_promlm, ptje_nem, puntaje, region, sexo)
        )

        session.execute(
            "INSERT INTO informatica_maule_ordenada (region, carrera, periodo, cedula, facultad, gratuidad, grupo_depen, latitud, longitud, pace, preferencia, psu_promlm, ptje_nem, puntaje, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (region, carrera, periodo, cedula, facultad, gratuidad, grupo, lat, lon, pace, preferencia, psu_promlm, ptje_nem, puntaje, sexo)
        )

        session.execute(
            "INSERT INTO salud_ordenada_por_puntaje (facultad, puntaje, cedula, carrera, gratuidad, grupo_depen, latitud, longitud, pace, periodo, preferencia, psu_promlm, ptje_nem, region, sexo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (facultad, puntaje, cedula, carrera, gratuidad, grupo, lat, lon, pace, periodo, preferencia, psu_promlm, ptje_nem, region, sexo)
        )

    except Exception as e:
        print(f"❌ Error con cédula {row.get('CEDULA', '???')}: {e}")

print("✅ Carga completada.")
