cadastrado = 0
quantidade = 0
ttotal = 0
total_item = 0

tquantidade = 0
ttotal_historico = 0

def menu():
    global cadastrado
    print('Bem vindo a Loja ADM Materiais de Construção\n')
    print('1 - Realizar cadastro\n')
    print('2 - Fazer compras\n')
    print('3 - Visualizar relatório\n')
    print('4 - Sair\n')
    opcao = int(input('Escolha uma opção: '))

    match opcao:
        case 1:
            cadastro()
        case 2:
            if cadastrado == 1:
                catalogo()
            else:
                print('Precisa fazer o cadastro primeiro!\n')
        case 3:
            relatorio()
        case 4:
            print('Saindo...')
            return False  # Retorna False para encerrar o loop principal
        case _:
            print('Modo inválido!\n')
    return True

def cadastro():
    global cadastrado
    nomeCad = input('Digite seu nome completo: \n')
    telefoneCad = int(input('Digite seu telefone: \n'))
    emailCad = input('Digite seu email: \n')
    cadastrado = 1
    print("Cadastro realizado com sucesso!\n")

def catalogo():
    global quantidade, ttotal, total_item
    preco = 0 

    while True:
        print('Produtos do nosso catálogo: \n')
        print('1 - tijolo - R$0,79')
        print('2 - cimento - R$37,00')
        print('3 - argamassa - R$18,00')
        print('4 - cal virgem - R$18,00')
        print('5 - areia - R$110,00\n')

        produtos = int(input('Escolha um produto e digite o id correspondente: '))

        match produtos:
            case 1:
                preco = 0.79
            case 2:
                preco = 37.00
            case 3:
                preco = 18.00
            case 4:
                preco = 18.00
            case 5:
                preco = 110.00
            case _:
                print('Opção inválida\n')
                continue 

        qtd_item = int(input('Escolha a quantidade: '))
        
        total_item = qtd_item * preco
        ttotal = ttotal + total_item
        quantidade = quantidade + qtd_item

        continuar = input("Deseja adicionar mais um produto? (S/N): ")

        if continuar.lower() == 'n':
            print(f'\nValor total da compra: R${ttotal:.2f}')
            pagamento()
            break

def pagamento():
    global ttotal, quantidade, ttotal_historico, tquantidade
    
    saldo_restante = ttotal
    
    print('\n--- FORMA DE PAGAMENTO ---')
    opcao_avista = input('O cliente vai pagar com Pix ou Dinheiro? (S/N): ').lower()

    if opcao_avista == 's':
        # Exibe o valor líquido apenas se for pagar em dinheiro ou Pix
        print('\n------------------------')
        print(f'Valor Total Bruto: R${saldo_restante:.2f}')
        print(f'Valor Líquido à vista (10% desc): R${(saldo_restante * 0.90):.2f}')
        print('------------------------')
    else:
        # Oculta completamente o valor líquido se for usar outra forma de pagamento
        print('\n------------------------')
        print(f'Valor Total da Compra: R${saldo_restante:.2f}')
        print('------------------------')

    while saldo_restante > 0:
        if opcao_avista == 's':
            print(f'\nSaldo restante a pagar (Bruto): R${saldo_restante:.2f}')
            print(f'-> Valor líquido restante com desconto: R${(saldo_restante * 0.90):.2f}')
            print('Escolha o método à vista:')
            print('1 - Pix (10% de desconto sobre o valor pago nesta modalidade)')
            print('2 - Dinheiro (10% de desconto sobre o valor pago nesta modalidade)')
            fpag = int(input('Escolha a opção: '))
        else:
            print(f'\nSaldo restante a pagar: R${saldo_restante:.2f}')
            print('Escolha a modalidade do cartão:')
            print('3 - Débito')
            print('4 - Crédito')
            fpag = int(input('Escolha a opção: '))

        match fpag:
            case 1 if opcao_avista == 's':  # PIX com desconto
                print(f'\n[PIX] Limite máximo necessário para quitar tudo com desconto: R${(saldo_restante * 0.90):.2f}')
                valor_desejado = float(input('Quanto deseja pagar no Pix? R$'))
                
                max_pagável_com_desconto = saldo_restante * 0.90
                if valor_desejado >= max_pagável_com_desconto:
                    valor_desejado = max_pagável_com_desconto
                    print(f'Valor ajustado para quitar o saldo total: R${valor_desejado:.2f}')
                
                ttotal_historico += valor_desejado
                valor_abatido = valor_desejado / 0.90
                saldo_restante -= valor_abatido
                print(f'Pagamento de R${valor_desejado:.2f} processado. Abatido R${valor_abatido:.2f} do saldo bruto.')

            case 2 if opcao_avista == 's':  # DINHEIRO com desconto e troco
                print(f'\n[DINHEIRO] Limite máximo necessário para quitar tudo com desconto: R${(saldo_restante * 0.90):.2f}')
                max_pagável_com_desconto = saldo_restante * 0.90
                
                valor_entregue = float(input('Quanto em dinheiro o cliente entregou? R$'))
                
                if valor_entregue >= max_pagável_com_desconto:
                    troco = valor_entregue - max_pagável_com_desconto
                    print('Pagamento em dinheiro quita o saldo restante!')
                    if troco > 0:
                        print(f'Troco a devolver: R${troco:.2f}')
                    
                    ttotal_historico += max_pagável_com_desconto
                    saldo_restante = 0
                else:
                    ttotal_historico += valor_entregue
                    valor_abatido = valor_entregue / 0.90
                    saldo_restante -= valor_abatido
                    print(f'Abatido R${valor_abatido:.2f} do saldo bruto.')

            case 3 | 4 if opcao_avista != 's':  # CARTÃO (Débito ou Crédito - sem desconto)
                tipo_cartao = "Débito" if fpag == 3 else "Crédito"
                print(f'\n[{tipo_cartao.upper()}] Saldo atual a pagar: R${saldo_restante:.2f}')
                
                valor_cartao = float(input(f'Quanto deseja passar no cartão de {tipo_cartao.lower()}? R$'))
                
                if valor_cartao > saldo_restante:
                    valor_cartao = saldo_restante
                    print(f'Valor ajustado para o limite do saldo: R${valor_cartao:.2f}')
                
                ttotal_historico += valor_cartao
                saldo_restante -= valor_cartao
                print(f'Pagamento de R${valor_cartao:.2f} no {tipo_cartao} processado.')

            case _:
                print('Modo inválido para a categoria de pagamento selecionada.')

    print('\n=====================================')
    print(' COMPRA FINALIZADA COM SUCESSO! ')
    print('=====================================')

    tquantidade += quantidade
    ttotal = 0
    quantidade = 0

def relatorio():
    global tquantidade, ttotal_historico
    print('\n==============================')
    print('Relatório Geral de Vendas da Loja:')
    print(f'Quantidade total de produtos vendidos: {tquantidade}')
    print(f'Valor total faturado (líquido com descontos): R${ttotal_historico:.2f}')
    print('==============================\n')

# LOOP PRINCIPAL QUE MANTÉM O PROGRAMA RODANDO
rodando = True
while rodando:
    rodando = menu()
