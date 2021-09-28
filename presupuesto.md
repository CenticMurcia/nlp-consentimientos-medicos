### Script de PDFs a textos limpios (3..5 días)
- Sobre la conversión desde PDF:
  - Buscar el comando de terminal (o paquete de python) adecuado.
  - Pascual ya ha hecho cosas con la terminal del Mac.
- Sobre la limpieza:
  - Habría que usar expresiones regulares (regex) (Pascual ya ha hecho cosas aquí también).
  - Serían textos de español e inglés (lista de stopwords distintas, etc.)
  - Determinar estrategia para el trato de las tablas y listas que aparecen en el PDF.
  - Trabajar aqui con metodologia ágil para iterar y mejorar el script de limpieza poco a poco.
- El script debe funcionar con un PDF o con varios PDFs a la vez
- Generar alerta o warning sobre aquellos PDFs que no se convirtieron o no se limpiaron aduacuadamente (por lo tanto el script debe correr tests de checkeo al final de cada conversión) 

### Etiquetado morfológico (POS tagging) (10 días)
- Parte funadamental porque permiter anotar y sacar mucha información de los textos (anotacón de cada palabra según sea verbo, adjetivo, etc.).
- Lo ideal aquí es hacer uso del probablente etiquetdor morfologico: **Freeling** en Python. Ya que permite varios idiomas y genera analisis muy detallados.
- En caso de fracaso con Freeling o simplemente para complementar a Freeling, se probarán otros POS taggers como, **Spacy**, **NLTK** o **Stanford Stanza**.

### Métricas básicas morfológicas (2 días)
- Implementar metricas desde el etiquetado morfológico anterior.
- Pascual ya tiene bastante trabajado cuales sería las principaels métricas a sacar.
- Ejemplo:
  - Número de verbos totales.
  - Porcentage de número de verbos.
  - Etc.

### Métricas que indican la legibilidad (3 dias)
- Implentar (o encontrar librerias) en Python fórmulas ya establecidas que determinan la legibilidad de un texto.
- Nos darán la lista de metricas a implementar.
- Ejemplo de metricas:
  - Metrica **Flex index** (para textos en inglés)
  - Metrica **Fernandez Huertas** (para textos en español)


### Metricas que hacen uso de datos externos (4..5 días)
- Metricas que cotejan con listas de vocabulario externas para sacar porcentajes.
- Se nos darán las listas de vocabulario o nos dirán como descargarlas.
- Ejemplo de listas de vocalario:
  - Vocabulario médico
  - Vocabulario legal
  - Vocabulario de frecuancia general (palabaras más comunes de un idioma)

### Análisis comparativo entre textos (4 días)
- Comparar textos entre si.
- Hacer reducción dimensional para visualizar todos los textos
- Hacer clustering para encontrar textos similares.
  - Sacar metricas anteriores de **por grupos** de textos, (en lugar de por textos induviduales).

### Generar informe final del script (3 días)
- Generar resultados/informe/report/graficas
- Probablente **Streamlit** sea la mejor herramienta para entregar nuestro script de analisis de texos
- Capacidad de exportar la tabla de metricas que saquemos y las gráficas a Excel

### Formación del uso del script (2 días)
- Días para dar instrucciones del uso del script para ser capaces de analizar varios textos (PDFs) a la vez.

### EXTRA: Machine Learning supervisado (5 días, probablemente no se haga)
- Etiquetado de los datos (la legibilidad de los textos)
- Entrenar modelo de ML




