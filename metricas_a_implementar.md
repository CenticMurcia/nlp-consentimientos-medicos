
## Métricas básicas

- Número de letras en el texto
- Número de silabas en el texto
- Número de palabras en el texto (tokens)
- Número de palabras unicas en el texto (Tipos)
- Número de frases en el texto (oraciones)
- Ratio Tipo/Token (es un numero entre 0 y 1)
- Tiempo (en minutos) estimado de lectura:
  - Para lector Basico (150 tokens por minuto)
  - Para lector Medio  (250 tokens por minuto)
  - Para lector Rápido (350 tokens por minuto)
- Métricas de legibilidad:
  - Indice Fernande Huerta (L)     = 206.84 - (0.6 * num_tokens) - (1.02 * num_frases)
  - Indice de comprensibilidad (C) = 95.2 - (9.7 * num_letras / num_tokens) - (0.35 * num_tokens / num_frases)
  - Índice de perspecuidad (P)     = 206.835 - (62.3 * num_silabas / num_tokens) - (num_tokens / num_frases)
  - Índice mu = (num_tokens / (num_tokens - 1)) * ( letras_por_palabra.mean() / letras_por_palabra.varianza() ) * 100



## Métricas de vocabulario externo

> ### Sacar metricas para:
> 1. Numero absoluto de tokens
> 2. Numero porcentaje de tokens
> 3. Numero absoluto de tokens unicos (tipos)
> 4. Numero porcentaje de tokens unicos (tipos)
> 5. Numero absoluto de lemmas [OCIONAL]
> 6. Numero porcentaje de lemmas [OCIONAL]
> 7. Numero absoluto de lemmas unicos [OCIONAL]
> 8. Numero porcentaje de lemmas unicos [OCIONAL]

- Vocabulario de lenguaje juridico especialiaado
- Vocabulario de lenguaje médico especialidao
- Vocabulario común de banda de frecuencia <1K
- Vocabulario común de banda de frecuencia 1K..5K
- Vocabulario común de banda de frecuencia 5K..10K
- Vocabulario común de banda de frecuencia 10K..15K




## Métricas desde freeling (conteo y porcentajes de etiquetas morfologicas)

> ### Sacar metricas para:
> 1. Conteo de etiquetas_mor entre tokens
> 2. Porcentaje de etiquetas_mor entre tokens
> 3. Conteo de etiquetas_mor entre tokens unicos (tipos)
> 4. Porcentaje de etiquetas_mor entre tokens unicos (tipos)
> 5. Conteo de etiquetas_mor entre palabras que solo aparcen 1 vez (hápax legomena)
> 6. Porcentaje de etiquetas_mor entre palabras que solo aparcen 1 vez (hápax legomena)

- N: Sutantivos (1_tipo, 4_class)
  - NC: Comun
  - NP: Propio
  - N___S: Persona
  - N___G: Localización
  - N___O: Organización
  - N___V: Otras
- A: Adjetivos
  - AO: Ordinal
  - AQ: Calificativo
  - AP: Posesivo
- C: Conjunciones
  - CC: Coordinativas
  - CS: Soborinadas
- R: Advervios
  - RN: Negativo
  - RG: General
- V: Verbos (1_tipe, 2_mood, 3_tense, 2_moodX3_tense)
- D: Determinantes
  - DA: Articulo
  - DD: Demostrativo
  - DI: Indefinido
  - DP: Posesivo
  - DT: Interrogativo
  - DE: Exclamativo
- P: Pronombres
  - Pronombres de 1a persona
  - Pronombres de 2a persona
  - Pronombres de 3a persona