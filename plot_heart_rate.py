import matplotlib.pyplot as plt
from participant import Participant

def plot_heart_rate(participant):
    base_heart_rate = participant.baseline_heart_rate
    plt.axhline(y=base_heart_rate, color='g', linestyle='--', label='Baseline Heart Rate')
    for session in participant.sessions:
        session_type = session.get_session_type()
        organized_observations = session.organize_observations_by_timestamp()
        heart_rates= []
        time_stamps = []
        for obs in organized_observations:
            heart_rates.append(obs.heart_rate)
            time_stamps.append(obs.timestamp)
        plt.plot(time_stamps, heart_rates)

        match session_type:
            case "Resting":
                plt.axhline(y=base_heart_rate - 20, color='r', linestyle='--', label='Min Resting')
                plt.axhline(y=base_heart_rate + 20, color='r', linestyle='--', label='Max Resting')
            case "Moderate Activity":
                plt.axhline(y=85, color='r', linestyle='--', label='Min Moderate')
                plt.axhline(y=109, color='r', linestyle='--', label='Max Moderate')
            case "High Activity":
                plt.axhline(y=110, color='r', linestyle='--', label='Min High Activity')
                plt.axhline(y=180, color='r', linestyle='--', label='Max High Activity')
            case "Recovery":
                plt.axhline(y=base_heart_rate - 20, color='r', linestyle='--', label='Min Expected')
                plt.axhline(y=180, color='r', linestyle='--', label='Max Expected')

        plt.title("Heart Rate over session")
        plt.xlabel("TimeStamp")
        plt.ylabel("Heart Rate (bpm)")
        plt.legend()

        plt.show()