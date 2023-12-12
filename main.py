from argparse import ArgumentParser
from os import path
from classes import AFNDe

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="arquivo", help="Recebe arquivo automato de entrada", metavar="FILE", required=True)
    parser.add_argument("-o", "--output", dest="output", help="Exporta o automato transformado como arquivo")
    args = parser.parse_args()

    if not path.isfile(args.arquivo):
        print("Arquivo inexistente")
        exit 

    alfabeto = None
    estados  = None
    iniciais = None
    finais   = None
    palavras = []
    transicoes = {}

    # lê o arquivo do automato
    with open(args.arquivo) as f:
        linhas = f.read().splitlines()
        for linha in linhas:
            if linha == "": 
                continue
            elif linha[0] == "A":
                alfabeto = linha[2:].split(" ")
            
            elif linha[0] == "Q":
                estados = linha[2:].split(" ")

            elif linha[0] == "q":
                iniciais = linha[2:].split(" ")
            
            elif linha[0] == "F": 
                finais = linha[2:].split(" ")

            elif linha[0] == "T":
                content = linha[2:].split(" ")
                if(len(content) != 3):
                    print("Transicao inválida")
                    exit
                if (content[0], content[1]) not in transicoes:
                    transicoes[content[0], content[1]] = []
                transicoes[content[0], content[1]].append(content[2])

            elif linha[0] == "P":
                palavras.append(linha[2:])

    if (alfabeto == None or
        estados  == None or
        iniciais == None or
        finais   == None or
        transicoes == {}):
        print("Arquivo não corresponde à um automato válido")
        exit

    # Transforma o automato e roda as palavras
    automato = AFNDe(alfabeto, estados, iniciais, finais, transicoes)
    automato.to_AFND()
    automato.to_AFD()

    for palavra in palavras:
        if automato.run(palavra) == True:
            print("M aceita a palavra <{}>".format(palavra))
        else:
            print("M rejeita a palavra <{}>".format(palavra))

    if args.output != None:
        fid = open(args.output, 'w')
        
        fid.write("# Alfabeto:\nA ")
        for symbol in automato.Alfabeto:
            fid.write("{} ".format(symbol))

        fid.write("\n\n# Estados:\nQ ")
        for state in automato.Estados:
            fid.write("{} ".format(state))

        fid.write("\n\n# Estado Inicial:\nq ")
        for state in automato.Inicial:
            fid.write("{} ".format(state))

        fid.write("\n\n# Estados Finais:\nF ")
        for state in automato.Finais:
            fid.write("{} ".format(state))

        fid.write("\n\n# Transicoes\n")
        for state, symbol in automato.Transicoes:
            fid.write("T {} {} {}\n".format(state, symbol, automato.Transicoes[state,symbol]))

        fid.write("\n\n# Palavras\n")
        for palavra in palavras:
            if automato.run(palavra) == True:
                fid.write("M aceita a palavra <{}>\n".format(palavra))
            else:
                fid.write("M rejeita a palavra <{}>\n".format(palavra))

        fid.close()

