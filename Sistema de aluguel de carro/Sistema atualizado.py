from datetime import datetime, timedelta
import re

class Veiculo:
    
    def __init__(self, placa, modelo, marca, ano, diaria):
        self.placa = placa.upper()
        self.modelo = modelo.title()
        self.marca = marca.title()
        self.ano = ano
        self.diaria = diaria
        self.status = "Disponível"
        
    def __str__(self):
        return f"Placa: {self.placa} | Modelo: {self.modelo} | Marca: {self.marca} | Ano: {self.ano} | Valor Diária: R${self.diaria:.2f} | Status: {self.status}"
    
    def calcular_preco_aluguel(self, dias):
        return dias * self.diaria
    
class Cliente:
    
    def __init__(self, nome, cpf, telefone, email, cnh):
        self.nome = nome.title()
        self.cpf = self.formatar_cpf(cpf)
        self.telefone = self.formatar_telefone(telefone)
        self.email = email.lower()
        self.cnh = cnh
        self.historico = []
    
    def adicionar_historico(self, aluguel):
        self.historico.append(aluguel)

    def formatar_cpf(self, cpf):
        cpf_numeros = re.sub(r'\D', '', cpf)
        return f'{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}'
    
    def formatar_telefone(self, telefone):
        telefone_numeros = re.sub(r'\D', '', telefone)
        return f'({telefone_numeros[:2]}) {telefone_numeros[2:7]}-{telefone_numeros[7:]}'
    
    def __str__(self):
        return f"Nome: {self.nome} | CPF: {self.cpf} | Telefone: {self.telefone} | Email: {self.email} | CNH: {self.cnh}"
    
class Aluguel:
    
    def __init__(self, cliente, veiculo, data_retirada, qte_dias, km_inicial):
        self.cliente = cliente
        self.veiculo = veiculo
        self.data_retirada = data_retirada
        self.data_devolucao = data_retirada + timedelta(days=qte_dias)
        self.km_inicial = km_inicial
        self.km_final = None
        self.valor_total = veiculo.calcular_preco_aluguel(qte_dias)
        self.status_pagamento = "Pendente"
    
    def devolver_veiculo(self, km_final, dias_atraso = 0, danos=False):
        self.km_final = km_final
        multa = 0
        if dias_atraso > 0:
            multa += dias_atraso * (self.veiculo.diaria * 0.2) 
        if danos:
            multa += self.veiculo.diaria * 5  
        self.valor_total += multa
        self.veiculo.status = "Disponível"
        self.status_pagamento = "Pago"

        print(f"\nDevolução realizada com sucesso!\nCliente: {self.cliente.nome} | Veículo: {self.veiculo.modelo} | Placa {self.veiculo.placa}\n"
          f"KM Inicial: {self.km_inicial} | KM Final: {self.km_final}\n"
          f"Dias em atraso: {dias_atraso} | Danos ao veículo: {'Sim' if danos else 'Não'}\n"
          f"Valor multas: R${multa} | Valor total: R${self.valor_total:.2f}")


    def __str__(self):
        return f"Cliente: {self.cliente.nome} | Veículo: {self.veiculo.modelo} | Placa: {self.veiculo.placa} | Data Retirada: {self.data_retirada.date()} | Devolução Prevista: {self.data_devolucao.date()} | Valor Total: R${self.valor_total:.2f}"
    
