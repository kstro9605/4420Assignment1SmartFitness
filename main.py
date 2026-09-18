
from data_generator import available_scenarios, generate_fitness_data
from participant import Participant
from observation import Observation
from session import Session, QualityError
from sample_data import *
from analyzer import Analyzer
#from plot_heart_rate import plot_heart_rate


def main():
    participant_name = input("Please Enter your name: ")

    while True:
        user_input = input("Please enter the duration of your workout in whole minutes: ")
        try:
            duration = int(user_input)
            if duration > 0:
                break 
            print("Error: Excercise must last at least 1 minute for sensor data to be collected")
        except ValueError:
            print("Error: Please enter a valid duration.")

    print("For assignment assesment we generate sample data following different classifications: Resting, Moderate Activity, High Activity, Recovery, and Poor Quality/Invalid data")
    session_type = input("Please select a session classification (resting, moderate, high, recovery, or poor): ").lower()
    print(f"Generating data for sessions. Here are reports of invalid data: ")
    try:
        match session_type:
            case "resting":
                participant = generate_valid_resting_participant_data(participant_name, duration)
            case "moderate":
                participant = generate_valid_moderate_participant_data(participant_name, duration)
            case "high":
                participant = generate_valid_high_participant_data(participant_name, duration)
            case "recovery":
                participant = generate_valid_recovery_participant_data(participant_name, duration)
            case "poor":
                participant = generate_valid_poor_participant_data(participant_name, duration)
                raise QualityError(f"Quality of session data is not valid and will not be analyzed.")
            case _:
                raise ValueError(f"Invalid Session Type: {session_type}")

        analyzer = Analyzer()
        analysis_results = analyzer.analyze_sessions(participant)
        analyzer.print_analysis_results(participant, analysis_results)

        #Logic for using matplotlib to plot heart rate and averages that is not allowed in this assignment
        #plot_heart_rate(participant)
    
    except ValueError as e:
        print(f"Validation error found {e}")
    except QualityError as e:
        print(f"Quality of data error: {e}")
            

if __name__ == "__main__":
    main()

