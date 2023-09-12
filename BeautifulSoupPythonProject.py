import requests as req
from bs4 import BeautifulSoup


class Jogo:

  def __init__(self):
    self.link = None
    self.titulo = None
    self.publisher = None
    self.developer = None
    self.rating = None
    self.gameplay = None
    self.visual = None
    self.criticos = None
    self.anoLancamento = None
    self.numJogadores = None
    self.dataLancamento = None
    self.userRatings = None
    self.genero = None
    self.capa = None
    self.perspectiva = None
    self.reviewSite = None


class ListaJogos:

  def __init__(self):
    self.lista = []

  def reiniciaLista(self):
    self.lista = []

  def addJogo(self, jogo):
    self.lista.append(jogo)


def exibe(conteudo):
  print("-----------------")
  if conteudo == None:
    print("Conteúdo não registrado para o jogo.")
  else:
    print(conteudo)
  print("-----------------")


def main():
  listaJogos = ListaJogos()
  escolha = 3

  while escolha != '0':
    pagina = 0
    print("----------------- MENU -----------------")
    escolha = input(
      "Para ver jogos do Nintendo Switch, digite 1.\nPara ver jogos de Xbox One, digite 2.\nPara fechar o programa, digite 0.\n----------------------------------------\n"
    )


    ###################JOGOS NINTENDO SWITCH########################
    if escolha == '1':
      comando = '0'
      while comando != '-1':
        listaJogos.reiniciaLista()
        pagina = str(pagina)  #número da página da lista de jogos
        linkBase = "https://www.nintendolife.com/"
        if pagina == '1':
          pagina = '2'
        response = req.get(linkBase + "nintendo-switch/games/browse?page=" +
                           pagina)
  
        if response.status_code == 200:
          parsed_html = BeautifulSoup(response.text, "html.parser")
          jogos = parsed_html.findAll("div", class_="item-wrap")
          jogoslinks = parsed_html.findAll("a", class_="img scanlines")
          indiceJogoLista = 0
  
          for jogo in jogos:
            newJogo = Jogo()
            tituloJogo = (jogo.text).split("\n")
            tituloJogo = tituloJogo[0].split(" Switch")
            if len(
                tituloJogo
            ) > 1:  #removendo as notícias que também tem div com classe "item-wrap"
              newJogo.titulo = tituloJogo[0]
              newJogo.link = jogoslinks[indiceJogoLista]["href"]
              listaJogos.addJogo(newJogo)
              indiceJogoLista += 1
  
          print("Jogos: ")
          indice = 0
          for jogo in listaJogos.lista:
            print("%d - Título: %s" % (indice, jogo.titulo))
            print("-------------------------")
            indice += 1
          comando = input(
            "Para ver algum jogo, digite seu ID, para ir para a próxima página de jogos, digite next, para sair digite -1\n"
          )
  
          if comando.lower() == 'next':
            pagina = int(pagina)
            pagina += 1
  
          elif comando.isnumeric() and int(comando) < len(listaJogos.lista) and comando != '-1':
            comando = int(comando)
            jogo = listaJogos.lista[comando]
            responseSwitchGame = req.get(linkBase + jogo.link)
            if responseSwitchGame.status_code == 200:
              parsedSwitchGame_html = BeautifulSoup(responseSwitchGame.text,
                                                    "html.parser")
  
              anoLancamento = parsedSwitchGame_html.find("p", class_="year")
              jogo.anoLancamento = anoLancamento.text
  
              avaliacaoUsuarios = parsedSwitchGame_html.find(
                "p", class_="user-ratings")
              avaliacaoUsuarios = (
                avaliacaoUsuarios.text).split("User Ratings: ")
              jogo.userRatings = (avaliacaoUsuarios[1])
  
              reviewSite = parsedSwitchGame_html.findAll("p",
                                                         class_="our-review")
              reviewSite = (reviewSite[0].text).split(":")
              jogo.reviewSite = reviewSite[1].strip()
  
              rating = parsedSwitchGame_html.find("span", class_="score accent")
              jogo.rating = rating.text
  
              capa = parsedSwitchGame_html.find_all("img", {"class": "lazy"})[0]
              capa_content = req.get(capa["data-original"]).content
              jogo.capa = capa_content
  
              overviewJogo1 = (parsedSwitchGame_html.findAll("dt"))
              overviewJogo2 = (parsedSwitchGame_html.findAll("dd"))
              numJogoSwitch = 0
  
              for elemento in overviewJogo1:
                if "Number of Players" in elemento.text:
                  jogo.numJogadores = overviewJogo2[numJogoSwitch].text
  
                elif "Publisher" in elemento.text:
                  jogo.publisher = overviewJogo2[numJogoSwitch].text
  
                elif "Developer" in elemento.text:
                  jogo.developer = overviewJogo2[numJogoSwitch].text
  
                elif "Release Date" in elemento.text:
                  releaseDate = (overviewJogo2[numJogoSwitch].text).split('\n')
                  releaseDate = releaseDate[1].split(',')
                  releaseDate = releaseDate[0]
                  jogo.dataLancamento = releaseDate.strip()
  
                elif "Genre" in elemento.text:
                  jogo.genero = overviewJogo2[numJogoSwitch].text
  
                numJogoSwitch += 1
  
              comandoView = 1
              while comandoView != 0:
  
                comandoView = int(
                  input(
                    """Digite o número correspondente para ver a informação do jogo:
              0- Sair
              1- Publicadora
              2- Desenvolvedora
              3- Nota do jogo
              4- Ano de lançamento
              5- Número de jogadores
              6- Data de lançamento
              7- Quantidade de avaliações de usuários
              8- Gêneros do jogo
              9- Capa do jogo
              10- Avaliação do site sobre o jogo
              """))
                if comandoView == 1:
                  exibe(jogo.publisher)
  
                elif comandoView == 2:
                  exibe(jogo.developer)
                elif comandoView == 3:
                  exibe(jogo.rating)
  
                elif comandoView == 4:
                  exibe(jogo.anoLancamento)
  
                elif comandoView == 5:
                  exibe(jogo.numJogadores)
                  
                elif comandoView == 6:
                  exibe(jogo.dataLancamento)
                  
                elif comandoView == 7:
                  exibe(jogo.userRatings)
  
                elif comandoView == 8:
                  exibe(jogo.genero)
  
                elif comandoView == 9:
                  tituloSemEspaco = (jogo.titulo).replace(" ", "")
                  with open(tituloSemEspaco + '.jpg', 'wb') as file:
                    file.write(capa_content)
                  print("-----------------")
                  print("Capa salva como %s" % (tituloSemEspaco + '.jpg'))
                  print("-----------------")
                elif comandoView == 10:
                  exibe(jogo.reviewSite)
  
                elif comandoView != 0:
                  print("-----------------")
                  print("Comando inválido. Tente novamente.")
                  print("-----------------")
  
            else:
              print("Erro")
              print(responseSwitchGame)

          elif comando != '-1':
            print("Comando inválido.")
  
        else:
          print("Erro.")
          print(response.status_code)


