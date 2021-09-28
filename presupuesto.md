### Script de PDFs a textos limpios (3..5 días)
- Sobre la conversion desde PDF:
  - Buscar el comando de terminal (o paquete de python) adecuado.
  - Pascual ya ha hecho cosas con la terminal del Mac.
- Sobre la limpieza:
  - Habría que usar expresiones regulares (regex) (Pascual ya ha hecho cosas aquí también).
  - Serían textos de español e inglés (lista de stopwords distintas, etc.)
  - Trabajar aqui con metodologia ágil para iterar y mejorar el script de limpieza poco a poco.
- El script debe funcionar con un PDF o con varios PDFs a la vez
- Generar alerta o warning sobre aquellos PDFs que no se convirtieron o no se limpiaron aduacuadamente (por lo tanto el script debe correr tests de checkeo al final de cada conversión) 

### Etiquetado morfológico (POS tagging) (10 días)
- Parte funadamental porque permiter anotar y sacar mucha información de los textos (anotacón de cada palabra según sea verbo, adjetivo, etc.).
- Lo ideal aquí es hacer uso del probablente etiquetdor morfologico: **Freeling** en Python. Ya que permite varios idiomas y genera analisis muy detallados.
- En caso de fracaso con Freeling o simplemente para complementar a Freeling, se probarán otros POS taggers como, **Spacy**, **NLTK** o **Stanford Stanza**.
