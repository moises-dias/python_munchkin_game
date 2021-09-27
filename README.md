# Munchkin Online
## Boardgame online programado em Python.

### Descrição:
Munchkin Online é um tabuleiro contendo as cartas do jogo munchkin que permite a até 10 jogadores jogarem o cardgame de forma online ou local. O projeto foi feito com a intenção de simular da melhor forma a experiência do jogo físico. No estado atual, o projeto já permite que partidas sejam realizadas normalmente, como pode ser visto no vídeo abaixo, mas possui muitas melhorias que serão desenvolvidas futuramente, como inclusão de registros (logs) de ações de cada jogador, redimensionamento das áreas e alerta de jogadores com mais de cinco cartas na mão. 

### Clique na imagem para visualizar um vídeo de alguns minutos de jogo:
[![Munchkin Online](https://img.youtube.com/vi/AXy6kqnnp74/0.jpg)](https://www.youtube.com/watch?v=AXy6kqnnp74 "Munchkin Online Gameplay")

### O jogo possui 6 áreas distintas:
* Table: na parte superior direita, é o equivalente a mesa, onde os jogadores batalham e jogam cartas para afetar uns aos outros, possui também dois contadores, para contabilizar o bônus dos monstros e jogadores durante uma batalha, bastando colocar o cursor em cima de um desses dois contadores e digitar o valor ou apagar um valor de uma batalha passada.
* Players: na parte superior esquerda, mostra o nome dos jogadores conectados, assim como seu nível, numero de cartas na mão e numero de cartas equipadas.
* Equipments: abaixo da área Players, é uma área exclusiva de cada jogador, mas que pode ser visualizada por todos os jogadores, é referente aos equipamentos e maldições equipados pelo jogador. Por padrão o jogador visualiza seus próprios equipamentos, mas pode visualizar os dos outros jogadores ao passar o mouse por cima do nome dos jogadores na área Players.
* Hand: é uma área exclusiva de cada jogador onde apenas o jogador consegue visualizar, é referente as cartas que o jogador possui na mão.
* Deck: essa área possui 4 pilhas: duas pilhas com a face para baixo referente aos baralhos de porta e tesouro, respectivamente e duas pilhas de descarte de porta e tesouro, respectivamente. Sendo que cada uma possui um número do total de cartas na respectiva pilha.
* Logs: essa área seria utilizada para exibir os registros das ultimas ações realizadas (movimentações de cartas, descarte, alteração de níveis) como isso é mais difícil de acompanhar de forma online, mas na versão atual possui um simulador de um dado, onde ao ser clicado exibe um número de 1 a 6 aleatóriamente.

### Comandos:
| Comando                      | Acão                                                     |
| -----------                  |:------:                                                  |
| Botão esquerdo mouse         | segura uma carta*                                        |
| Soltar botão esquerdo mouse  | solta uma carta**                                        |
| Botão direito mouse          | vira a face de uma carta*                                |
| D                            | Descartar uma carta*                                     |
| V                            | Exibe a carta com um tamanho maior*                      |
| Números                      | Altera o nível do próprio jogador***                     |
| reset12345                   | Retorna todas as cartas do jogo às pilhas do baralho     |
| reset54321                   | Retorna as cartas do descarte às pilhas do baralho       |

 
 \* o cursor do mouse deve estar em cima da carta para ter efeito  
 \** o jogador deve estar segurando uma carta para a ação ter efeito  
 \*** o cursor do mouse deve estar na área Players

### Instruções para execução do jogo:
#### LOCALMENTE
**Iniciando servidor**:  
Descomentar as linhas 12 e 13 no arquivo server.py, colocando o ip da sua rede na variavel server (linha 12) e o numero da porta na variavel port (linha 13, por padrão eu utilizei 5555) e então executar o arquivo server.py utilizando python 3.

**Iniciando o cliente**:  
No arquivo conf.txt, colocar o seu nome na primeira linha, o ip da sua rede na segunda linha e a porta na terceira linha (ip e porta devem ser os mesmos do arquivo server.py)
o cliente pode então ser iniciado tanto pelo código (client.py) quanto pelo executável (client.exe) gerado pelo pyinstaller.

#### ONLINE
**Iniciando o servidor**:  
Para jogar online, o servidor deve ser hospedado em alguma nuvem, eu vou aqui explicar como realizar essa hospedagem no Google Cloud Platform.
* No painel do GCP, acesse a ferramenta Compute Engine e dentro dela clique em create instance.
* Na pagina que abrir, selecione um nome para a VM, no campo região selecione o mais próximo da sua localidade, e em machine type, a opção mais básica já é suficiente para essa aplicação, após a confirmação desses itens clique em create.
* Anote o número do External IP que aparece na máquina que foi criada.
* Clique em SSH na máquina criada, no terminal que se abrir, execute o comando ```nano server.py``` e insira o código do arquivo server.py disponível nesse repositório.
* Salve o arquivo server.py criado na VM, e execute o mesmo com o comando ```python3 server.py```  

Caso preferir, nesse [link](https://www.youtube.com/watch?v=RFPlXmgKCtk) tem um vídeo mostrando o processo descrito acima. 

**Iniciando o cliente**:  
No arquivo conf.txt, colocar o seu nome na primeira linha, o External IP da VM segunda linha e a porta 3389 na terceira linha.
o cliente pode então ser iniciado tanto pelo código (client.py) quanto pelo executável (client.exe) gerado pelo pyinstaller.

### Agradecimentos
Os agradecimentos vão principalmente para o Steve Jackson, criador do jogo munchkin.  
E para o Tim Ruscica, do site TechWithTim, pelo [tutorial de jogo online usando python](https://www.techwithtim.net/tutorials/python-online-game-tutorial/) que foi o ponto de partida para esse projeto.
