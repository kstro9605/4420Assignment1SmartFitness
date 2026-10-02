class Participant:
    def __init__(self, profile):
        self.participant_id = profile["participant_id"]
        self.name = profile["name"]
        self.baseline_heart_rate = int(profile["baseline_heart_rate"])
        self.baseline_skin_response = float(profile["baseline_skin_response"])
        self.baseline_temperature = float(profile["baseline_temperature"])
        self.sessions = dict()

    def get_number_of_sessions(self):
        return len(self.sessions)

    def add_session(self, session):
        self.sessions[session.session_id] = session

    def get_session(self, id):
        return self.sessions.get(id)

    def __repr__(self):
        return f"Participant (participant_id={self.participant_id}, baseline_heart_rate={self.baseline_heart_rate}, baseline_skin_response={self.baseline_skin_response}, baseline_temperature={self.baseline_temperature}, sessions={self.sessions})"