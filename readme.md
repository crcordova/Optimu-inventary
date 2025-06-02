# Gestión de Demanda e Inventarios en Retail

## Objetivo del Proyecto

Desarrollar un sistema de forecasting de demanda y reposición de inventario para una cadena de retail que comercializa bebidas (Gaseosas, Jugos, Aguas) en 5 tiendas. El objetivo es optimizar la disponibilidad de productos, minimizar quiebres de stock y reducir costos de inventario.  

## Parte I: Predicción de Demanda

Se desarrolló un pipeline de forecasting a nivel SKU-tienda utilizando:

   - Modelos base: XGBoost
   - Atributos producto: `['region', 'tienda', 'familia', 'precio_unitario','temperatura', 'indice_economico', 'año', 'mes', 'dia', 'dia_semana', 'semana']`  


## Parte II: Optimización de Inventario

### Problema  

Formular un modelo de programación lineal entera, que decida semanalmente el inventario de cada producto en cada tienda 

### Función objetivo

Minimizar el costo de inventarios dado por el sobre stock y por el quiebre de stock

### Variable de desicion

Cantidad de producto `i` en tienda `j`

### Restricciones:

    Capacidad limitada por tienda

    Capacidad de producción limitada a nivel nacional

    Demanda minima

    Costos:

        Inventarios (costo de mantener inventario)

        Quiebre de Stock (ventas perdidas)


## Parte III: Reflexión

### ✅ Lo que funcionó

 - Integración de variables exógenas (temperatura)  

 - Predicción SKU-tienda específica con buena granularidad  

 - Solución de inventario interpretable para operaciones  

### ⚠️ Limitaciones

 - Calidad/precisión de predicciones aún perfectible  

 - Algunas suposiciones simplifican la logística real (no se consideran costos de transportes)  

 - Solo considera un rango de tiempo estatico (1 semana)  

### Próximos Pasos

 - Incorporar condiciones de borde (inventario inicial)  

 - Incluir costos por producto más detallados (e.g., margen unitario)  

## Arquitectura Técnica Propuesta

- Consideraría una arquitectura basada en microservicios y un pipeline robusto, 
- primero tener un datalake o warehouse con los diversos datos necesarios (ventas, clima...),
- luego con un orquestador (tipo airflow) consumir la data diariamente y realizar las transformaciones requeridas.
- Nuestro primer microservicio sería el modelo de predicción de la demanda (Forecast), el cual recibe la data y como salida tendríamos el forecast de los productos,
- luego el microservicio de optimización recibirá la data del Forecast con la cual calculará el inventario óptimo de cada tienda, 
- cabe destacar que cada microservicio debe tener su propia DB para almacenar resultados.
- Finalmente tener el microservicio de reporting que consumirá la data de los modelos, el cual permite tomar decisiones estratégicas.
