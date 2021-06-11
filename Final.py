import requests
from datetime import datetime
import pandas as pd


def menu_inicial(n_senha, tam_senha):
    print('\nSeja bem vindo ao SENAC. Para continuar seu cadastro, escolha uma das opções abaixo:\n ')
    print('1. Login')
    print('2. Cadastro de conta')
    print('3. Esqueci minha senha')
    print('4. Sair do sistema')
    sair = False
    while not sair:
        escolha = input('\nDigite a opção desejada: ')
        if escolha == '1':
            login_conta()
        elif escolha == '2':
            cadastro_conta(n_senha, tam_senha)
        elif escolha == '3':
            esqueci_senha()
        elif escolha == '4':
            print('\nObrigado por usar nosso sistema')
            sair = True
        else:
            print('\nOpção inválida')
    return


def login_conta():
    loginemail = input('Digite seu e-mail: ')
    loginsenha = input('Digite sua senha: ')
    print(loginemail, loginsenha)
    print('\nLogin realizado.')
    return


def escolha_senha(n, t_senha):
    lista_de_numeros = []
    while len(lista_de_numeros) < n:
        print('\nVoce deve digitar {:.0f} numeros distintos de {:.0f} digitos'.format(n, t_senha))
        digitado = input('Digite os números desejados: ')
        if len(digitado) == t_senha and digitado not in lista_de_numeros:
            try:
                lista_de_numeros.append(digitado)
            except Exception as error:
                print(error)
                print(digitado + ' não é um número')
        else:
            print('O número digitado não possui {} dígitos ou já foi usado. Tente novamente.\n'.format(t_senha))
    senha = min(lista_de_numeros)
    return senha


