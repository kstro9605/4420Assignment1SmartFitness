from observation import Observation

class Session:
    observations = []
    __classification = "invalid"
    def __init__(self, observations):
        number_of_observations = len(observations)
        valid_observations = []
        
        for observation in observations:
            try:
                Observation.validate(observation)
                valid_observations.append(observation)
            except ValueError as e:
                print(f"Error validating observation: {e}")
        if len(valid_observations) / number_of_observations < 0.2:
            raise ValueError("More than 20% of observations are invalid. Session may be unreliable.")
        average_signal_quality = sum(obs.signal_quality for obs in valid_observations) / len(valid_observations)
        if average_signal_quality < 0.2:
            raise QualityError("Average signal quality is below 0.2, indicating poor data quality.")
        self.observations.extend(valid_observations)

    def add_observation(self, observation):
        try:    
            Observation.validate(observation)
            self.observations.append(observation)
        except ValueError as e:
            raise ValueError(f"Error adding observation: {e}")

    def determine_starting_observation(self):
        if not self.observations:
            return None
        return min(self.observations, key=lambda obs: obs.timestamp)

    def determine_ending_observation(self):
        if not self.observations:
            return None
        return max(self.observations, key=lambda obs: obs.timestamp)  

    def organize_observations_by_timestamp(self):
        return sorted(self.observations, key=lambda obs: obs.timestamp)     

    def set_session_type(self, session_type):
        self.__classification = session_type       

    def get_session_type(self):
            return self.__classification     
            
    def __repr__(self):
        return f"Session(observations={self.observations})"

class QualityError(Exception):
    pass