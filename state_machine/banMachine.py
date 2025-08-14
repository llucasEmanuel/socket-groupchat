import time
from threading import Timer

class BanStateMachine:
    def __init__(self, server):
        self.state = "IDLE"
        self.server = server
        self.ban_target = None
        self.votes = {}  # Dicionário {username: 'y'/'n'}
        self.vote_timer = None
        self.required_votes_at_start = 0
        
    def request_ban(self, target):
        # Verifica se já existe uma votação ativa
        if self.state != "IDLE":
            return "Uma votação de banimento já está em andamento."
        
        # Verifica se o usuário existe no servidor
        target_exists = any(client.username == target for client in self.server.client_list)
        if not target_exists:
            return f"Usuário '{target}' não encontrado no servidor."
        
        # Inicia nova votação
        self.state = "VOTING"
        self.ban_target = target
        self.votes = {}
        
        # Calcula votos necessários no momento do início da votação
        total_clients = len(self.server.client_list)
        self.required_votes_at_start = (total_clients // 2) + 1
        
        # Inicia timer de 60 segundos
        self.vote_timer = Timer(60.0, self._timeout_vote)
        self.vote_timer.start()
        
        # Notifica todos sobre o início da votação
        message = f"[Server] Votação iniciada para banir '{target}'. Digite /vote y ou /vote n. Tempo: 60 segundos."
        self.server.broadcast_message(f"8-{message}")
        
        # Envia status inicial da votação
        self._send_vote_status()
        
        return f"Votação para banir '{target}' iniciada."
    
    def receive_vote(self, voter_username, vote):
        if self.state != "VOTING":
            return "Nenhuma votação ativa no momento."
        
        vote = vote.lower()
        if vote not in ['y', 'n']:
            return "Voto inválido. Use /vote y ou /vote n."
        
        # Registra/atualiza o voto do usuário
        self.votes[voter_username] = vote
        
        # Envia status atualizado para todos
        self._send_vote_status()
        
        # Verifica se a votação deve terminar
        self._check_vote_completion()
        
        return f"Voto registrado: {vote}"
    
    def _send_vote_status(self):
        # Conta votos sim
        yes_votes = sum(1 for vote in self.votes.values() if vote == 'y')
        
        # Calcula votos necessários baseado no número atual de clientes
        current_clients = len(self.server.client_list)
        required_votes = (current_clients // 2) + 1
        
        # Envia mensagem de status para todos
        status_message = f"**[ {self.ban_target} ] ban {yes_votes}/{required_votes}**"
        self.server.broadcast_message(f"8-{status_message}")
    
    def _check_vote_completion(self):
        yes_votes = sum(1 for vote in self.votes.values() if vote == 'y')
        current_clients = len(self.server.client_list)
        required_votes = (current_clients // 2) + 1
        
        # Se atingiu os votos necessários, bane imediatamente
        if yes_votes >= required_votes:
            self._execute_ban()
    
    def _timeout_vote(self):
        """Chamada quando o timer de 60 segundos expira"""
        if self.state == "VOTING":
            yes_votes = sum(1 for vote in self.votes.values() if vote == 'y')
            current_clients = len(self.server.client_list)
            required_votes = (current_clients // 2) + 1
            
            if yes_votes >= required_votes:
                self._execute_ban()
            else:
                self._reject_ban()
    
    def _execute_ban(self):
        """Executa o banimento do usuário"""
        # Adiciona à lista de banidos
        banned_client = next((client for client in self.server.client_list if client.username == self.ban_target), None)
        if banned_client:
            self.server.ban_list.append(banned_client)
        
        # Remove da lista de clientes ativos
        is_for_all, message = self.server.remove_client(self.ban_target, ban_on=True)
        
        # Notifica todos sobre o banimento
        ban_message = f"[Server] '{self.ban_target}' foi banido do chat."
        self.server.broadcast_message(f"8-{ban_message}")
        
        self._reset_voting()
    
    def _reject_ban(self):
        """Rejeita o banimento por falta de votos ou timeout"""
        reject_message = f"[Server] Votação para banir '{self.ban_target}' foi rejeitada."
        self.server.broadcast_message(f"8-{reject_message}")
        
        self._reset_voting()
    
    def _reset_voting(self):
        """Reseta o estado da máquina de votação"""
        if self.vote_timer:
            self.vote_timer.cancel()
        
        self.state = "IDLE"
        self.ban_target = None
        self.votes = {}
        self.vote_timer = None
        self.required_votes_at_start = 0
    
    def handle_client_disconnect(self, username):
        """Atualiza a votação quando um cliente se desconecta"""
        if self.state == "VOTING":
            # Remove o voto do cliente que saiu (se havia votado)
            if username in self.votes:
                del self.votes[username]
            
            # Se o usuário sendo votado saiu, cancela a votação
            if username == self.ban_target:
                cancel_message = f"[Server] Votação cancelada - '{username}' saiu do chat."
                self.server.broadcast_message(f"8-{cancel_message}")
                self._reset_voting()
                return
            
            # Atualiza o status da votação com o novo número de clientes
            self._send_vote_status()
            
            # Verifica se ainda é possível completar a votação
            self._check_vote_completion()
    
    def handle_client_connect(self):
        """Atualiza a votação quando um novo cliente se conecta"""
        if self.state == "VOTING":
            # Apenas atualiza o status da votação com o novo número de clientes
            self._send_vote_status()
            
            # Informa o novo cliente sobre a votação em andamento
            welcome_vote_msg = f"[Server] Votação em andamento para banir '{self.ban_target}'. Digite /vote y ou /vote n."
            # Aqui você pode implementar uma mensagem específica para o novo cliente
            # Por simplicidade, será enviado no broadcast normal