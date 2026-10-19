# Revisão: Por que o rio Paraná sobe e desce sem parar

**Nota: 5,5 / 10**

Imagens bonitas e áudio no padrão (-14,7 LUFS, pico -1,7 dBFS, sem cortes nem silêncios). A nota fica abaixo de 6 por causa de erros de narração. O roteiro também tem um erro geográfico, e as legendas juntam frases diferentes.

## Cenas a refazer

| Cena | Motivo | Ajuste |
|---|---|---|
| 4 | "gera" sai embolado (~22 s, ouvido como "aleira o que e re"); a frase sobre Itaipu fica incompreensível | Gerar de novo a narração com outra semente e conferir se "gera energia" sai limpo |
| 5 | ~30,0 s: surgem manchas cor de ferrugem no leito e o brilho sobe ~30% dentro da cena | Pedir "consistent lighting, static riverbed, no new objects appearing" e água rasa e clara |

## Problemas

- **Alta, narração, 8 s e 29 s (cenas 2 e 5):** "nas nascentes" vira "nascentes" nas duas vezes. A voz funde as sílabas repetidas (pipeline).
- **Alta, narração, 22 s (cena 4):** "gera" embolado (sorteio).
- **Média, roteiro, 5,2 s (cena 2):** o roteiro diz que o Paraná recebe as águas das nascentes da Serra do Mar. As cabeceiras ficam no Planalto Central (rios Grande e Paranaíba).
- **Média, visual, 30,0 s (cena 5):** objetos novos no leito e deriva de brilho.
- **Média, legenda, 16,5 a 18,5 s e 43,0 a 44,5 s:** "COLOSSAL. O RIO SOBE" e "NOVAMENTE. O RIO PARANÁ" juntam duas frases e atravessam o corte.
- **Média, ritmo, cena 4 (8,6 s):** lago quase parado por tempo demais, e pequeno demais para ser Itaipu.
- **Baixa:** a abertura corta em "O RIO PARANÁ NÃO"; a cena 7 é lenta (1,85 palavras/s) e mostra folhas de outono; a cena 3 não mostra rios se encontrando; algumas palavras foram ouvidas com dúvida.

## Pipeline

1. Legendas: quebrar os blocos no ponto final e no corte de cena.
2. Roteiro: evitar palavras vizinhas com a mesma sílaba e checar fatos geográficos.
3. Narração: transcrever cada frase logo depois de gerar e refazer quando divergir do roteiro.
