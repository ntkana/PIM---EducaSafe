import time
import sys
import json
import os
import statistics

def texto(texto, velocidade=0.03):
    for caractere in texto:
        sys.stdout.write(caractere)
        sys.stdout.flush()
        time.sleep(velocidade)
    print()

def home():
    r = input("Primeira vez no EducaSafe? ").strip().capitalize()
    return r

def welcome():
    print("\n" + "=" * 30)
    texto("Bem-vindo(a) ao EducaSafe!", 0.05)
    print("=" * 30)
    texto(
        "\nNosso curso de Segurança Digital foi criado especialmente para pessoas idosas. "
        "Aqui, você vai aprender a navegar com segurança pela internet, reconhecer golpes e fraudes, "
        "e usar redes sociais com mais confiança.\n", 0.03
    )
    texto(
        "+ Ao longo do curso, você encontrará lições simples e práticas, com quizzes e desafios divertidos "
        "para testar seus conhecimentos.\nCada módulo tem, em média, 2h de duração, totalizando 10 horas de curso. "
        "Ao final, você receberá um certificado de conclusão!", 0.03
    )
    texto(
        ">>> Lembre-se: você pode aprender no seu próprio ritmo e repetir lições sempre que quiser. "
        "Estamos aqui para ajudar em cada passo da sua jornada digital.\n", 0.03
    )
    texto("Preparado(a) para se tornar um(a) Guardião(ã) da Segurança Digital?", 0.03)

    resposta = input("\nDigite 'Sim' para continuar ou 'Não' para sair: ").strip().capitalize()
    return resposta

def validarEmail(email):
    if email == email.lower() and email.endswith("@gmail.com"):
        permitido = "abcdefghijklmnopqrstuvwxyz0123456789._%+-"
        for caractere in email.split("@")[0]:
            if caractere not in permitido:
                return False
        return True
    return False

def validarSenha(senha):
    return len(senha) >= 8 and any(c.islower() for c in senha) and any(c.isupper() for c in senha)

def carregarUsuarios():
    if os.path.exists("users.json"):
        with open("users.json", "r") as arquivo:
            return json.load(arquivo)
    return {}

def salvarUsuarios(usuarios):
    with open("users.json", "w") as arquivo:
        json.dump(usuarios, arquivo, indent=4)

def cadastro():
    usuarios = carregarUsuarios()
    
    nomeSignIn = input("\nDigite o seu nome completo: ")

    while True:
        sexo = input("Informe seu sexo (Masculino/Feminino): ").strip().capitalize()
        if sexo in ["Masculino", "Feminino"]:
            break
        else:
            print("Resposta inválida. Digite Masculino ou Feminino.")

    while True:
        try:
            idade = int(input("Digite sua idade: "))
            break
        except ValueError:
            print("Por favor, digite apenas números.")

    conhecimento = input("Você já tem algum conhecimento básico sobre segurança digital? (Sim/Não): ").strip().capitalize()

    while True:
        emailSignIn = input("Digite o seu email: ").strip()
        if validarEmail(emailSignIn):
            break
        else:
            texto("E-mail inválido. Certifique-se de que está todo em minúsculas e termina com @gmail.com.", 0.02)

    while True:
        senhaSignIn = input("Digite uma senha: ")
        if validarSenha(senhaSignIn):
            confSenhaSignIn = input("Confirme a senha: ")
            if senhaSignIn == confSenhaSignIn:
                texto("\nCadastro concluído com sucesso!", 0.03)
                texto("Perfeito, agora vamos dar início à nossa jornada!", 0.01)
                usuarios[emailSignIn] = {
                    "nome": nomeSignIn,
                    "sexo": sexo,
                    "idade": idade,
                    "conhecimento": conhecimento,
                    "senha": senhaSignIn,
                    "tempos": [],
                    "progresso": {}
                }
                salvarUsuarios(usuarios)
                return emailSignIn  
            else:
                texto("As senhas não coincidem. Tente novamente.", 0.02)
        else:
            texto("Senha inválida. Deve ter pelo menos 8 caracteres, uma letra maiúscula e uma minúscula.", 0.02)

def login():
    usuarios = carregarUsuarios()
    
    emailLogin = input("\nDigite seu email: ").strip()
    senhaLogin = input("Digite sua senha: ").strip()
    
    if emailLogin in usuarios and usuarios[emailLogin]["senha"] == senhaLogin:
        texto("\nLogin realizado com sucesso!", 0.03)
        texto(f"Bem-vindo(a), {usuarios[emailLogin]['nome']}!", 0.03)
        inicio = time.time()
        return usuarios, emailLogin, inicio
    else:
        texto("\nEmail ou senha incorretos. Tente novamente.", 0.03)
        return None, None, None

def logout(usuarios, emailLogin, inicio):
    fim = time.time()
    duracao = round(fim - inicio, 2)
    usuarios[emailLogin]["tempos"].append(duracao)
    salvarUsuarios(usuarios)

