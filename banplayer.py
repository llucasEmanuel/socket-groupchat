import time

class BanStateMachine:
    def __init__(self, server):
        self.state = "IDLE"
        self.server = server
        self.ban_target = None
        self.yes_votes = 0
        self.no_votes = 0
        self.vote_deadline = None

    def request_ban(self, requester, target):
        if self.state != "IDLE" or getattr(self.server, "votacao_ativa", False):
            return "Another ban vote is already running."

        self.state = "VOTING"
        self.server.votacao_ativa = True
        self.ban_target = target
        self.yes_votes = 0
        self.no_votes = 0
        self.vote_deadline = time.time() + 60

        self.notify_all(f"Vote to ban {target} started by {requester}. Type YES or NO.")

    def receive_vote(self, vote):
        if self.state != "VOTING":
            return "No active vote."

        vote = vote.upper()
        if vote == "y":
            self.yes_votes += 1
        elif vote == "n":
            self.no_votes += 1

        # Calcula votos necessários no momento atual
        required_votes = (len(self.server.clientes) // 2) + 1

        self.notify_all(f"[ {self.ban_target} ] ban {self.yes_votes}/{required_votes}")

        if self.yes_votes >= required_votes or time.time() > self.vote_deadline:
            self.decide_ban()

    def decide_ban(self):
        required_votes = (len(self.server.clientes) // 2) + 1

        if self.yes_votes >= required_votes:
            self.server.banidos.append(self.ban_target)
            self.notify_all(f"{self.ban_target} has been banned.")
        else:
            self.notify_all(f"Ban for {self.ban_target} rejected.")

        self.reset()

    def reset(self):
        self.state = "IDLE"
        self.server.votacao_ativa = False
        self.ban_target = None
        self.yes_votes = 0
        self.no_votes = 0
        self.vote_deadline = None

    def notify_all(self, message):
        for cliente in self.server.clientes:
            cliente.send_message(message)
