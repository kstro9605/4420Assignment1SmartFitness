from data_generator import generate_fitness_data
from session import Session
from observation import Observation
from participant import Participant

def generate_valid_resting_participant_data(participant_name, session_length):
    participant = associate_participant_observations( *generate_fitness_data(
            participant_id=participant_name,
            scenario="resting",
            seed=42,
            number_of_windows=session_length,
        ))
    
    return participant

def generate_valid_recovery_participant_data(participant_name, session_length):
    participant = associate_participant_observations( *generate_fitness_data(
            participant_id=participant_name,
            scenario="recovery",
            seed=42,
            number_of_windows=session_length,
        ))

    return participant

def generate_valid_moderate_participant_data(participant_name, session_length):
    participant = associate_participant_observations( *generate_fitness_data(
            participant_id=participant_name,
            scenario="moderate_activity",
            seed=42,
            number_of_windows=session_length,
        ))

    return participant

def generate_valid_high_participant_data(participant_name, session_length):
    participant = associate_participant_observations( *generate_fitness_data(
            participant_id=participant_name, 
            scenario="high_activity",
            seed=42,
            number_of_windows=session_length,
        ))

    return participant

def generate_valid_poor_participant_data(participant_name, session_length):
    participant = associate_participant_observations( *generate_fitness_data(
            participant_id=participant_name,
            scenario="poor_quality",
            seed=42,
            number_of_windows=session_length,
        ))

    return participant

def associate_participant_observations(profile, observations):
    participant = Participant(profile)
    observations = [Observation(obs) for obs in observations]
        
    session = Session(observations)
    participant.add_session(session) 

    return participant