def estatisticas():
    usuarios = carregarUsuarios()
    total = len(usuarios)
    if total == 0:
        print("Nenhum usuário registrado ainda.")
        return

    idades = [u["idade"] for u in usuarios.values()]
    homens = [u for u in usuarios.values() if u["sexo"] == "Masculino"]
    mulheres = [u for u in usuarios.values() if u["sexo"] == "Feminino"]
    conhecimentos = [u["conhecimento"] == "Sim" for u in usuarios.values()]
    tempos_totais = [sum(u["tempos"]) for u in usuarios.values() if u["tempos"]]

    print("\n=== Estatísticas do EducaSafe ===")
    print(f"Total de usuários: {total}")
    print(f"Homens: {len(homens)} ({(len(homens)/total)*100:.1f}%)")
    print(f"Mulheres: {len(mulheres)} ({(len(mulheres)/total)*100:.1f}%)")
    print(f"Média de idade: {statistics.mean(idades):.1f}")
    print(f"Mediana da idade: {statistics.median(idades)}")
    try:
        print(f"Moda da idade: {statistics.mode(idades)}")
    except:
        print("Moda da idade: Não há uma moda única.")

    print(f"Pessoas com conhecimento prévio: {sum(conhecimentos)} ({(sum(conhecimentos)/total)*100:.1f}%)")

    if tempos_totais:
        print(f"Tempo médio de uso: {statistics.mean(tempos_totais):.1f} segundos")
    else:
        print("Nenhum dado de tempo de uso disponível ainda.")

def perguntar(pergunta, alternativas, respostaCerta):
    print(f"\n{pergunta}")
    for alt in alternativas:
        print(alt)
    
    while True:
        resposta = input("Digite a letra da resposta correta: ").strip().upper()
        if resposta in ["A", "B", "C", "D"]:
            break
        else:
            print("Por favor, digite apenas A, B, C ou D.")
    
    if resposta == respostaCerta:
        print("Resposta correta!")
        return True
    else:
        print(f"Resposta errada. A resposta certa era: {respostaCerta}")
        return False

def modulo1(usuarios, emailLogin):
    progresso = usuarios[emailLogin].get("progresso", {})
    modulo1_info = progresso.get("modulo1")

    if modulo1_info:
        texto(f"\nVocê já fez este módulo antes e acertou {modulo1_info['acertos']} de {modulo1_info['total']} perguntas.", 0.03)
        refazer = input("Deseja refazer o módulo para tentar melhorar sua pontuação? (Sim/Não): ").strip().capitalize()
        if refazer != "Sim":
            texto("Tudo bem! Seu progresso foi mantido.", 0.03)
            return

    texto("\nMÓDULO 1 – Introdução à Segurança Digital", 0.04)
    texto("\nO que o(a) senhor(a) vai aprender neste módulo:", 0.03)
    texto("• O que é segurança digital;", 0.02)
    texto("• Quais são os golpes mais comuns na internet;", 0.02)
    texto("• Como se proteger com práticas simples no dia a dia.\n", 0.02)

    texto("Agora, vamos responder algumas perguntas para fixar o que aprendemos.\n", 0.03)

    perguntas = [
        ("1. O que é segurança digital?",
         ["A) Proteger o computador contra quedas.",
          "B) Garantir que seus dados estejam seguros na internet.",
          "C) Usar sempre o mesmo aplicativo de mensagens.",
          "D) Nunca desligar o computador."], "B"),
    ]

    perguntas += [ 
        ("2. Qual dos itens abaixo é um exemplo de golpe online?",
         ["A) Receber uma mensagem de um amigo.",
          "B) Baixar um aplicativo na loja oficial.",
          "C) Navegar em um site de notícias.",
          "D) Um e-mail dizendo que você ganhou um prêmio e precisa clicar em um link."], "D"),
        ("3. Por que devemos nos proteger na internet?",
         ["A) Para evitar vírus e fraudes.",
          "B) Para jogar mais rápido.",
          "C) Para ganhar prêmios.",
          "D) Para acessar qualquer site sem problemas."], "A"),
        ("4. O que NÃO devemos fazer ao navegar na internet?",
         ["A) Clicar em qualquer link recebido por e-mail.",
          "B) Verificar se o site tem 'https://'.",
          "C) Usar senhas fortes.",
          "D) Manter o antivírus atualizado."], "A"),
        ("5. Qual das opções é uma boa prática de segurança digital?",
         ["A) Compartilhar senhas com amigos.",
          "B) Usar a mesma senha para todos os sites.",
          "C) Utilizar autenticação em dois fatores.",
          "D) Ignorar atualizações de software."], "C"),
        ("6. O que são fraudes online?",
         ["A) Produtos com desconto.",
          "B) Sites que vendem produtos falsos ou roubam dados.",
          "C) Propagandas na internet.",
          "D) Vídeos de entretenimento."], "B"),
        ("7. Como reconhecer um e-mail de phishing?",
         ["A) Sempre vem com imagens.",
          "B) Contém erros de gramática e links suspeitos.",
          "C) É enviado por amigos.",
          "D) É muito curto."], "B"),
        ("8. Qual o risco de baixar arquivos de sites desconhecidos?",
         ["A) Ganhar prêmios.",
          "B) Aumentar a velocidade do computador.",
          "C) Instalar vírus ou malware.",
          "D) Receber mais anúncios."], "C"),
        ("9. O que são vírus de computador?",
         ["A) Mensagens engraçadas.",
          "B) Programas que danificam o computador e roubam informações.",
          "C) Jogos online.",
          "D) Vídeos."], "B"),
        ("10. Qual a melhor maneira de proteger seus dispositivos?",
         ["A) Deixá-los sempre ligados.",
          "B) Nunca usar senhas.",
          "C) Desconectar da internet sempre.",
          "D) Usar antivírus e manter o sistema atualizado."], "D")
    ]

    acertos = 0
    for pergunta, alternativas, respostaCerta in perguntas:
        if perguntar(pergunta, alternativas, respostaCerta):
            acertos += 1

    print(f"\nO(a) senhor(a) acertou {acertos} de {len(perguntas)} perguntas.")

    atual = progresso.get("modulo1", {"acertos": 0})
    if acertos > atual["acertos"]:
        usuarios[emailLogin]["progresso"]["modulo1"] = {
            "acertos": acertos,
            "total": len(perguntas)
        }
        texto("Parabéns! Sua nova pontuação foi salva. ", 0.03)
    else:
        texto("Você não superou sua pontuação anterior, então manteremos a melhor nota.", 0.03)

        salvarUsuarios(usuarios)
    texto("Módulo 1 finalizado. Parabéns por avançar no seu aprendizado!", 0.03)

    while True:
        print("\nO que deseja fazer agora?")
        print("1 - Ir para o próximo módulo") 
        print("2 - Refazer o módulo")
        print("3 - Salvar e sair")
        escolha = input("Digite o número da opção desejada: ").strip()

        if escolha == "1":
            return "next" 
        elif escolha == "2":
            break
        elif escolha == "3":
            return "quit" 
        else:
            print("Opção inválida. Tente novamente.")

        if escolha == "1":
            modulo1(usuarios, emailLogin)
            return  
        elif escolha == "2":
            texto("Até a próxima! Seu progresso foi salvo.", 0.03)
            return
        else:
            print("Opção inválida. Tente novamente.")

