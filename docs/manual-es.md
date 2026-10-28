# ContestPusher — Manual de usuario (Español)

> **⚠️ Estado de revisión:** Revisado tras las pruebas el [FECHA] por [INDICATIVO]  
> Los elementos marcados con `[PENDIENTE]` o `[VERIFICAR]` deben confirmarse después de las pruebas.

---

## Contenido

1. [Instalación](#instalación)
2. [Iniciar la aplicación](#iniciar-la-aplicación)
3. [Configurar servicios](#configurar-servicios)
   - [LoTW — Logbook of the World](#lotw--logbook-of-the-world)
   - [eQSL.cc](#eqslcc)
   - [QRZ Logbook](#qrz-logbook)
   - [Club Log](#club-log)
   - [HRDLog.net](#hrdlognet)
4. [Subir un registro](#subir-un-registro)
5. [Ver el historial](#ver-el-historial)
6. [Preguntas frecuentes](#preguntas-frecuentes)

---

## Instalación

### Requisitos

| Software | Versión | Descargar |
|---|---|---|
| Python | 3.9 o superior | [python.org/downloads](https://www.python.org/downloads/) |
| TQSL | Última versión | [arrl.org/tqsl-download](https://www.arrl.org/tqsl-download) *(solo para LoTW)* |

> **Windows:** Durante la instalación de Python, marca la opción **"Add Python to PATH"**.

### Extraer los archivos

Extrae el archivo de ContestPusher en la carpeta que prefieras, por ejemplo `C:\ContestPusher\`.

---

## Iniciar la aplicación

**Windows:**
```
Doble clic en start.bat
```

**Linux / macOS:**
```bash
chmod +x start.sh
./start.sh
```

La primera vez se instalan las dependencias automáticamente. Luego abre tu navegador en:

```
http://localhost:8090
```

> El puerto se puede cambiar con la variable de entorno `CONTESTPUSHER_PORT`.

---

## Configurar servicios

Ve a **Servicios** (⚙️ en la barra lateral).  
Haz clic en un servicio para desplegar su configuración. Actívalo con el interruptor, rellena los datos y haz clic en **Guardar**.

Las contraseñas y claves API se almacenan **cifradas localmente** en tu equipo (Fernet AES-128).

---

### LoTW — Logbook of the World

**¿Qué es?**  
LoTW es el sistema oficial de QSL digital de la ARRL. Las confirmaciones se firman criptográficamente con un certificado vinculado a tu indicativo.

**Requisitos:**
- TQSL instalado y configurado con el certificado de tu indicativo
- Cuenta activa en LoTW en [lotw.arrl.org](https://lotw.arrl.org)

**Configuración en ContestPusher:**

| Campo | Descripción |
|---|---|
| **Ruta de TQSL** | Ruta completa al ejecutable de TQSL. Por defecto: `C:\Program Files\TQSL\tqsl.exe` (Windows) o `/usr/bin/tqsl` (Linux). `[VERIFICAR TRAS PRUEBA]` |
| **Indicativo** | Tu indicativo, p. ej. `EA1ABC`. Debe coincidir con el certificado instalado en TQSL. |
| **Contraseña** | Tu contraseña de LoTW / TQSL. Se almacena cifrada. |

**Cómo obtener un certificado LoTW:**

1. Crea una cuenta en [lotw.arrl.org](https://lotw.arrl.org)
2. Abre TQSL y accede al **Station Location Wizard**
3. Solicita un certificado para tu indicativo
4. La ARRL envía un correo de confirmación con un archivo `.tq6`
5. Abre ese archivo en TQSL — el certificado quedará instalado

> Las subidas a LoTW pueden tardar **30 segundos o más**, ya que TQSL primero firma el registro y luego lo sube.

---

### eQSL.cc

**¿Qué es?**  
eQSL.cc es un sistema electrónico de QSL gratuito, popular por sus confirmaciones rápidas.

**Crear una cuenta:**  
Regístrate gratuitamente en [eqsl.cc/Member.cfm](https://www.eqsl.cc/Member.cfm)

**Configuración en ContestPusher:**

| Campo | Descripción |
|---|---|
| **Nombre de usuario** | Tu nombre de usuario en eQSL.cc (tu indicativo) |
| **Contraseña** | Tu contraseña de eQSL.cc |

> eQSL **no** necesita clave API. Solo se requieren el nombre de usuario y la contraseña.

---

### QRZ Logbook

**¿Qué es?**  
El libro de registro en línea de QRZ.com, con confirmación automática de QSL para otros usuarios de QRZ.

**Requisitos:**  
Una suscripción de pago **QRZ XML Subscription**. Sin suscripción de pago la clave API no funciona.  
Suscríbete en [qrz.com/shop](https://www.qrz.com/shop).

**Dónde encontrar la clave API:**

1. Inicia sesión en [qrz.com](https://www.qrz.com)
2. Ve a **Logbook** → **Settings** (icono de engranaje)
3. Copia el valor que aparece junto a **API Key**

**Configuración en ContestPusher:**

| Campo | Descripción |
|---|---|
| **Clave API** | La clave de la configuración de tu libro de registro de QRZ (cadena alfanumérica larga) |

---

### Club Log

**¿Qué es?**  
Club Log es un servicio gratuito para estadísticas, análisis DXCC y publicación de registros de expediciones.

**Crear una cuenta:**  
Regístrate gratuitamente en [clublog.org](https://clublog.org)

**Configuración en ContestPusher:**

| Campo | Descripción |
|---|---|
| **Correo electrónico** | El correo electrónico de tu cuenta de Club Log |
| **Contraseña** | Tu contraseña de Club Log |
| **Indicativo** | Tu indicativo tal como está registrado en Club Log |
| **Application key** | `[VERIFICAR]` Puede ser necesaria — se encuentra en tu perfil de Club Log en Settings → API |

> Club Log acepta archivos ADIF directamente mediante HTTP POST. No se necesita suscripción de API aparte.

---

### HRDLog.net

**¿Qué es?**  
HRDLog.net es un libro de registro en línea y una comunidad para radioaficionados.

**Crear una cuenta:**  
Regístrate gratuitamente en [hrdlog.net](https://www.hrdlog.net)

**Dónde encontrar la clave API (Upload Code):**

1. Inicia sesión en [hrdlog.net](https://www.hrdlog.net)
2. Ve a **My Account** → **Upload Code** (o **API**)
3. Copia el Upload Code — es una cadena alfanumérica corta

**Configuración en ContestPusher:**

| Campo | Descripción |
|---|---|
| **Indicativo** | Tu indicativo |
| **Upload Code** | El Upload Code / clave API de tu cuenta de HRDLog.net |

---

## Subir un registro

1. Ve a **Subir** (📤 en la barra lateral)
2. Arrastra tu archivo `.adi` o `.adif` a la zona de carga, o haz clic para explorar
3. Haz clic en **Enviar a todos los servicios**
4. ContestPusher sube en paralelo a todos los servicios activados
5. Cada servicio muestra ✅ (exitoso) o ❌ (fallido) con un mensaje

> Asegúrate de que todos los servicios deseados estén activados antes de subir.

---

## Ver el historial

Ve al **Historial** (📋) para ver todas las subidas anteriores con fecha, nombre de archivo, número de QSOs y el resultado por servicio.

---

## Preguntas frecuentes

**La subida a LoTW tarda mucho o muestra un error.**  
Comprueba que TQSL está correctamente configurado con un certificado de indicativo válido. Abre TQSL manualmente y prueba una subida. Verifica también la ruta de TQSL en la configuración de ContestPusher.

**Mi contraseña ha desaparecido tras reiniciar.**  
`[VERIFICAR TRAS PRUEBA]` Las contraseñas se guardan cifradas en `contestpusher.db` y deberían conservarse. Si desaparecen, es posible que se haya eliminado el archivo `.key`.

**¿Puedo usar ContestPusher sin internet?**  
No — cada servicio requiere conexión a internet para subir el registro.

**¿Puedo subir solo una parte de los QSOs?**  
Simplemente sube un archivo ADIF que contenga solo los QSOs que deseas. ContestPusher sube todo lo que hay en el archivo.

**La aplicación no arranca.**  
- Comprueba que Python 3.9+ está instalado y en el PATH  
- Comprueba que el puerto 8090 no está ya en uso por otra aplicación  
- Consulta el mensaje de error en la ventana de terminal

---

*ContestPusher es de código abierto (MIT). Código fuente: [github.com/pe5jw/ContestPusher](https://github.com/pe5jw/ContestPusher)*  
*73*
