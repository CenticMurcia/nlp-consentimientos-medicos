# Proyecto NLP

## Introducción

Determinacion de la legibilidad y entendibilidad de consentimientos médicos en español y catalán.

Proyecto en colaboración con la UMU (Pascual, pascualf@um.es) y Anabel e Isabel (de la univesidad Jaume I de Castellón).

## Pasos del proyecto

## Parte 1 (analisis de los consentimientos disponibles)

1. Recopilación de los textos (Hecho por Pascual)
   - De los PDFs se extraerán los textos `.txt`
   - Serán 100 textos en español y 50 en catalán.
2. Etiquetado morfológico (POS tagging)
   - Usando [Freeling](http://nlp.lsi.upc.edu/freeling/node/1) porque sigue el estándard de [EAGLES](http://blade10.cs.upc.edu/freeling-old/doc/tagsets/tagset-es.html)
3. Generar Features de los textos. Por ejemplo:
   - Longitud del texto (numero de palabras, letras, etc).
   - Proporción de sustantivos, verbos, adverbios
   - Proporción de palabras médicas
   - Proporción de palabras legales
   - Métrica Fernandez Huertas
   - Frecuencia de uso (las palabras son comunes o no).
   - Media de silabas o letras de todas las palabras.
4. Aplicar ML
   - Principalmente se hará Aprendizaje No Supervisado para analizar.
     - Analisis de componentes (PCA)
     - LDA creo que es una buena técnica a usar también.
     - Clustering
   - Si nos animamos a etiquetar el dataset (decir su entendibilidad) o Pascual nos pasa las etiquetas puestas por los *Focus groups*, podremos aplicar Aprendizaje Supervisado.
5. Mostrar conclusiones en forma de gráficas. Tenemos que responeder a la pregunta: ¿Qué factores determinan la entendibilidad y legibilidad del constentimeto?
   - Es la longitud del texto?
   - Es la cantidad de vocabulario médico?
   - Es la cantidad de vocabulario legal?
   - Es la cantidad de palabras poco comunes?
   - Es el formato del consentimiento (experesado en una frase o en la mitad del texto)?

## Parte 2: Generar nuestras plantillas de consentimientos

Dimensiones:

Practica clinica

- Nivel del paciente (infantil, adulto nivel bajo, adulto nivel medio)
- Tipo de intervenccion (quirurjica, invasiva, tratamiento, etc)
- Especialidad médica
- Porcentaje de posibles consecuencias (inofensivo, medio, peligroso)
- Nivel de empatia hacia el paciente

## Trabajos relacionados

- <https://www.kaggle.com/c/commonlitreadabilityprize>