usuarios = {}
emailLogin = None
inicio = None

resposta0 = home()

if resposta0 == "Sim":
    resposta1 = welcome()
    if resposta1 == "Sim":
        texto("\nÓtimo! Vamos começar o curso. \n", 0.03)
        texto("Primeiro vamos te cadastrar e criar o seu perfil!", 0.03)
        emailLogin = cadastro()
        usuarios = carregarUsuarios()
        inicio = time.time()
        texto(f"Bem-vindo(a), {usuarios[emailLogin]['nome']}! Você está pronto para começar o curso.", 0.03)

    elif resposta1 in ["Não", "Nao"]:
        texto("\nTudo bem! Estaremos aqui quando você estiver pronto(a). \n", 0.03)
        sys.exit()
    else:
        texto("\nResposta inválida. Tente novamente ao reiniciar o programa.\n", 0.03)
        sys.exit()

else:
    usuarios, emailLogin, inicio = login()

if usuarios and emailLogin:
    modulo1(usuarios, emailLogin)
    input("\nPressione Enter quando quiser sair do sistema...")
    logout(usuarios, emailLogin, inicio)

def modulo2(usuarios, emailLogin):
    progresso = usuarios[emailLogin].get("progresso", {})
    modulo_info = progresso.get("modulo2")

    if modulo_info:
        texto(f"\nVocê já fez este módulo antes e acertou {modulo_info['acertos']} de {modulo_info['total']} perguntas.", 0.03)
        refazer = input("Deseja refazer o módulo para tentar melhorar sua pontuação? (Sim/Não): ").strip().capitalize()
        if refazer != "Sim":
            texto("Tudo bem! Seu progresso foi mantido.", 0.03)
            return

    texto("\nMÓDULO 2 – Senhas e Dados Pessoais", 0.04)
    
    texto("\nNeste módulo, vamos conversar sobre algo muito importante: as nossas senhas e os nossos dados pessoais.", 0.03)
    texto("Muitas vezes, usamos senhas simples por serem fáceis de lembrar. Mas senhas fracas facilitam o trabalho de golpistas.", 0.03)
    texto("Uma boa senha deve ser como uma fechadura segura: difícil de adivinhar e única para cada porta (ou site).", 0.03)
    
    texto("\nO que é uma senha segura?", 0.03)
    texto("Uma senha segura mistura letras maiúsculas e minúsculas, números e símbolos. Exemplo: Abc123@!", 0.03)
    texto("Evite usar datas de nascimento, nomes de familiares ou sequências como '123456'.", 0.03)
    
    texto("\nPor que não repetir a mesma senha em todos os sites?", 0.03)
    texto("Imagine que alguém descubra sua senha do e-mail. Se você usar essa mesma senha no banco, no Facebook e em outros lugares, essa pessoa terá acesso a tudo!", 0.03)
    texto("Por isso, o ideal é ter senhas diferentes para cada site. Pode parecer complicado, mas existem cadernos seguros, ou aplicativos de cofre de senhas que ajudam nisso.", 0.03)
    
    texto("\nO que são dados pessoais?", 0.03)
    texto("São informações que identificam você: seu CPF, RG, endereço, telefone, número do cartão de crédito e até sua foto.", 0.03)
    texto("Esses dados devem ser protegidos, pois podem ser usados para aplicar golpes em seu nome.", 0.03)
    
    texto("\nNunca compartilhe senhas e dados por WhatsApp, e-mail ou telefone.", 0.03)
    texto("Mesmo que pareça ser alguém conhecido, desconfie. Golpistas podem se passar por familiares ou funcionários de banco.", 0.03)
    texto("Instituições sérias nunca pedem senhas por mensagem ou ligação. Nunca mesmo.", 0.03)

    texto("\nVamos revisar com algumas perguntas sobre o que acabamos de aprender.", 0.03)

    perguntas = [
        ("1. Qual das opções abaixo é uma senha segura?",
         ["A) 12345678", "B) minhaSenha", "C) Abc123@!", "D) senha123"], "C"),
        ("2. Por que é importante ter senhas diferentes em sites diferentes?",
         ["A) Porque fica mais bonito", "B) Para evitar que um vazamento comprometa tudo",
          "C) Para lembrar mais fácil", "D) Não faz diferença"], "B"),
        ("3. Quais são dados pessoais sensíveis?",
         ["A) Nome do seu cachorro", "B) CPF, endereço, dados bancários", "C) Comida favorita", "D) Cor preferida"], "B"),
        ("4. É seguro enviar sua senha por WhatsApp ou e-mail?",
         ["A) Sim, se for para alguém de confiança", "B) Sim, se for urgente",
          "C) Não, nunca é seguro", "D) Depende do celular"], "C"),
        ("5. Qual dessas práticas ajuda a proteger seus dados?",
         ["A) Usar datas de aniversário como senha",
          "B) Compartilhar senhas com familiares",
          "C) Criar senhas únicas e difíceis de adivinhar",
          "D) Anotar a senha em post-its perto do computador"], "C"),
    ]

    acertos = sum(perguntar(p, alts, resp) for p, alts, resp in perguntas)
    print(f"\nVocê acertou {acertos} de {len(perguntas)} perguntas.")

    atual = progresso.get("modulo2", {"acertos": 0})
    if acertos > atual["acertos"]:
        usuarios[emailLogin]["progresso"]["modulo2"] = {
            "acertos": acertos,
            "total": len(perguntas)
        }
        texto("Parabéns! Sua nova pontuação foi salva.", 0.03)
    else:
        texto("Você não superou sua pontuação anterior, então manteremos a melhor nota.", 0.03)

    salvarUsuarios(usuarios)
    texto("Módulo 2 finalizado. Ótimo trabalho!", 0.03)

    while True:
        print("\nO que deseja fazer agora?")
        print("1 - Refazer o módulo")
        print("2 - Salvar e sair")
        escolha = input("Digite o número da opção desejada: ").strip()

        if escolha == "1":
            modulo2(usuarios, emailLogin)
            return  
        elif escolha == "2":
            texto("Até a próxima! Seu progresso foi salvo.", 0.03)
            return
        else:
            print("Opção inválida. Tente novamente.")

