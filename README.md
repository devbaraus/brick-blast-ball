# Brick Blast Ball (Réplica)

Este repositório contém o projeto de uma réplica do jogo **Brick Blast Ball**, desenvolvido como atividade prática para a disciplina de **Laboratório de Programação** do 1º período do curso de **Bacharelado em Ciência da Computação** do **Instituto Federal de Goiás (IFG) - Câmpus Anápolis**.

---

## 📌 Contexto Acadêmico

Como sugerido no [Projeto Pedagógico do Curso (PPC) de Ciência da Computação do IFG](https://www.ifg.edu.br/attachments/article/1042/PPC_CienciaComputacao.pdf), a ferramenta **AppGameKit** é adotada logo no primeiro período na disciplina de **Laboratório de Programação**. O objetivo dessa abordagem lúdica é estimular e desenvolver:
- **Lógica de programação** de forma visual e interativa.
- **Competências matemáticas e geométricas** (vetores, colisões, reflexão de ângulos).
- **Resolução de problemas complexos** por meio da estruturação e arquitetura de um jogo completo desde o início da graduação.

---

## 🎮 O Jogo: Brick Blast Ball

O jogo é um clássico de estilo *Brick Breaker* / *BBTAN*, onde o jogador deve mirar e lançar esferas para quebrar blocos numerados. Cada bloco possui um número que representa a quantidade de impactos necessários para destruí-lo. À medida que as rodadas avançam, novos blocos surgem com valores maiores, e o jogador pode coletar itens para aumentar o número de esferas disparadas por rodada.

### Funcionalidades
- **Sistema de Mira e Lançamento:** Lançamento de esferas com física de reflexão nas paredes e blocos.
- **Destruição Progressiva de Blocos:** Blocos numerados que exigem múltiplos impactos para serem quebrados.
- **Trilha Sonora Dinâmica:** Efeitos sonoros e músicas ambientais para imersão no jogo.
- **Dificuldade Incremental:** O jogo se torna progressivamente mais desafiador com o aumento do valor dos blocos a cada rodada.

---

## 🎥 Demonstração

Confira abaixo o vídeo de demonstração do funcionamento do jogo (gameplay, colisões e progressão):

<video src="Screencast_20260703_231955.webm" width="100%" controls autoplay loop muted>
  Seu navegador não suporta a exibição de vídeos HTML5. Você pode baixar o vídeo diretamente em [Screencast_20260703_231955.webm](file:///zoomer/brick-blast-ball/Screencast_20260703_231955.webm).
</video>

*(Caso o reprodutor acima não funcione, você pode visualizar ou baixar o vídeo clicando no link a seguir: [Screencast_20260703_231955.webm](file:///zoomer/brick-blast-ball/Screencast_20260703_231955.webm))*

---

## 🛠️ Tecnologias Utilizadas

- **Engine de Desenvolvimento:** [AppGameKit (AGK)](https://www.appgamekit.com/)
- **Linguagem:** AGK BASIC (Tier 1) - *desenvolvido utilizando a linguagem nativa do AppGameKit para controle de lógica de tela, movimentação e colisões física*.
- **Assets de Áudio:** Efeitos e trilhas dinâmicas em formato `.ogg`.
- **Assets de Imagem:** Sprites 2D personalizados para fundos, blocos e projéteis.

---

## 📂 Estrutura do Projeto

O repositório está estruturado com os seguintes componentes principais:
- [Brick Blocks.exe](file:///zoomer/brick-blast-ball/Brick%20Blocks.exe): O executável compilado do jogo, pronto para rodar.
- Imagens de fundo (`back0.jpg` a `back9.png`): Planos de fundo utilizados nas fases do jogo.
- Sprites do jogo (`ball.png`, `gBall.png`, `square.png`): Texturas para as esferas normais/especiais e os blocos.
- Áudios do jogo (`song1.ogg` a `song5.ogg`): Trilha sonora e efeitos sonoros de impacto e feedback.
- [Screencast_20260703_231955.webm](file:///zoomer/brick-blast-ball/Screencast_20260703_231955.webm): Demonstração gravada da gameplay do jogo.

---



## 🚀 Como Executar

Para rodar o jogo localmente no Windows:
1. Clone este repositório ou baixe os arquivos diretamente.
2. Execute o arquivo [Brick Blocks.exe](file:///zoomer/brick-blast-ball/Brick%20Blocks.exe).
3. Use o mouse para mirar e clique para lançar as esferas.

---
*Desenvolvido como parte das atividades acadêmicas de Bacharelado em Ciência da Computação — IFG Câmpus Anápolis.*
