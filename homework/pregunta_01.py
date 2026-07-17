"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.

    """
    with open("files/input/clusters_report.txt", encoding="utf-8") as file:
        lineas = file.readlines()

    registros = []
    cluster_actual = None

    for linea in lineas:
        linea = linea.strip()

        if linea == "":
            # linea vacia: separa un cluster del siguiente, no hace nada
            continue

        if linea[0].isdigit():
            # linea nueva de cluster: "1  105  15,9 %  maximum power..."
            partes = linea.split(maxsplit=3)
            numero_cluster = int(partes[0])
            cantidad = int(partes[1])
            # partes[2] es "15,9" y partes[3] arranca con "%  maximum..."
            porcentaje_texto, resto = partes[2], partes[3]
            porcentaje = float(porcentaje_texto.replace(",", "."))
            # quitamos el "%" que quedo al inicio del resto
            resto = resto.replace("%", "", 1).strip()

            cluster_actual = {
                "cluster": numero_cluster,
                "cantidad_de_palabras_clave": cantidad,
                "porcentaje_de_palabras_clave": porcentaje,
                "principales_palabras_clave": resto,
            }
            registros.append(cluster_actual)

        elif linea == "-" * len(linea):
            # linea de puros guiones (separador de encabezado): se ignora
            continue

        elif linea in ("Cluster", "palabras clave  palabras clave") or (
            cluster_actual is None
        ):
            # lineas de encabezado antes del primer cluster: se ignoran
            continue

        else:
            # linea de continuacion de palabras clave del cluster actual
            cluster_actual["principales_palabras_clave"] += " " + linea

    df = pd.DataFrame(registros)

    # limpieza final de la columna de palabras clave
    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .str.rstrip(".")
        .str.split()
        .str.join(" ")
    )
    # colapsar espacios alrededor de comas y unificar separador ", "
    df["principales_palabras_clave"] = df["principales_palabras_clave"].apply(
        lambda texto: ", ".join(palabra.strip() for palabra in texto.split(","))
    )

    return df