def modulo3(usuarios, emailLogin):
    progresso = usuarios[emailLogin].get("progresso", {})
    modulo_info = progresso.get("modulo3")

    if modulo_info:
        texto(f"\nVocê já fez este módulo antes e acertou {modulo_info['acertos']} de {modulo_info['total']} perguntas.", 0.03)
        refazer = input("Deseja refazer o módulo para tentar melhorar sua pontuação? (Sim/Não): ").strip().capitalize()
        if refazer != "Sim":
            texto("Tudo bem! Seu progresso foi mantido.", 0.03)
            return

    texto("\nMÓDULO 3 – Golpes Comuns no Dia a Dia", 0.04)

    texto("\nNeste módulo, vamos aprender como funcionam os golpes mais comuns que circulam todos os dias, especialmente pela internet e pelo celular.", 0.03)
    texto("Muitos desses golpes são feitos para enganar pessoas de boa fé, se passando por parentes, bancos ou empresas conhecidas.", 0.03)
    texto("Nosso objetivo aqui é te ajudar a reconhecer essas armadilhas e saber como se proteger.", 0.03)

    texto("\nVamos ver alguns tipos de golpes muito comuns:", 0.03)

    texto("\n1. Golpes no WhatsApp", 0.03)
    texto("Você recebe uma mensagem de um número desconhecido dizendo que é seu filho, neto ou parente. A pessoa diz que trocou de número e pede dinheiro emprestado.", 0.03)
    texto("Em muitos casos, é um golpista se passando por alguém da família. Sempre ligue para confirmar antes de enviar qualquer valor.", 0.03)

    texto("\n2. Golpes por e-mail", 0.03)
    texto("Mensagens dizendo que sua conta vai ser cancelada, que você ganhou um prêmio ou que precisa clicar em um link para evitar um problema.", 0.03)
    texto("Esses e-mails costumam ter erros de português, logotipos falsos e links perigosos. Evite clicar. Apague imediatamente.", 0.03)

    texto("\n3. Links suspeitos", 0.03)
    texto("Às vezes, você recebe uma mensagem dizendo: 'Clique aqui para ganhar um prêmio' ou 'Você precisa atualizar seu cadastro'.", 0.03)
    texto("Esses links podem levar a sites falsos que roubam seus dados. Sempre desconfie de links que chegam sem aviso.", 0.03)

    texto("\n4. Telefonemas falsos", 0.03)
    texto("Alguém liga dizendo ser do banco ou da operadora do cartão. A pessoa diz que seu cartão foi clonado e pede número da conta, senha ou dados pessoais.", 0.03)
    texto("Desligue na hora. Nenhum banco liga pedindo senha. Se tiver dúvida, vá até a agência ou ligue para o número oficial da empresa.", 0.03)

    texto("\nAgora que você aprendeu a identificar golpes comuns, vamos testar seus conhecimentos com um pequeno questionário.", 0.03)

    perguntas = [
        ("1. Qual é um exemplo de golpe no WhatsApp?",
         ["A) Mensagem de bom dia", "B) Vídeo de família",
          "C) Pedido de dinheiro de um 'familiar' que trocou de número", "D) Piadas"], "C"),

        ("2. O que indica um e-mail suspeito?",
         ["A) Tem emoji", "B) Vem com erros de português e links estranhos",
          "C) Assunto alegre", "D) Vem de um conhecido"], "B"),

        ("3. Ao clicar em 'clique aqui para prêmio', você pode...",
         ["A) Ganhar algo", "B) Instalar vírus ou dar acesso aos seus dados",
          "C) Nada", "D) Acelerar o celular"], "B"),

        ("4. Um banco liga pedindo senha. O que fazer?",
         ["A) Informar tudo", "B) Ignorar",
          "C) Confirmar número e ligar de volta ao número oficial", "D) Agradecer"], "C"),

        ("5. Como evitar cair em golpes por links?",
         ["A) Conferir se o endereço do site é verdadeiro (ex: gov.br e não gov-br.com)",
          "B) Clicar rápido", "C) Ignorar segurança", "D) Só usar Wi-Fi"], "A"),
    ]

    acertos = sum(perguntar(p, alts, resp) for p, alts, resp in perguntas)
    print(f"\nVocê acertou {acertos} de {len(perguntas)} perguntas.")

    atual = progresso.get("modulo3", {"acertos": 0})
    if acertos > atual["acertos"]:
        usuarios[emailLogin]["progresso"]["modulo3"] = {
            "acertos": acertos,
            "total": len(perguntas)
        }
        texto("Parabéns! Sua nova pontuação foi salva.", 0.03)
    else:
        texto("Você não superou sua pontuação anterior, então manteremos a melhor nota.", 0.03)

    salvarUsuarios(usuarios)
    texto("Módulo 3 finalizado. Você está ficando cada vez mais preparado.", 0.03)

    while True:
        print("\nO que deseja fazer agora?")
        print("1 - Refazer o módulo")
        print("2 - Salvar e sair")
        escolha = input("Digite o número da opção desejada: ").strip()

        if escolha == "1":
            modulo3(usuarios, emailLogin)
            return  
        elif escolha == "2":
            texto("Até a próxima! Seu progresso foi salvo.", 0.03)
            return
        else:
            print("Opção inválida. Tente novamente.")

