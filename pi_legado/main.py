
#importação
import time
import oracledb
from conexao import conectar_banco
from funcoes import mostrar_dados
from funcoes import criptografia
from funcoes import descriptografia
from funcoes import funcmenu
#conecta com banco de dados
connection = conectar_banco()

#projeto Integrador
print('''\n\t 
========================================================================== 
|    BBBBB   EEEEE   M   M         V   V   IIIII   N   N   DDDD    OOOO   |
|    B    B  E       MM MM         V   V     I     NN  N   D   D  O    O  |
|    BBBBB   EEEE    M M M          V V      I     N N N   D   D  O    O  |
|    B    B  E       M   M          V V      I     N  NN   D   D  O    O  |
|    BBBBB   EEEEE   M   M           V     IIIII   N   N   DDDD    OOOO   |
==========================================================================
      |                 SISTEMA DE CADASTRO DE PRODUTOS            |
      |                     PARA SISTEMAS DE ESTOQUE               |  
      ==============================================================''')
time.sleep(1)

menu = funcmenu()
while menu != 5:
    if menu == 1:
        cursor = connection.cursor()
        print("\n\t\t<<< Cadastro de produto >>>\n")
        id_produto = int(input('ID do produto: '))

        cursor.execute(f"SELECT idProduto FROM piprodutos WHERE idProduto = {id_produto}")
        existing_product = cursor.fetchone()

        while existing_product:
            print('Produto com este id já existe.')
            id_produto = int(input('ID do produto: '))
            cursor.execute(f"SELECT idProduto FROM piprodutos WHERE idProduto = {id_produto}")
            existing_product = cursor.fetchone()
        else:
            nome_produto = str(input('Nome do produto: '))
            descricao_produto = str(input('Descrição: '))
            custo_produto = float(input('Custo do produto: '))
            custo_imposto = float(input('Imposto (%): '))
            comissao_vendas = float(input('Comissão da venda (%): '))
            custo_fixo = float(input('Custo fixo (%): '))
            margem_lucro = float(input("Rentabilidade (%): "))
            while comissao_vendas+custo_fixo+custo_imposto+margem_lucro>100: 
                print("Digite um valor válido de rentabilidade")
                margem_lucro = float(input("Rentabilidade: %"))    
            pv = 100*custo_produto/(100 -(custo_fixo+  comissao_vendas + custo_imposto + margem_lucro))
            descricao_produto = criptografia(descricao_produto)
            if margem_lucro>20:
                Rentabilidade = 'Margem de lucro alta'
            elif margem_lucro <= 20 and margem_lucro > 10:
                Rentabilidade = 'Margem de lucro média'
            elif margem_lucro <=10 and margem_lucro > 0:
                Rentabilidade = 'Margem de lucro baixa'
            elif margem_lucro == 0:
                Rentabilidade = 'Equilíbrio'
            else:
                Rentabilidade = 'Prejuízo'
            print(f"\nLucro: {Rentabilidade}")
            
            
            cursor.execute("""
                    INSERT INTO PIProdutos (idProduto, nome, descricao, custoProduto, custofixo, comissao, imposto, margemLucro)
                    VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
                    """, (id_produto, nome_produto, descricao_produto, custo_produto, custo_fixo, comissao_vendas, custo_imposto, margem_lucro))
            
            connection.commit()
        

            print('\nDados inseridos com sucesso.')      

        
    elif menu == 2:
        cursor = connection.cursor()
        print("\n\t\t<<< Lista de produtos >>>\n")
        cursor.execute("SELECT * FROM piprodutos")
        mostrar_dados(cursor)
        
    elif menu == 3:
        cursor = connection.cursor()
        print("\n\t\t<<< Alteração de cadastro >>>\n")
        idAlt = int(input("\n\tDigite o ID do produto que deseja alterar: "))
        cursor.execute(f"SELECT idProduto FROM piprodutos WHERE idProduto = {idAlt}")
        existeid = cursor.fetchone()
        if not existeid:
            print("\n\t\tO ID não existe!")
        else:
        
            cursor.execute(f"SELECT * FROM piprodutos where idProduto = {idAlt}")
            mostrar_dados(cursor)
            menuAlt = int(input('''\n\t 
                ---------------------------------------------
                |     DIGITE A OPÇÃO QUE DESEJAR ALTERAR    |
                ---------------------------------------------
            1- ID  | 2- Nome  |  3- Descrição | 4- Custo do Produto

            5- Custo Fixo | 6- Comissão de Vendas | 7- Custo Imposto
            
                            8- Margem de Lucro
            '''))

            
            if menuAlt == 1:
                op = 'idProduto'
            elif menuAlt == 2:
                op = 'nome'
            elif menuAlt == 3:
                op = 'descricao'
            elif menuAlt == 4:
                op = 'custoProduto'
            elif menuAlt == 5:
                op = 'custofixo'
            elif menuAlt == 6:
                op = 'comissao'
            elif menuAlt == 7:
                op = 'imposto'
            elif menuAlt == 8:
                op = 'margemLucro'
            else:
                print('Digite um opção valida!')
                
            
            if menuAlt ==1:
                vAlt = int(input("\n\tDigite o valor q deseja alterar: "))
                cursor.execute(f"SELECT idProduto FROM piprodutos WHERE idProduto = {vAlt}")
                existing_product = cursor.fetchone()
                
                while existing_product:
                    print('Produto com este id já existe.')
                    vAlt = int(input('ID do produto: '))
                    cursor.execute(f"SELECT idProduto FROM piprodutos WHERE idProduto = {vAlt}")
                    existing_product = cursor.fetchone()
                else:
                    cursor.execute(f"UPDATE PIProdutos SET {op} = {vAlt} WHERE idProduto = {idAlt}")
                    
            elif menuAlt == 2:

                vAlt = str(input("\n\tDigite a alteração: "))
                cursor.execute(f"UPDATE PIProdutos SET {op} = '{vAlt}' WHERE idProduto = {idAlt}")
                
            elif menuAlt==3:
                vAlt = str(input("\n\tDigite a alteração: "))
                vAlt=criptografia(vAlt)
                cursor.execute(f"UPDATE PIProdutos SET {op} = '{vAlt}' WHERE idProduto = {idAlt}")

            else:
                vAlt = float(input("\n\tDigite a alteração: "))
                cursor.execute(f"UPDATE PIProdutos SET {op} = {vAlt} WHERE idProduto = {idAlt}")
            
            print("\tProduto Alterado com sucesso!")
            connection.commit()
            
    elif menu == 4:
        print("\n\t\t<<< Exclusão de produto >>>\n")
        idExcluir = int(input("\n\tDigite o ID do produto que deseja excluir: "))
            

        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM PIProdutos WHERE idProduto = {idExcluir}")
        existeid=cursor.fetchone()
        if not existeid:
            print("O ID não existe!")
        else:
            cursor.execute(f"SELECT * FROM PIProdutos WHERE idProduto = {idExcluir}")
            mostrar_dados(cursor)   
            menuEx = str(input('\tDeseja realmente Excluir: s[SIM] n[NÃO]\n'))
            menuEx = menuEx.lower()
            if menuEx=='s':
                cursor.execute(f"DELETE FROM PIProdutos WHERE idProduto = {idExcluir}")
                connection.commit()
                print('\t\tProduto excluído com sucesso!')
            elif menuEx=='n':
                print('Produto não excluído')
            else:
                print('Digite uma opção válida!')
        
    else:
        print('\n\t DIGITE UM NÚMERO CORRESPONDENTE A UMA AÇÃO DO MENU')
        
    menu = funcmenu()
#cursor.close()
print ("Programa encerrado.")
connection.close()