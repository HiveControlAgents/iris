# Revisão: Why Owls Fly in Total Silence

**Nota: 5,5 / 10**

O visual está limpo e a parte técnica está correta (1080x1920, 17,7 MB). Mas a narração reprova na transcrição, a fala corre rápido demais no começo e um vídeo sobre voo silencioso nunca mostra a coruja voando.

## Refazer

- **Cena 4 (11,6 a 15,1 s):** a pena é cinza com pintas laranja, de outra espécie, e só tem penugem na base. A narração fala da borda traseira franjada, que não aparece. O brilho também deriva 20% dentro da cena. *Ajuste:* rêmige de suindara buff-dourada com franja macia ao longo de toda a borda traseira, luz constante.

## Problemas

| s | cena | tipo | gravidade | o que acontece | origem |
|---|---|---|---|---|---|
| 0,0 | 1 a 7 | narração | alta | Whisper ouviu português em todo o vídeo ("um alvo pode voar por perto"). A estrutura bate com o roteiro, então provavelmente é idioma ou sotaque da voz, ou o transcritor sem idioma fixo. Confirmar retranscrevendo com `en`. | pipeline |
| 0,0 | 1 a 4 | ritmo | média | 3,2 a 4,0 palavras/s (alvo de 2,3 a 3,0) | pipeline |
| 0,0 | 1 | ritmo | média | O gancho diz "can fly right past you" com a coruja parada no galho | pipeline |
| 20,2 | 6 | visual | média | Sem voo, sem rato e quase sem névoa. As cenas 1, 2, 6 e 7 repetem a mesma pose pousada | pipeline |
| 11,6 | 4 | visual | média | Pena errada, franja no lugar errado, brilho +20% | sorteio |
| 15,1 | 5 | visual | baixa | A pena e a coruja mudam de aparência entre as cenas | pipeline |
| 17,5 | 5 | legenda | baixa | Blocos "WHICH SWALLOWS THE TINY" e "COMING. THAT IS WHY" | pipeline |
| 0,0 | — | áudio | baixa | -15,3 LUFS (alvo -14 ±1) | pipeline |

## Pipeline

1. Fixar a voz em inglês nativo e passar `language='en'` ao Whisper da inspeção.
2. Limitar o roteiro a 3,0 palavras/s por cena.
3. Em tema de ação animal, mostrar a ação (voo planado em câmera lenta) no gancho.
4. Quebrar as legendas na pontuação e no sintagma.
5. Normalizar a mixagem final para -14 LUFS.