def modulo4(usuarios, emailLogin):
    progresso = usuarios[emailLogin].get("progresso", {})
    modulo_info = progresso.get("modulo4")

    if modulo_info:
        texto(f"\nVocê já fez este módulo antes e acertou {modulo_info['acertos']} de {modulo_info['total']} perguntas.", 0.03)
        refazer = input("Deseja refazer o módulo para tentar melhorar sua pontuação? (Sim/Não): ").strip().capitalize()
        if refazer != "Sim":
            texto("Tudo bem! Seu progresso foi mantido.", 0.03)
            return

    texto("\nMÓDULO 4 – Navegação Segura", 0.04)

    texto("\nNeste módulo, vamos aprender algumas práticas importantes para garantir que sua navegação na internet seja segura.", 0.03)
    texto("A internet pode ser um lugar maravilhoso, mas também tem riscos. Por isso, é importante tomar alguns cuidados.", 0.03)

    texto("\n1. Evite clicar em propagandas e notícias chamativas", 0.03)
    texto("Você pode encontrar pop-ups ou banners oferecendo prêmios ou descontos imperdíveis. Esses anúncios muitas vezes são falsos e podem levar você a sites perigosos. Sempre desconfie!", 0.03)

    texto("\n2. Sempre confira se o site começa com 'https://'", 0.03)
    texto("Quando você entrar em um site, verifique se ele começa com 'https://' e se há um cadeado na barra de endereços. Isso significa que a conexão é segura e que seus dados estarão protegidos.", 0.03)

    texto("\n3. Cuidado com downloads de aplicativos e arquivos", 0.03)
    texto("Não baixe aplicativos ou arquivos de fontes desconhecidas. Isso pode infectar seu dispositivo com vírus ou outros malwares. Baixe sempre de lojas oficiais como Google Play ou App Store.", 0.03)

    texto("\n4. Atualize seu celular/computador regularmente", 0.03)
    texto("Muitas atualizações contêm melhorias de segurança. Por isso, é importante manter seus dispositivos sempre atualizados para se proteger contra ameaças novas.", 0.03)

    texto("\nAgora que você já aprendeu algumas dicas de navegação segura, vamos testar seus conhecimentos.", 0.03)

    perguntas = [
        ("1. O que você deve fazer antes de clicar em um link ou propaganda?",
         ["A) Clicar rápido", "B) Verificar se o site é confiável", "C) Ignorar tudo", "D) Aguardar por 5 segundos"], "B"),

        ("2. Como saber se um site é seguro?",
         ["A) O site começa com 'https://' e tem um cadeado", "B) O site tem um fundo bonito", "C) O site tem muitos anúncios", "D) O site é novo"], "A"),

        ("3. O que é perigoso ao baixar um arquivo de um site desconhecido?",
         ["A) Melhorar a velocidade do seu computador", "B) Instalar vírus ou malware", "C) Não faz nada", "D) Nenhuma das alternativas"], "B"),

        ("4. Qual é a principal razão para manter o celular ou computador atualizado?",
         ["A) Melhorar o design", "B) Aumentar a velocidade", "C) Proteger contra novas ameaças", "D) Atualizar as fotos"], "C"),

        ("5. O que devemos fazer quando vemos uma notícia muito chamativa na internet?",
         ["A) Acreditar em tudo", "B) Procurar fontes confiáveis e confirmar a informação", "C) Compartilhar imediatamente", "D) Ignorar completamente"], "B"),
    ]

    acertos = sum(perguntar(p, alts, resp) for p, alts, resp in perguntas)
    print(f"\nVocê acertou {acertos} de {len(perguntas)} perguntas.")

    atual = progresso.get("modulo4", {"acertos": 0})
    if acertos > atual["acertos"]:
        usuarios[emailLogin]["progresso"]["modulo4"] = {
            "acertos": acertos,
            "total": len(perguntas)
        }
        texto("Parabéns! Sua nova pontuação foi salva.", 0.03)
    else:
        texto("Você não superou sua pontuação anterior, então manteremos a melhor nota.", 0.03)

    salvarUsuarios(usuarios)
    texto("Módulo 4 finalizado. Você está cada vez mais seguro na internet.", 0.03)

    while True:
        print("\nO que deseja fazer agora?")
        print("1 - Refazer o módulo")
        print("2 - Salvar e sair")
        escolha = input("Digite o número da opção desejada: ").strip()

        if escolha == "1":
            modulo4(usuarios, emailLogin)
            return  
        elif escolha == "2":
            texto("Até a próxima! Seu progresso foi salvo.", 0.03)
            return
        else:
            print("Opção inválida. Tente novamente.")

