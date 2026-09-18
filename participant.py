class Participant:
    def __init__(self, profile):
        self.participant_id = profile["participant_id"]
        self.baseline_heart_rate = profile["baseline_heart_rate"]
        self.baseline_skin_response = profile["baseline_skin_response"]
        self.baseline_temperature = profile["baseline_temperature"]
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def __repr__(self):
        return f"Participant (participant_id={self.participant_id}, baseline_heart_rate={self.baseline_heart_rate}, baseline_skin_response={self.baseline_skin_response}, baseline_temperature={self.baseline_temperature}, sessions={self.sessions})"