class SistemaAluguel:

    def __init__(self):
        self.veiculos = []
        self.clientes = []
        self.alugueis = []

    def cadastro_veiculo(self, placa, modelo, marca, ano, diaria):
        if any(veiculo.placa == placa.upper() for veiculo in self.veiculos):
            print(f"O veículo com placa {placa} já está cadastrado no sistema.")
            return
        veiculo = Veiculo(placa, modelo, marca, ano, diaria)
        self.veiculos.append(veiculo)
        print(f"\nNovo veículo cadastrado com sucesso!\nDados:\n{veiculo}")
    
    def validar_placa(self, placa):
        padrao = r'^[A-Za-z]{3}[0-9]{4}$|^[A-Za-z]{3}[0-9][A-Za-z][0-9]{2}$'
        if re.match(padrao, placa):
            return True
        else:
            return False

    def cadastro_cliente(self, nome, cpf, telefone, email, cnh):
        # Verifica se o CPF e CNH já foram cadastrados
        if any(cliente.cpf == self.formatar_cpf(cpf) for cliente in self.clientes):
            print(f"CPF {cpf} já cadastrado no sistema. Não é possível realizar novo cadastro.")
            return
        if any(cliente.cnh == cnh for cliente in self.clientes):
            print("CNH já cadastrada.")
            return
    
        if any(cliente.email == email.lower() for cliente in self.clientes):
            print("E-mail já cadastrado.")
            return

        cliente = Cliente(nome, cpf, telefone, email, cnh)
        self.clientes.append(cliente)
        print(f"\nNovo cliente cadastrado com sucesso!\nDados:\n{cliente}")

    def formatar_cpf(self, cpf):
        cpf_numeros = re.sub(r'\D', '', cpf)
        return f'{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}'

    def validar_cpf(self, cpf):
        cpf_numeros = re.sub(r'\D', '', cpf)
        if len(cpf_numeros) != 11:
            return False
        if cpf_numeros == cpf_numeros[0] * 11:
            return False
        soma = sum(int(cpf_numeros[i]) * (10 - i) for i in range(9))
        digito1 = 11 - (soma % 11)
        digito1 = digito1 if digito1 < 10 else 0
        soma = sum(int(cpf_numeros[i]) * (11 - i) for i in range(10))
        digito2 = 11 - (soma % 11)
        digito2 = digito2 if digito2 < 10 else 0

        return cpf_numeros[-2:] == f"{digito1}{digito2}"

    def validar_email(self, email):
        padrao = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(padrao, email))
    
    def validar_telefone(self, telefone):
        telefone_numeros = re.sub(r'\D', '', telefone)
        return len(telefone_numeros) == 11
    
    def validar_cnh(self, cnh):
        cnh_numeros = re.sub(r'\D', '', cnh)
        return len(cnh_numeros) == 11

    def listar_veiculos(self):

        if not self.veiculos:
            print("Nenhum veículo cadastrado")
            return

        print("\nVeículos cadastrados:")
        for veiculo in self.veiculos:
            print(veiculo)
    
    def listar_clientes(self):
        for cliente in self.clientes:
            print(cliente)

    def realizar_aluguel(self):
        # Seleção do cliente
        cliente_cpf = input("Digite o CPF do cliente: ")
        cliente = next((c for c in self.clientes if c.cpf == self.formatar_cpf(cliente_cpf)), None)
        if not cliente:
            print("Cliente não encontrado.")
            return

        # Seleção do veículo
        placa_veiculo = input("Digite a placa do veículo que deseja alugar: ").upper()
        veiculo = next((v for v in self.veiculos if v.placa == placa_veiculo and v.status == "Disponível"), None)
        if not veiculo:
            print("Veículo não encontrado ou indisponível.")
            return

        while True:
            data_retirada_str = input("Digite a data de retirada (formato: DD/MM/AAAA): ")
            try:
                data_retirada = datetime.strptime(data_retirada_str, "%d/%m/%Y")
                data_atual = datetime.now()
                if data_retirada < data_atual:
                    print("A data de retirada não pode ser anterior ao dia de hoje. Tente novamente.")
                    continue
                break
            except ValueError:
                print("Data de retirada inválida. Use o formato DD/MM/AAAA. Tente novamente.")

        dias_aluguel = int(input("Digite a quantidade de dias para o aluguel: "))
        valor_total = veiculo.calcular_preco_aluguel(dias_aluguel)
        km_inicial = int(input("Digite a quilometragem inicial: "))

        aluguel = Aluguel(cliente, veiculo, data_retirada, dias_aluguel, km_inicial)
        self.alugueis.append(aluguel)
        cliente.adicionar_historico(aluguel)
        veiculo.status = "Indisponível"

        print(f"\nAluguel realizado com sucesso!\n{aluguel}")

    def atualizar_status_veiculos(self):
        data_atual = datetime.now()
        for aluguel in self.alugueis:
            if aluguel.veiculo.status == "Indisponível" and aluguel.data_devolucao <= data_atual:
                aluguel.veiculo.status = "Disponível"

    def devolver_veiculo(self):
        cliente_cpf = input("Digite o CPF do cliente: ")
        cliente = next((c for c in self.clientes if c.cpf == self.formatar_cpf(cliente_cpf)), None)
        if not cliente:
            print("Cliente não encontrado.")
            return

        # Seleciona o veículo pelo histórico de aluguel do cliente
        for idx, aluguel in enumerate(cliente.historico):
            print(f"{idx + 1}. Veículo: {aluguel.veiculo.modelo} | Data Retirada: {aluguel.data_retirada.date()} | Devolução Prevista: {aluguel.data_devolucao.date()}")
        
        aluguel_idx = int(input("Selecione o número do aluguel a ser devolvido: ")) - 1
        aluguel = cliente.historico[aluguel_idx]

        if aluguel.km_final is not None:
            print("Este veículo já foi devolvido.")
            return

        km_final = int(input("Digite a quilometragem final do veículo: "))
        if km_final < aluguel.km_inicial:
            print("Erro: A quilometragem final não pode ser menor que a quilometragem inicial.")
            return
        dias_atraso = int(input("Digite quantos dias de atraso houve (0 se não houve atraso): "))
        danos = input("O veículo sofreu danos? (s/n): ").lower() == 's'

        aluguel.devolver_veiculo(km_final, dias_atraso, danos)

    def historico_cliente(self):
        cliente_cpf = input("Digite o CPF do cliente: ")
        cliente = next((c for c in self.clientes if c.cpf == self.formatar_cpf(cliente_cpf)), None)
        
        if not cliente:
            print("Cliente não encontrado.")
            return

        if not cliente.historico:
            print(f"O cliente {cliente.nome} não tem aluguéis registrados.")
            return

        print(f"\nHistórico de aluguéis do cliente {cliente.nome}:")
        for idx, aluguel in enumerate(cliente.historico):
            devolvido = "Sim" if aluguel.km_final is not None else "Não"
            print(f"{idx + 1}. Veículo: {aluguel.veiculo.modelo} Placa: {aluguel.veiculo.placa}| Data Retirada: {aluguel.data_retirada.date()} | Devolução: {aluguel.data_devolucao.date()} | Devolvido: {devolvido} | Valor Total: R${aluguel.valor_total:.2f}")

        print("\nFim do histórico.")

    def relatorio_receita(self):
        print("\nEscolha uma opção:")
        print("1. Receita Total")
        print("2. Receita Mensal")
        opcao = input("Digite o número da opção: ")

        if opcao == '1':
            if not self.alugueis:
                print("Nenhum aluguel foi registrado até o momento.")
                return

            receita_total = 0
            print("\nRelatório de Receita Total:")
            for aluguel in self.alugueis:
                receita_total += aluguel.valor_total
                print(f"\nCliente: {aluguel.cliente.nome} | Veículo: {aluguel.veiculo.modelo} | Data Retirada: {aluguel.data_retirada.date()} | Data devolução: {aluguel.data_devolucao.date()} Valor Total: R${aluguel.valor_total:.2f}")
            
            print(f"\nReceita total gerada: R$ {receita_total:.2f}")

        elif opcao == '2':
            mes = int(input("Digite o mês (1-12): "))
            ano = int(input("Digite o ano (AAAA): "))
            receita_mensal = 0
            alugueis_mensais = [aluguel for aluguel in self.alugueis if aluguel.data_retirada.month == mes and aluguel.data_retirada.year == ano]

            if not alugueis_mensais:
                print(f"Nenhum aluguel foi registrado no mês {mes}/{ano}.")
                return

            print(f"\nRelatório de Receita do Mês {mes}/{ano}:")
            for aluguel in alugueis_mensais:
                receita_mensal += aluguel.valor_total
                print(f"\nCliente: {aluguel.cliente.nome} | Veículo: {aluguel.veiculo.modelo} | Data Retirada: {aluguel.data_retirada.date()} | Data devolução: {aluguel.data_devolucao.date()} Valor Total: R${aluguel.valor_total:.2f}")

            print(f"\nReceita do mês {mes}/{ano}: R$ {receita_mensal:.2f}")

        else:
            print("Opção inválida.")