def modulo5(usuarios, emailLogin):
    progresso = usuarios[emailLogin].get("progresso", {})
    modulo_info = progresso.get("modulo5")

    if modulo_info:
        texto(f"\nVocê já fez este módulo antes e acertou {modulo_info['acertos']} de {modulo_info['total']} perguntas.", 0.03)
        refazer = input("Deseja refazer o módulo para tentar melhorar sua pontuação? (Sim/Não): ").strip().capitalize()
        if refazer != "Sim":
            texto("Tudo bem! Seu progresso foi mantido.", 0.03)
            return

    texto("\nMÓDULO 5 – Redes Sociais com Segurança", 0.04)

    texto("\nAs redes sociais são ótimas para manter contato com amigos e familiares, mas é preciso usá-las com segurança.", 0.03)
    texto("Neste módulo, vamos aprender algumas dicas para garantir que sua experiência nas redes sociais seja mais segura e tranquila.", 0.03)

    texto("\n1. Não aceite convites de pessoas desconhecidas", 0.03)
    texto("Pessoas que você não conhece podem estar se passando por alguém de sua confiança. Antes de aceitar qualquer solicitação, verifique o perfil da pessoa e, se possível, converse por outro meio.", 0.03)

    texto("\n2. Não poste informações sensíveis", 0.03)
    texto("Evite divulgar detalhes sobre sua localização, viagens, números de documentos e outras informações pessoais. Isso pode ser usado por criminosos para te prejudicar.", 0.03)

    texto("\n3. Configure a privacidade de suas redes sociais", 0.03)
    texto("Nas configurações das redes sociais, você pode definir quem pode ver suas postagens, quem pode comentar e quem pode enviar mensagens. Isso ajuda a proteger sua privacidade.", 0.03)

    texto("\n4. Perfis falsos de famosos ou conhecidos", 0.03)
    texto("Golpistas criam perfis falsos se passando por pessoas famosas ou pessoas da sua rede de contatos. Cuidado com perfis que tentam se aproximar e pedir dinheiro ou informações pessoais.", 0.03)

    texto("\nAgora que você aprendeu as principais dicas de segurança nas redes sociais, vamos testar seu conhecimento com algumas perguntas.", 0.03)

    perguntas = [
        ("1. O que fazer ao receber um convite de amizade de uma pessoa desconhecida?",
         ["A) Aceitar imediatamente", "B) Verificar o perfil e, se necessário, perguntar a amigos em comum", "C) Ignorar", "D) Nenhuma das alternativas"], "B"),

        ("2. Qual é o risco de postar sua localização em tempo real?",
         ["A) Nenhum, é apenas uma diversão", "B) Você pode atrair pessoas com más intenções", "C) Nada acontece", "D) Aumenta seu número de seguidores"], "B"),

        ("3. Como você pode proteger sua privacidade nas redes sociais?",
         ["A) Deixando tudo público", "B) Desabilitando as configurações de privacidade", "C) Configurando para que apenas amigos vejam suas postagens"], "D) Compartilhando tudo com todos", "C"),

        ("4. Como identificar um perfil falso nas redes sociais?",
         ["A) O perfil tem poucas postagens", "B) O perfil tem fotos muito bonitas", "C) O perfil tenta pedir dinheiro ou informações pessoais"], "D) O perfil tem muitos amigos", "C"),

        ("5. Você deve compartilhar senhas ou dados bancários por mensagem direta nas redes sociais?",
         ["A) Sim, é seguro", "B) Não, isso é muito perigoso", "C) Sim, se for com um amigo", "D) Só se pedir pelo chat"], "B"),
    ]

    acertos = sum(perguntar(p, alts, resp) for p, alts, resp in perguntas)
    print(f"\nVocê acertou {acertos} de {len(perguntas)} perguntas.")

    atual = progresso.get("modulo5", {"acertos": 0})
    if acertos > atual["acertos"]:
        usuarios[emailLogin]["progresso"]["modulo5"] = {
            "acertos": acertos,
            "total": len(perguntas)
        }
        texto("Parabéns! Sua nova pontuação foi salva.", 0.03)
    else:
        texto("Você não superou sua pontuação anterior, então manteremos a melhor nota.", 0.03)

    salvarUsuarios(usuarios)
    texto("Módulo 5 finalizado. Você agora sabe como se proteger nas redes sociais.", 0.03)

    while True:
        print("\nO que deseja fazer agora?")
        print("1 - Refazer o módulo")
        print("2 - Salvar e sair")
        escolha = input("Digite o número da opção desejada: ").strip()

        if escolha == "1":
            modulo5(usuarios, emailLogin)
            return  
        elif escolha == "2":
            texto("Até a próxima! Seu progresso foi salvo.", 0.03)
            return
        else:
            print("Opção inválida. Tente novamente.")

