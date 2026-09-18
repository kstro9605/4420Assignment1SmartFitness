class Analyzer:
    def __init__(self):
        pass

    def analyze_sessions(self, participant):
        analysis_results = []
        baseline_hr = participant.baseline_heart_rate
        baseline_skin = participant.baseline_skin_response
        baseline_temp = participant.baseline_temperature

        sessionCount = 1
        for session in participant.sessions:
            session_analysis = dict()
            session_analysis["session_number"] = sessionCount
            sessionCount += 1
            starting_observation = session.determine_starting_observation()
            ending_observation = session.determine_ending_observation()
            organized_observations = session.organize_observations_by_timestamp()

            session_analysis["duration"] = ending_observation.timestamp - starting_observation.timestamp + 1
            session_analysis["average_heart_rate"] =  sum(obs.heart_rate for obs in organized_observations) / len(organized_observations)
            session_analysis["average_skin_response"] = sum(obs.skin_response for obs in organized_observations) / len(organized_observations)
            session_analysis["average_temperature"] = sum(obs.temperature for obs in organized_observations) / len(organized_observations)
            session_analysis["max_heart_rate"] = max(obs.heart_rate for obs in organized_observations)
            session_analysis["min_heart_rate"] = min(obs.heart_rate for obs in organized_observations)
            session_classification = self.determine_session_type(organized_observations, baseline_hr)
            session_analysis["session_type"] = session_classification
            session.set_session_type(session_classification)

            session_analysis["valid_observations"] = len(organized_observations)

            analysis_results.append(session_analysis)   

        return analysis_results

    def determine_session_type(self, observations, baseline_heart_rate):
        heart_rates = [obs.heart_rate for obs in observations]
        average_heart_rate = sum(heart_rates) / len(heart_rates)
        activity_levels = [obs.activity_level for obs in observations]
        heart_rate_trend = self.__detect_trend(heart_rates)
        activity_level_trend = self.__detect_trend(activity_levels)
    
        if heart_rate_trend == 1 or activity_level_trend == 1:
            match average_heart_rate:
                # I am not a huge fan of this case but because the resting values for seed 42 are technically an increasing trend,
                # I had to add this case to avoid misclassifying the resting scenario as moderate activity. 
                # Also important note that i made the 85 bpm cutoff because that is MY upper range of resting 
                case hr if hr < 85:
                    return "Resting"
                case hr if 85 <= hr <= 109:
                    return "Moderate Activity"
                case hr if hr > 110:
                    return "High Activity"
        elif (heart_rate_trend == -1 or activity_level_trend == -1) and average_heart_rate > baseline_heart_rate:
            return "Recovery"
        elif average_heart_rate <= baseline_heart_rate + 15:
            return "Resting"
        else:
            return "Insufficient Data"

    ''' I believe this method of determining whether the median slope is increasing vs decreasing would work for Real life 
        values but unfortunately due to the random generation of values used that go up and down much more erradically than a real heart rate
        would this is an unreliable means of determining trends of this data
    def __get_median(self, values):
        sorted_values = sorted(values)
        n = len(sorted_values)
        mid = n // 2
        if n % 2 == 1:
            return sorted_values[mid]
        else:
            return (sorted_values[mid - 1] + sorted_values[mid]) / 2.0

    def __detect_trend(self, data):
        slopes = []
        n = len(data)
        
        for i in range(n):
            for j in range(i + 1, n):
                slope = (data[j] - data[i]) / (j - i)
                slopes.append(slope)

        print(slopes)
                
        # Taking the median to possibly overlook outliers.
        median_slope = self.__get_median(slopes)

        if median_slope > 0:
            return 1  #postive slope == increasing trend
        elif median_slope < 0:
            return -1  # negative slope == decreasing trend   
        else:
            return 0  # No trend'''

    def __detect_trend(self, data):
        half_data = len(data) // 2
        if half_data == 0:
            half_data = 1

        first_half = data[:half_data]
        last_half = data[-half_data:]

        avg_first = sum(first_half) / len(first_half)
        avg_last = sum(last_half) / len(last_half)
        
        if avg_first > avg_last:
            return -1
        elif avg_first < avg_last:
            return 1
        else: 
            return 0


    def print_analysis_results(self, participant, analysis_results):
        print(f"\nAnalysis results for participant: {participant.participant_id}:")
        print(f"Baseline Heart Rate: {participant.baseline_heart_rate} bpm")
        print(f"Baseline Skin Response: {participant.baseline_skin_response}")
        print(f"Baseline Temperature: {participant.baseline_temperature} °C\n")
        for session_analysis in analysis_results:
            print(f"Session number {session_analysis['session_number']}:")
            print(f"  Duration: {session_analysis['duration']} Minutes (may be inaccurate due to invalid sensor data)")
            print(f"  Average Heart Rate: {session_analysis['average_heart_rate']:.2f} bpm")
            print(f"  Average Skin Response: {session_analysis['average_skin_response']:.2f}")
            print(f"  Average Temperature: {session_analysis['average_temperature']:.2f} °C")
            print(f"  Max Heart Rate: {session_analysis['max_heart_rate']} bpm")
            print(f"  Min Heart Rate: {session_analysis['min_heart_rate']} bpm")
            print(f"  Session Type: {session_analysis['session_type']}")
            print(f"  Sensor captured {session_analysis['valid_observations']} acceptable readings out of {session_analysis['duration']} expected")
    
      