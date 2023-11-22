import xml

import requests
import urllib3
import xmltodict
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def diaAnterior(date_str):
  # Convert the string to a datetime object
  date_obj = datetime.strptime(date_str, '%Y-%m-%d')

  # Subtract one day
  previous_day = date_obj - timedelta(days=1)

  # Convert back to string in the same format
  previous_day_str = previous_day.strftime('%Y-%m-%d')

  return previous_day_str

# fecha formato 'aaaa-mm-dd
def obtener_cotizaciones(fecha):
  try:
    fechaList = fecha.split("-")
    dia = fechaList[2]
    mes = fechaList[1]
    ano = fechaList[0]

    url_bcu = f"https://www.bcu.gub.uy/_layouts/15/BCU.Cotizaciones/handler/FileHandler.ashx?op=downloadcotizacionesxml&KeyValuePairs={{%22KeyValuePairs%22:{{%22Monedas%22:[{{%22Val%22:%220%22,%22Text%22:%22TODAS%22}}],%22FechaDesde%22:%22{dia}/{mes}/{ano}%22,%22FechaHasta%22:%22{dia}/{mes}/{ano}%22,%22Grupo%22:%221%22}}}}"
    cotizacionesXML = requests.get(url_bcu, verify=False)

    if cotizacionesXML.status_code == 200:
      cotizDic = xmltodict.parse(cotizacionesXML.content)
      cotizaciones = cotizDic.get("datoscotizaciones", {}).get("datoscotizaciones.dato", [])

      salida = {}
      for moneda in cotizaciones:
        if "CodigoISO" not in moneda:
          return obtener_cotizaciones(diaAnterior(fecha))
        salida[moneda.get("CodigoISO", "")] = float(moneda.get("TCC", 0))

      return salida
    else:
      print(f"Error al obtener las cotizaciones. Código de estado: {cotizacionesXML.status_code}")
      return None
  except requests.RequestException as e:
    print(f"Error al realizar la solicitud: {e}")
    return None
  except xml.parsers.expat.ExpatError as xml_error:
    print(f"Error al parsear el XML: {xml_error}")
    return None
  except Exception as ex:
    print(f"Error inesperado: {ex}")
    return None

def obtener_valor_de_cotizacion(moneda):
  cotizaciones = obtener_cotizaciones('2023-11-19')
  valor_cotizacion = cotizaciones.get(moneda)
  return valor_cotizacion

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
  c = obtener_valor_de_cotizacion('ARS')
  print(c)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
