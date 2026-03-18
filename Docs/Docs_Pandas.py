import os

try:
    import pandas as pd
except ModuleNotFoundError:
    pd = None


def crear_df_ejemplo():
    return pd.DataFrame(
        {
            "Edad": [25, 30, 22, 35],
            "Nombre": ["Ana", "Juan", "Luis", "Marta"],
            "Sueldo": [2500, 3100, 2000, 4000],
        }
    )


def cargar_datos(csv_path="archivo.csv", excel_path="archivo.xlsx"):
    if os.path.exists(csv_path):
        print(f"Cargando CSV: {csv_path}")
        return pd.read_csv(csv_path)
    if os.path.exists(excel_path):
        print(f"Cargando Excel: {excel_path}")
        return pd.read_excel(excel_path)

    print("No se encontraron archivos externos; se usa DataFrame de ejemplo.")
    return crear_df_ejemplo()


def demo_pandas(df):
    print("\n1) Inspeccion rapida")
    print(df.head(3))
    print(df.tail(3))
    print(df.info())
    print("shape:", df.shape)
    print("columnas:", df.columns.tolist())
    print("nombres unicos:", df["Nombre"].unique())

    print("\n2) Estadistica descriptiva")
    print(df.describe(include="all"))
    print("media edad:", df["Edad"].mean())
    print("mediana sueldo:", df["Sueldo"].median())
    print("moda nombre:", df["Nombre"].mode().tolist())
    print("conteo nombre:\n", df["Nombre"].value_counts())

    print("\n3) Seleccion y filtrado")
    print(df["Nombre"])
    print(df[["Nombre", "Sueldo"]])
    print(df.iloc[0:3])
    print(df[df["Edad"] > 30])
    print(df[(df["Edad"] > 20) & (df["Sueldo"] < 3000)])

    print("\n4) Limpieza de datos")
    print("nulos por columna:\n", df.isnull().sum())
    print(df.dropna())
    print(df.fillna(0))
    print(df.replace("Ana", "Ana Maria"))
    print(df.rename(columns={"Edad": "Anios"}))
    print(df.drop("Sueldo", axis=1))

    print("\n5) Agrupacion y agregacion")
    print(df.groupby("Nombre")["Sueldo"].mean())


if __name__ == "__main__":
    if pd is None:
        print(
            "Pandas no esta instalado. Instala dependencias con: "
            "pip install pandas openpyxl"
        )
    else:
        data = cargar_datos()
        demo_pandas(data)