def main():
    sistema = SistemaAluguel()

    while True:
        print("\nMenu de Opções:")
        print("1. Cadastrar Veículo")
        print("2. Cadastrar Cliente")
        print("3. Realizar Aluguel")
        print("4. Devolver Veículo")
        print("5. Histórico de alugueis")
        print("6. Consultar Frota")
        print("7. Gerar Relatório de Receita")
        print("8. Sair")
        
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            # Cadastro de veículos
            while True:
                placa = input("Digite a placa do veículo: ")
                if sistema.validar_placa(placa):
                    break
                else:
                    print("Placa inválida.")
            marca = input("Digite a marca do veículo: ")
            modelo = input("Digite o modelo do veículo: ")
            ano = int(input("Digite o ano de fabricação do veículo: "))
            diaria = float(input("Digite o valor da diária do veículo: "))
            sistema.cadastro_veiculo(placa, modelo, marca, ano, diaria)

        elif opcao == '2':
            # Cadastro de clientes
            nome = input("Digite o nome do cliente: ")
            while True:
                cpf = input("Digite o CPF do cliente: ")
                if sistema.validar_cpf(cpf):
                    break
                else:
                    print("CPF inválido!")
            while True:
                telefone = input("Digite o telefone do cliente (formato (DDD) 9xxxx-xxxx ou apenas números): ")
                if sistema.validar_telefone(telefone):
                    break
                else:
                    print("Telefone inválido! O telefone deve seguir o formato (DDD)9XXXX-XXXX.")
            while True:
                email = input("Digite o e-mail do cliente: ")
                if sistema.validar_email(email):
                    break
                else:
                    print("E-mail inválido! Siga o formato usuario@dominio.com.")
            while True:
                cnh = input("Digite o número da CNH do cliente (11 dígitos): ")
                if sistema.validar_cnh(cnh):
                    break
                else:
                    print("CNH inválida! A CNH deve conter 11 dígitos.")
            sistema.cadastro_cliente(nome, cpf, telefone, email, cnh)

        elif opcao == '3':
            sistema.realizar_aluguel()

        elif opcao == '4':
            sistema.devolver_veiculo()

        elif opcao == '5':
            sistema.historico_cliente()

        elif opcao == '6':
            sistema.listar_veiculos()

        elif opcao == '7':
            sistema.relatorio_receita()

        elif opcao == '8':
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()