
def criptografia(nome):
    tabela= ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    vetcifra = []
    nome = nome.upper()
    nome = nome.replace(" ","")
    if len(nome)%2==1:
        nome += nome[len(nome)-1]

    for i in range(len(nome)): 
        aux = nome[i]
        aux =tabela.index(aux)
        aux +=1
        vetcifra.append(aux)
      
    matchave = [4,3,1,2]  

    vetcifrado =[]

    for i in range(0,3,2):
        for k in range(0,len(vetcifra),2):
        
            aux= 0
            aux += matchave[i]*vetcifra[k]
            aux +=matchave[i+1]*vetcifra[k+1]
            aux = aux%26
            vetcifrado.append(aux)

    nomecriptografado = ''

    k = len(vetcifra)//2

    for i in range(k):

        aux = vetcifrado[i]-1
        aux = tabela[aux]
        nomecriptografado = nomecriptografado+aux
        aux = vetcifrado[k]-1
        aux = tabela[aux]
        nomecriptografado+=aux
        k+=1
    
    return nomecriptografado

def descriptografia(desc):
    tabela= ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    
    
    descnumero = []
    desc = desc.upper()
    desc = desc.replace(" ","")
    for i in range(len(desc)):

        aux = tabela.index(desc[i])
        aux +=1

        if aux==26:
            aux=0

        descnumero.append(aux)

    matchave = [42,-63,-21,84]
    descnumero2 = []

    for i in range(0,3,2):
        for k in range(0,len(descnumero),2):

            aux = 0
            aux +=matchave[i]*descnumero[k]
            aux +=matchave[i+1]*descnumero[k+1]
            
            aux = aux%26
            
            descnumero2.append(aux)
            
    descnumero.clear()
    k = len(descnumero2)//2

    numerodescriptografado = []
    for i in range(k):
        aux = descnumero2[i]-1
        aux = tabela[aux]
        
        numerodescriptografado.append(aux)
        aux = descnumero2[k]-1
        aux = tabela[aux]
        numerodescriptografado.append(aux)
        k+=1

    letradescriptografada = ''
    for i in range(len(numerodescriptografado)):
        letradescriptografada += numerodescriptografado[i]
  
    return(letradescriptografada)

#mostrar dados
def mostrar_dados(cursor):
    for row in cursor:
                id_produto=row[0]
                nome_produto=row[1]
                descricao_produto=row[2]
                custo_produto=row[3]
                custo_imposto=row[6]
                comissao_vendas=row[5]
                custo_fixo=row[4]
                margem_lucro=row[7]
                pv = 100*custo_produto/(100 -(custo_fixo+  comissao_vendas + custo_imposto + margem_lucro))
                descricao_produto=descriptografia(descricao_produto)
                

                totalPorcentagens =custo_produto * ((custo_fixo/100) + (comissao_vendas/100) + (custo_imposto/100))
                totalGastos = totalPorcentagens +custo_produto
                D = pv*custo_fixo/100
                E = pv*comissao_vendas/100
                F = pv*custo_imposto/100
                OC = D+E+F
                C = pv-custo_produto
                H = C-OC
                CP_porcentagem = 100*custo_produto/pv
                custo_porcentagem = 100*C/pv
                CF_porcentagem = custo_fixo*pv/100
                CV_porcentagem = comissao_vendas*pv/100
                IV_porcentagem = custo_imposto*pv/100
                OC_porcentagem = 100*OC/pv 
                margem_reais = margem_lucro*pv/100
        
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
      
                print(f"\t\t{id_produto} {nome_produto}\t\t{descricao_produto} ")
                print("\nDescrição          Valor                       %")
                print(f"Preço de venda:     R${pv:.2f}                    100% ")
                print(f"Preço de compra:    R${custo_produto:.2f}                    {CP_porcentagem:.2f}%")
                print(f"Receita bruta:      R${C:.2f}                    {custo_porcentagem:.2f}%")
                print(f"Custo fixo:         R${CF_porcentagem:.2f}                    {custo_fixo:.2f}%")
                print(f"Comissão de vendas: R${CV_porcentagem:.2f}                     {comissao_vendas:.2f}%")
                print(f"Impostos:           R${IV_porcentagem:.2f}                     {custo_imposto:.2f}% ")
                print(f"Outros custos:      R${OC:.2f}                    {OC_porcentagem:.2f}%")
                print(f"H.Rentabilidade     R${margem_reais:.2f}              {margem_lucro:.2f}%")
                print(f"Lucro: {Rentabilidade}\n") 

def funcmenu():
    opcao = int(input('''\n\t 
            --------------------------------------
            |     DIGITE A OPÇÃO QUE DESEJAR!    |
            --------------------------------------
        1- Cadastrar Produto   2- Ver Produtos Castrados

        3- Alterar Produto     4- Exclusão de Produto
          
                        5- Sair
    '''))
    return opcao