def cadastro_conta(n_sen, t_senha):
    print('\nPara continuar seu cadastro, serão necessários os seguintes dados: ')

    nomeuser = str(input('\nEscreva seu nome completo: '))
    user = str(input('\nDigite um nome de usuário: '))
    senhafinal = escolha_senha(n_sen, t_senha)

    print("\nUse está senha gerada para futuros acessos:", senhafinal)

    nomeanimal = input('\nPara uma segurança mais eficaz da sua conta, digite o nome de um animal de sua escolha: ')
    escola = input('\nNome da escola em que estudou: ')
    input('\nTelefone para contato: ')
    email = input('\nDigite seu e-mail: ')
    empresa = input('\nEscreva o nome da empresa em que trabalha ou tenha interesse em trabalhar futuramente: ')

    # Informações de CPF
    def todos_numeros_iguais(cpf_1):
        if len(cpf_1) < 0:
            return True
        return all(x == cpf_1[0] for x in cpf_1)

    def recupera_soma(cpf_1, fator):
        return sum([int(n) * (fator - pos) for pos, n in enumerate(cpf_1[:9])])

    def recupera_digito(soma):
        resultado = (soma * 10) % 11
        if resultado == 10:
            return 0
        return resultado

    def recupera_primeiro_digito(cpf_1):
        soma = recupera_soma(cpf_1, 10)
        return recupera_digito(soma)

    def recupera_segundo_digito(cpf_1, primeiro_digito):
        soma = recupera_soma(cpf_1, 11) + (primeiro_digito * 2)
        return recupera_digito(soma)

    def cpf_valido(cpf_1):
        cpf_1 = cpf_1.replace('.', '').replace('-', '')
        if len(cpf_1) != 11 or not cpf_1.isnumeric() or todos_numeros_iguais(cpf_1):
            return False
        digito1 = recupera_primeiro_digito(cpf_1)
        digito2 = recupera_segundo_digito(cpf_1, digito1)
        return digito1 == int(cpf_1[9]) and digito2 == int(cpf_1[10])

    print('\nInforme seu CPF: ')
    cpf = input()
    if cpf_valido(cpf):
        print('CPF é válido.\n')
    else:
        print('CPF inválido.\n')

    # informações de CEP
    address = 'erro'
    while address == 'erro':
        correto = False
        while not correto:
            cep_input = input('Digite o CEP para a consulta: ')

            if len(cep_input) != 8:
                print('Quantidade de dígitos inválida!')
            else:
                correto = True

        request = requests.get('https://viacep.com.br/ws/{}/json/'.format(cep_input))
        address_data = request.json()
        if 'erro' in address_data:
            print('CEP inválido:', cep_input)
        else:
            address = 'certo'

    print('CEP identificado: ')
    print("CEP: ", address_data['cep'])
    print('Logradouro: ', address_data['logradouro'])
    print('Bairro: ', address_data['bairro'])
    print('Cidade: ', address_data['localidade'])
    print('Estado: ', address_data['uf'])

    # calculo do IMC
    altura = float(input("\nDigite sua altura: "))
    peso = float(input("Peso: "))
    imc = round(peso / (altura ** 2), 2)
    print("\nSeu IMC é: %.4f" % imc)
    if imc < 20:
        print('Abaixo do peso.\n')
    elif imc <= 25:
        print('IMC ideal.\n')
    elif imc <= 30:
        print('Acima do peso.\n')

    # informações sobre genero
    sexo = str(input('(M) - Masculino\n(F) - Feminino. \nDigite uma letra de acordo com seu sexo: ').upper())
    if sexo == 'M':
        print('Sexo Masculino.\n')
    elif sexo == 'F':
        print('Sexo Feminino.\n')
    else:
        print('Sexo Inválido\n')

    print('\nPara avaliarmos a possibilidade de um desconto na matricula, digite sua idade e nascimento: ')

    # sistema de renda
    def menu(valor_tot, pol_idade, pol_renda):
        print('\nOlá! Bem vindo ao sistema de cálculo de descontos')
        continuar = True
        while continuar:
            print('\nDigite uma das opções abaixo:')
            print('1 - Calcular desconto')
            print('2 - Sair do sistema')
            opcao = input('\nDigite a opção desejada: ')
            if opcao == '1':
                nome, desc_idd, desc_rd = calcular_desconto(valor_tot, pol_idade, pol_renda)
                resultados(valor_tot, nome, desc_idd, desc_rd)
            elif opcao == '2':
                print('\nObrigado por usar nosso sistema')
                continuar = False
            else:
                print('Opção inválida')
                continuar = True
        return

    def calcular_desconto(valor_cheio, d_idade, d_renda):
        desconto_renda = 0
        desconto_idade = 0
        print('\nPrecisamos de algumas informações para calcular o seu desconto')
        idade = int(input('Qual a sua idade? '))
        renda = int(input('Qual a sua renda mensal? '))
        gravar(nomeanimal, address_data['uf'], idade, escola, senhafinal, nomeuser, renda, empresa, sexo, imc,
               address_data['cep'], email, user)
        j = 0
        while j < len(d_idade):
            if d_idade[j][0] <= idade < d_idade[j][1]:
                desconto_idade = valor_cheio * d_idade[j][2]
            j += 1
        k = 0
        while k < len(d_renda):
            if d_renda[k][0] < renda <= d_renda[k][1]:
                desconto_renda = valor_cheio * d_renda[k][2]
            k += 1
        return nomeuser, desconto_idade, desconto_renda

    def resultados(vt, nome, d1, d2):
        print(f"\nCaro(a) Sr(a). {nome}")
        print(f'O valor normal da mensalidade é de R$ {vt:.0f}.')
        print('\nBaseado no seu perfil de idade e renda, concederemos os seguintes descontos:')
        print(f'Um desconto por idade, no valor de R$ {d1:.0f}; e um desconto por renda, no valor de R$ {d2:.0f}.')
        print(f'O seu desconto total foi de R$ {d1 + d2:.0f}.')
        print(f'Assim sendo, o valor final da sua mensalidade será de R$ {vt - d1 - d2:.0f}.')
        print("\nEsperamos que estes descontos permitam que você decida por nossos cursos.")
        print('Seja bem-vindo(a). Obrigado!')

    # variaveis da idade/renda
    valor_mensalidade = 500
    desc_idade = [[1, 24, 0.0], [25, 235, 0.1]]  # faixas de idade e % de desconto
    desc_renda = [[1, 1000, .30], [1000, 2000, .25], [2000, 100000, .20]]  # faixas de renda e % de desconto

    if __name__ == '__main__':
        menu(valor_mensalidade, desc_idade, desc_renda)


def esqueci_senha():
    input('E-mail ou CPF vinculado a sua conta: ')
    print('Foi enviado um e-mail para redefinir sua senha.')


# banco de dados
def gravar(nomeanimal, estado, idade, nomeescola, senhafinal, loginfinal, renda, trabalho, sexo, imc, cep, email, user):
    registro = [[nomeanimal, estado, idade, nomeescola, senhafinal, loginfinal, renda, trabalho, sexo, imc, cep, email,
                 user]]
    df_2 = pd.DataFrame(registro)
    df_2.to_csv("Final.csv", mode="a", header=False)
    return


def ler(arquivo, colunas):
    df_2 = pd.read_csv(arquivo, index_col=0, header=None)
    df_2.columns = colunas
    return df_2


# variaveis da senha
num_senha = 3  # numero de digitaçoes para escolha da senha
tamanho_senha = 4  # numero de algarismos na senha

if __name__ == '__main__':
    columns = ["nomeanimal", "estado", "idade", "nomeescola", "senhafinal", "loginfinal", "renda",
               "trabalho", "sexo", "imc", "cep", "email", "user"]
    df = pd.DataFrame(columns=columns)
    menu_inicial(num_senha, tamanho_senha)
    df_1 = ler("Final.csv", columns)
    df_1.reset_index(inplace=True, drop=True)
    imprimir = input('Deseja imprimir o banco de dados? (Sim/Não): ')
    if imprimir == 'Sim':
        for i in range(len(df_1)):
            print(df_1.iloc[i].values)
    df_describe = df_1.describe()
    df_describe.drop(['senhafinal'], axis=1, inplace=True)
    print(df_describe)
