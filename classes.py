class AFNDe:


    def __init__(self, Alfabeto, Estados, Iniciais, Finais, Transicoes):
        self.Alfabeto = set(Alfabeto)
        self.Estados = set(Estados)
        self.Inicial = set(Iniciais)
        self.Finais = set(Finais)
        self.Transicoes = Transicoes



    def to_AFND(self):
        new_transition = {}
        Transicoes = self.Transicoes
        
        for state, symbol in Transicoes:
            if(symbol == "^e"):
                continue

            new_states = Transicoes[state, symbol]
            for new_state in new_states:
                # transfere estados resultantes do vazio
                if (new_state, "^e") in Transicoes:
                    empty_transitions = Transicoes[new_state, "^e"];
                    
                    if (state, symbol) not in new_transition:
                        new_transition[state, symbol] = []

                    for states in empty_transitions:
                        if states not in new_transition[state, symbol]:
                            new_transition[state, symbol].append(states)


                # se o estado resultante não for obsoleto, adiciona a regra normal
                for symbol2 in self.Alfabeto:
                    if (new_state, symbol2) in Transicoes:
                       
                        if (state, symbol) not in new_transition:
                            new_transition[state, symbol] = []
                    
                        if new_state not in new_transition[state, symbol]:
                            new_transition[state, symbol].append(new_state)
                        
                        break;
                
                if new_state in self.Finais:
                    if (state, symbol) not in new_transition:
                        new_transition[state, symbol] = []

                    if new_state not in new_transition[state, symbol]:
                        new_transition[state, symbol].append(new_state)

        self.Transicoes = new_transition


    def to_AFD(self):
        """
        1. copiar estados
        2. mantém símbolos
        3. criar nova pilha "novos estados"
        4. o conteúdo em novos estados deve ser ordenado


        enquanto a transição original for determinística:
            copiar normalmente a transição

        se a transição original for não determinística
            colocamos os estados da transição em novos estados em um
            campo X do array.

        Para cada conteúdo em novos estados: (descobrimos as transições dele)
            Para cada símbolo, acessamos concatenando cada uma 
            das transições dos estados diferentes em X, se a transição
            resulta em um estado não existente, colocamos o estado não
            existente em novos estados
        """	
        Simbolos = self.Alfabeto 
        Estados = self.Estados
        Transicoes = self.Transicoes
        
        new_Stack = []
        new_States_Set = set(Estados)
        new_Finals_Set = set(self.Finais)
        new_Transitions = {}


        for transicao_Estado, transicao_Simbolo in Transicoes:
            new_States = Transicoes[transicao_Estado, transicao_Simbolo] 
            if ( len(new_States) == 1 ):
                new_Transitions[transicao_Estado, transicao_Simbolo] = new_States[0]

            else:
                sorted_New_States = sorted(new_States)
                new_Stack.append(new_States)
                new_Transitions[transicao_Estado, transicao_Simbolo] = "".join(sorted_New_States)

        for stack_Content in new_Stack:
            joined = "".join(stack_Content)
            if joined in new_States_Set:
                continue
            
            for state in stack_Content:
                if state in self.Finais:
                    new_Finals_Set.add(joined)
                    break
                
            new_States_Set.add(joined)
            for Symbol in Simbolos:
                new_Result_State = set()
                for individual_State in stack_Content:
                    if (individual_State, Symbol) not in Transicoes:
                        continue

                    new_States = Transicoes[individual_State, Symbol]
                    for list_States in new_States:
                        for state in list_States:
                            new_Result_State.add(state)

                new_Result_State = sorted(new_Result_State)
                new_Stack.append(new_Result_State)

                new_Result_State = "".join(new_Result_State)
                new_Transitions[joined, Symbol] = new_Result_State

        self.Estados = new_States_Set
        self.Transicoes = new_Transitions
        self.Finais = new_Finals_Set



    def run(self, Palavra):
        estado_Atual = next(iter(self.Inicial))
        for symbol in Palavra:
            if (estado_Atual, symbol) not in self.Transicoes:
                return False
            estado_Atual = self.Transicoes[estado_Atual, symbol]

        if estado_Atual in self.Finais:
            return True
        
        return False