def prova_final(usuarios, emailLogin):
    progresso = usuarios[emailLogin].get("progresso", {})
    modulo_info = progresso.get("prova_final")

    if modulo_info:
        texto(f"\nVocê já fez esta prova antes e acertou {modulo_info['acertos']} de {modulo_info['total']} perguntas.", 0.03)
        refazer = input("Deseja refazer a prova para tentar melhorar sua pontuação? (Sim/Não): ").strip().capitalize()
        if refazer != "Sim":
            texto("Tudo bem! Seu progresso foi mantido.", 0.03)
            return

    texto("\nMÓDULO FINAL – A Prova de Segurança Digital", 0.04)

    texto("\nParabéns! Você completou os módulos de segurança digital e agora chegou o momento de testar tudo o que aprendeu.", 0.03)
    texto("Esta prova irá cobrir as principais dicas de segurança que discutimos nos módulos anteriores. Vamos ver o quanto você sabe!", 0.03)

    perguntas = [
        ("1. O que você deve fazer se encontrar um link suspeito em um e-mail ou mensagem?",
         ["A) Clicar nele para ver o que acontece", "B) Ignorar e deletar a mensagem", "C) Verificar se o remetente é confiável antes de clicar", "D) Compartilhar com amigos para saber se é real"], "C"),

        ("2. Qual é a principal diferença entre um site seguro e um site não seguro?",
         ["A) O design do site", "B) O endereço começa com 'https://' e tem um cadeado", "C) O número de anúncios", "D) O número de visitantes"], "B"),

        ("3. Por que você deve ter cuidado ao compartilhar informações pessoais em redes sociais?",
         ["A) Para proteger sua privacidade e evitar fraudes", "B) Para que as pessoas saibam mais sobre você", "C) Porque todo mundo gosta de saber mais sobre você", "D) Não há problema algum"], "A"),

        ("4. Se você não conhece a pessoa que está te convidando para uma rede social, o que deve fazer?",
         ["A) Aceitar o convite imediatamente", "B) Verificar o perfil e, se necessário, perguntar a amigos em comum", "C) Ignorar o convite", "D) Compartilhar seu número de telefone"], "B"),

        ("5. Quando é seguro baixar um arquivo de um site?",
         ["A) Quando o site parece confiável", "B) Quando o site começa com 'http://'", "C) Quando o site tem um cadeado na barra de endereços", "D) Quando o site tem um bom design"], "C"),

        ("6. O que é um vírus de computador?",
         ["A) Um programa que melhora o desempenho do computador", "B) Um arquivo malicioso que pode danificar seu dispositivo", "C) Uma forma de melhorar o sistema de segurança", "D) Um programa que aumenta a velocidade da internet"], "B"),

        ("7. O que deve ser feito se você perceber que alguém está tentando fraudar sua conta bancária online?",
         ["A) Ignorar e esperar que o problema desapareça", "B) Denunciar para o banco e mudar suas senhas", "C) Falar com amigos para saber o que fazer", "D) Deletar sua conta bancária"], "B"),

        ("8. Como você pode garantir que sua senha é segura?",
         ["A) Usando datas de nascimento simples", "B) Usando combinações de letras, números e símbolos", "C) Usando o nome do seu animal de estimação", "D) Usando o nome de sua cidade"], "B"),

        ("9. O que você deve fazer ao receber uma oferta de prêmio ou dinheiro em troca de informações pessoais?",
         ["A) Enviar as informações, pois é uma oportunidade", "B) Ignorar, pois pode ser uma fraude", "C) Pedir mais detalhes para confirmar a oferta", "D) Compartilhar com amigos para ganhar mais"], "B"),

        ("10. Como manter sua conta de rede social segura?",
         ["A) Deixando tudo público", "B) Aceitando todas as solicitações de amizade", "C) Configurando a privacidade e não compartilhando informações pessoais", "D) Usando senhas fáceis de lembrar"], "C"),
    ]

    acertos = sum(perguntar(p, alts, resp) for p, alts, resp in perguntas)
    print(f"\nVocê acertou {acertos} de {len(perguntas)} perguntas.")

    # Definir o número mínimo de acertos para aprovação (70% de 10 questões = 7 acertos)
    minimo_necessario = len(perguntas) * 0.7
    aprovado = acertos >= minimo_necessario

    if aprovado:
        texto("Parabéns! Você foi aprovado(a) na prova. Agora você está totalmente preparado(a) para navegar com segurança.", 0.03)
    else:
        texto("Infelizmente, você não atingiu a pontuação mínima para passar. Não se preocupe, você pode refazer a prova para melhorar sua pontuação.", 0.03)

    atual = progresso.get("prova_final", {"acertos": 0})
    if acertos > atual["acertos"]:
        usuarios[emailLogin]["progresso"]["prova_final"] = {
            "acertos": acertos,
            "total": len(perguntas)
        }
        texto("Sua nova pontuação foi salva.", 0.03)
    else:
        texto("Você não superou sua pontuação anterior, então manteremos a melhor nota.", 0.03)

    salvarUsuarios(usuarios)
    texto("Prova final concluída! Agora você está ainda mais preparado para navegar de forma segura na internet.", 0.03)

    while True:
        print("\nO que deseja fazer agora?")
        print("1 - Refazer a prova")
        print("2 - Salvar e sair")
        escolha = input("Digite o número da opção desejada: ").strip()

        if escolha == "1":
            prova_final(usuarios, emailLogin)
            return  
        elif escolha == "2":
            texto("Até a próxima! Seu progresso foi salvo.", 0.03)
            return
        else:
            print("Opção inválida. Tente novamente.")
