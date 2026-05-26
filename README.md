# Cruce de Beneficiarios Universo

Aplicación desarrollada en **Streamlit** para realizar cruces de CURPs contra una base de datos de beneficiarios y clasificar los resultados en beneficiarios directos, beneficiarios indirectos y no beneficiarios.

## Descripción

Este proyecto permite cargar un archivo `.txt` con una lista de CURPs y consultar una base de datos **SQL Server** para identificar si las personas se encuentran registradas dentro del universo de beneficiarios.

La aplicación muestra los resultados en tres grupos:

- Beneficiarios directos.
- Beneficiarios indirectos.
- No beneficiarios.

El objetivo es facilitar la validación de universos de personas contra registros institucionales, permitiendo detectar coincidencias y clasificar el tipo de relación con los programas sociales.

## Funcionalidades principales

- Carga de archivo `.txt` con CURPs.
- Lectura de CURPs separados por salto de línea.
- Consulta a base de datos SQL Server.
- Cruce de CURPs contra registros de beneficiarios.
- Identificación de beneficiarios directos.
- Identificación de beneficiarios indirectos.
- Identificación de CURPs no encontrados.
- Visualización de resultados en Streamlit.
- Manejo básico de errores cuando los CURPs tienen formato incorrecto.
- Configuración de conexión mediante archivo `config.yml`.

## Archivos principales

```text
.
├── README.md
├── app.py
├── requirements.txt
├── .gitignore
└── utils
    ├── config.py
    ├── connection.py
    └── data.py
```

## Archivos principales del proyecto

### `app.py`

Aplicación principal de Streamlit.

Permite:

- Mostrar la interfaz del sistema.
- Solicitar al usuario un archivo `.txt`.
- Leer CURPs desde el archivo cargado.
- Enviar la lista de CURPs a la función de consulta SQL.
- Mostrar beneficiarios directos.
- Mostrar beneficiarios indirectos.
- Mostrar CURPs no encontrados.

El archivo cargado debe contener un CURP por línea.

Ejemplo:

```text
CURPEJEMPLO1
CURPEJEMPLO2
CURPEJEMPLO3
```

### `utils/config.py`

Contiene la clase `Config`, encargada de leer el archivo de configuración `config.yml`.

Por defecto, el proyecto busca el archivo:

```text
config.yml
```

en la raíz del repositorio.

### `utils/connection.py`

Contiene la función de conexión a SQL Server usando SQLAlchemy.

La conexión se construye a partir de las credenciales definidas en `config.yml`.

### `utils/data.py`

Contiene la lógica principal de consulta.

La función `read_data_from_sql(table, curp_list)` recibe:

- El nombre de la sección de configuración.
- Una lista de CURPs.

Después construye una consulta SQL para buscar beneficiarios relacionados con viviendas beneficiadas.

También contiene funciones auxiliares para generar descargas de archivos CSV.

### `requirements.txt`

Archivo con las dependencias necesarias para ejecutar el proyecto.

Incluye:

```text
streamlit
sqlalchemy
pandas
pyyaml
pyodbc
```

## Requisitos

Para ejecutar el proyecto se recomienda contar con Python 3.8 o superior.

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

O manualmente:

```bash
pip install streamlit sqlalchemy pandas pyyaml pyodbc
```

También es necesario contar con un driver compatible para conectarse a SQL Server, por ejemplo:

```text
ODBC Driver 17 for SQL Server
```

o

```text
ODBC Driver 18 for SQL Server
```

## Configuración requerida

Para que el proyecto funcione correctamente, es necesario crear un archivo llamado:

```text
config.yml
```

en la raíz del repositorio.

Este archivo debe contener las credenciales de conexión a SQL Server.

## Formato requerido de `config.yml`

El código espera una sección llamada `ps`, ya que `app.py` llama la función de consulta usando:

```python
read_data_from_sql("ps", curp_list)
```

Por lo tanto, el archivo `config.yml` debe tener el siguiente formato:

```yaml
ps:
  USERNAME: "TU_USUARIO_SQL"
  PASSWORD: "TU_PASSWORD_SQL"
  SERVER: "TU_SERVIDOR_SQL"
  DATABASE: "TU_BASE_DE_DATOS"
  DRIVER: "TU_DRIVER_SQL"
```

## Ejemplo de `config.yml`

```yaml
ps:
  USERNAME: "usuario_sql"
  PASSWORD: "password_sql"
  SERVER: "servidor.database.windows.net"
  DATABASE: "base_datos"
  DRIVER: "ODBC Driver 17 for SQL Server"
```

La conexión se construye internamente con el siguiente formato:

```python
mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}
```

## Ejecución

Para ejecutar la aplicación localmente:

```bash
streamlit run app.py
```

Después de ejecutar el comando, Streamlit abrirá la aplicación en el navegador.

## Uso esperado

1. Crear el archivo `config.yml` con las credenciales de SQL Server.
2. Instalar las dependencias del proyecto.
3. Ejecutar la aplicación con Streamlit.
4. Subir un archivo `.txt` con un CURP por línea.
5. Revisar los resultados generados por la aplicación.
6. Identificar beneficiarios directos, beneficiarios indirectos y CURPs no encontrados.

## Estructura esperada del archivo `.txt`

El archivo debe contener una CURP por línea, sin comas ni caracteres adicionales.

Ejemplo:

```text
ABCD010101HNLXXX09
EFGH020202MNLXXX01
IJKL030303HNLXXX02
```

## Consulta SQL utilizada

El proyecto consulta información de tablas relacionadas con beneficiarios, controles de beneficiario y viviendas.

Las tablas referenciadas en el código son:

```text
DatosBeneficiario
BeneficiarioControl
DatosVivienda
```

La consulta identifica viviendas con beneficiarios directos y luego busca si los CURPs cargados pertenecen a dichas viviendas.

## Campos consultados

La consulta devuelve información como:

```text
CURP
IDVivienda
Nombre
Paterno
Materno
Celular
Municipio
Colonia
Localidad
CodigoPostal
TelPart
TelMovil
TelRecado
FechaAgregaVivienda
Observaciones
IDEstatusBeneficiario
FechaAgregaBeneficiario
FechaActualiza
IDPrograma
FechaAutorizacion
FechaCancelacion
```

## Clasificación de resultados

### Beneficiarios directos

Se consideran beneficiarios directos aquellos registros cuyo campo:

```text
IDEstatusBeneficiario
```

es igual a:

```text
4
```

### Beneficiarios indirectos

Se consideran beneficiarios indirectos aquellos registros cuyo campo:

```text
IDEstatusBeneficiario
```

es diferente de:

```text
4
```

### No beneficiarios

Se consideran no beneficiarios aquellos CURPs del archivo cargado que no aparecen en los resultados obtenidos desde SQL Server.

## Posibles mejoras

- Agregar validación formal de CURP.
- Permitir descarga de resultados en CSV o Excel desde la interfaz.
- Mostrar métricas resumen, como total de CURPs cargados, encontrados y no encontrados.
- Separar resultados en tablas más claras.
- Agregar filtros por municipio, programa o estatus.
- Mejorar el manejo de errores cuando falla la conexión SQL.
- Cambiar la consulta SQL a una consulta parametrizada.
- Normalizar CURPs eliminando espacios y convirtiendo a mayúsculas.
- Agregar pruebas unitarias para lectura de archivos y clasificación de resultados.
- Agregar archivo `config.example.yml`.

## Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- SQLAlchemy
- SQL Server
- PyODBC
- YAML

## Objetivo del proyecto

Facilitar el cruce de universos de CURPs contra registros institucionales de beneficiarios, permitiendo identificar de manera rápida qué personas son beneficiarias directas, indirectas o no aparecen en la base consultada.

## Estado del proyecto

Proyecto en desarrollo para uso interno en tareas de consulta, validación y cruce de beneficiarios.