###########################JOGOS XBOX ONE################################
    elif escolha == '2':
      comando = '0'
      while comando != '-1':
        listaJogos.reiniciaLista()
        pagina = str(pagina)  #número da página da lista de jogos


        response = req.get(
          "https://www.mobygames.com/platform/xbox-one/page:%s/" % (pagina))
        
        if response.status_code == 200:
          parsed_html = BeautifulSoup(response.text, "html.parser")
          jogos = parsed_html.findAll("td", class_="text-nowrap")
          indiceJogo = 0

          print("Jogos: ")
          for jogo in jogos:
            newJogo = Jogo()
            if jogo.a != None:
              newJogo.titulo = jogo.a.text
              newJogo.link = jogo.a["href"]
              listaJogos.addJogo(newJogo)
              print("%d - Título: %s" %
                    (indiceJogo, listaJogos.lista[indiceJogo].titulo))
              print("-------------------------")
              indiceJogo += 1
          comando = input(
            "Para ver algum jogo, digite seu ID, para ir para a próxima página de jogos, digite next, para sair digite -1\n"
          )
          if comando.lower() == 'next':
            pagina = int(pagina)
            pagina += 1

          elif comando.isnumeric() and int(comando) < len(listaJogos.lista) and comando != '-1':
            comando = int(comando)
            jogo = listaJogos.lista[comando]
            responseXboxGame = req.get(jogo.link)

            if responseXboxGame.status_code == 200:
              parsedXboxGame_html = BeautifulSoup(responseXboxGame.text,
                                                  "html.parser")
              numInformacaoJogoXbox = 0

              capa = parsedXboxGame_html.find_all("img",
                                                  {"class": "img-box"})[0]
              capa_content = req.get(capa["src"]).content
              jogo.capa = capa_content

              xboxGamesInformacoes1 = parsedXboxGame_html.findAll("dt")
              xboxGamesInformacoes2 = parsedXboxGame_html.findAll("dd")

              for elemento in xboxGamesInformacoes1:
                if 'Released' in elemento.text:
                  dataLancamento = xboxGamesInformacoes2[numInformacaoJogoXbox].text
                  dataLancamento = dataLancamento.split("\n")
                  dataLancamento = dataLancamento[2].strip()
                  jogo.dataLancamento = dataLancamento

                elif 'Publishers' in elemento.text:
                  publishers = xboxGamesInformacoes2[numInformacaoJogoXbox].text
                  publishers = publishers.split("\n")
                  for publisher in publishers:
                    if publisher != '':
                      if jogo.publisher == None:
                        jogo.publisher = publisher
                      else:
                        jogo.publisher += ' / '
                        jogo.publisher += publisher

                elif 'Developers' in elemento.text:
                  developers = xboxGamesInformacoes2[numInformacaoJogoXbox].text
                  developers = developers.split("\n")
                  for developer in developers:
                    if developer != '':
                      if jogo.developer == None:
                        jogo.developer = developer
                      else:
                        jogo.developer += ' / '
                        jogo.developer += developer

                elif 'Moby Score' in elemento.text:
                  rating = (xboxGamesInformacoes2[numInformacaoJogoXbox].text).split(' ')
                  jogo.rating = rating[4]

                elif 'Critics' in elemento.text:
                  criticos = (xboxGamesInformacoes2[numInformacaoJogoXbox].text).split('\n')
                  criticos = criticos[1].strip() + criticos[2].strip()
                  jogo.criticos = criticos

                elif 'Genre' in elemento.text:
                  generos = (xboxGamesInformacoes2[numInformacaoJogoXbox].text).split('\n')
                  for genero in generos:
                    if genero != '':
                      if jogo.genero == None:
                        jogo.genero = genero
                      else:
                        jogo.genero += ' / '
                        jogo.genero += genero

                elif 'Perspective' in elemento.text:
                  perspectivas = (xboxGamesInformacoes2[numInformacaoJogoXbox].text).split('\n')
                  for perspectiva in perspectivas:
                    if perspectiva != '':
                      if jogo.perspectiva == None:
                        jogo.perspectiva = perspectiva
                      else:
                        jogo.perspectiva += ' / '
                        jogo.perspectiva += perspectiva

                elif 'Visual' in elemento.text:
                  visuais = (xboxGamesInformacoes2[numInformacaoJogoXbox].text).split('\n')
                  for visual in visuais:
                    if visual != '':
                      if jogo.visual == None:
                        jogo.visual = visual
                      else:
                        jogo.visual += ' / '
                        jogo.visual += visual

                elif 'Gameplay' in elemento.text:
                  gameplays = (xboxGamesInformacoes2[numInformacaoJogoXbox].text).split('\n')
                  for gameplay in gameplays:
                    if gameplay != '':
                      if jogo.gameplay == None:
                        jogo.gameplay = gameplay
                      else:
                        jogo.gameplay += ' / '
                        jogo.gameplay += gameplay

                
                numInformacaoJogoXbox += 1
                
              comandoView = 1
              while comandoView != 0:

                comandoView = int(
                  input(
                    """Digite o número correspondente para ver a informação do jogo:
              0- Sair
              1- Publicadora
              2- Desenvolvedora
              3- Nota
              4- Data de lançamento
              5- Porcentagem de notas positivas dos críticos
              6- Capa
              7- Gêneros
              8- Perspectivas 
              9- Tipo de visual 
              10- Tipo de gameplay
              """))

                
                if comandoView == 1:
                  exibe(jogo.publisher)

                elif comandoView == 2:
                  exibe(jogo.developer)

                elif comandoView == 3:
                  exibe(jogo.rating)

                elif comandoView == 4:
                  exibe(jogo.dataLancamento)

                elif comandoView == 5:
                  exibe(jogo.criticos)

                elif comandoView == 6:
                  tituloSemEspaco = (jogo.titulo).replace(" ", "")
                  with open(tituloSemEspaco + '.jpg', 'wb') as file:
                    file.write(capa_content)
                  print("-----------------")
                  print("Capa salva como %s" % (tituloSemEspaco + '.jpg'))
                  print("-----------------")

                elif comandoView == 7:
                  exibe(jogo.genero)

                elif comandoView == 8:
                  exibe(jogo.perspectiva)

                elif comandoView == 9:
                  exibe(jogo.visual)

                elif comandoView == 10:
                  exibe(jogo.gameplay)

                elif comandoView != 0:
                  print("-----------------")
                  print("Comando inválido. Tente novamente.")
                  print("-----------------")

            else:
              print("Erro")
              print(responseXboxGame)

          elif comando != '-1':
              print("-----------------")
              print("Comando inválido.")
              print("-----------------")

        else:
          print("Erro.")
          print(response.status_code)
    elif escolha != '0':
      print("Comando inválido.")

main()