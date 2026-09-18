class Observation:
    __observation_status = []

    def __init__(self, observation_data):
        self.timestamp = observation_data["timestamp"]
        self.heart_rate = observation_data["heart_rate"]
        self.skin_response = observation_data["skin_response"]
        self.temperature = observation_data["temperature"]
        self.activity_level = observation_data["activity_level"]
        self.signal_quality = observation_data["signal_quality"]

    def validate(self):
        if self.heart_rate is not None and (self.heart_rate < 35 or self.heart_rate > 205):
            self.__observation_status.append("invalid heart rate")
            raise ValueError(f"Heart rate {self.heart_rate} is outside the expected range (35-205 bpm).")
        if self.skin_response is not None and self.skin_response < 0:
            self.__observation_status.append("invalid skin response")
            raise ValueError(f"Skin response {self.skin_response} cannot be negative.")
        if self.temperature is not None and (self.temperature < 25 or self.temperature > 42):
            self.__observation_status.append("invalid temperature")
            raise ValueError(f"Temperature {self.temperature} is outside the expected range (25-42 °C).")
        if self.activity_level is not None and (self.activity_level < 0 or self.activity_level > 1):
            self.__observation_status.append("invalid activity level")
            raise ValueError(f"Activity level {self.activity_level} is outside the expected range (0-1).")
        if self.signal_quality is not None and (self.signal_quality < 0 or self.signal_quality > 1):
            self.__observation_status.append("invalid signal quality")
            raise ValueError(f"Signal quality {self.signal_quality} is outside the expected range (0-1).")
        if self.signal_quality is not None and (self.signal_quality < .19):
            self.__observation_status.append("Signal quality too low for accuracy")
            raise ValueError(f"Signal quality {self.signal_quality} is below acceptable range.")
        if self.signal_quality == 0:
            self.__observation_status = "Unacceptable signal quality"
            raise ValueError("Signal quality is zero, indicating unacceptable data quality.")
    

    def __repr__(self):
        return f"Observation(timestamp={self.timestamp}, heart_rate={self.heart_rate}, skin_response={self.skin_response}, temperature={self.temperature}, activity_level={self.activity_level}, signal_quality={self.signal_quality})"
