# Smart Fitness Session Analyzer
Python Programming Assignment (I) Option A
Kyle Strother 
Student Number: 416279

## Description
A fitness centre receives simulated measurements from wearable devices used during training sessions. It needs a Python
program that organizes participants and exercise sessions, validates measurements, compares measurements with personal
reference values, classifies session intensity and describes recovery after activity.

The Program in this repository utilizes the instructor provided data generator to simulate measurements pertaining to:
  - Reading Time Stamp
  - Heart Rate
  - Skin Response
  - Skin Temperature
  - Activity Level
  - Sensor signal quality

The program will prompt the user for their name, the duration of the exercise session, and then ask what type of activity they want simulated.
Upon generation and placement into a *Observation* Object, the program will then validate this set to remove any unreliable data points and alert the user that a measurement has been removed from the set.
these sets are then compiled into a *Session* Object which is then passed to an *Analyzer* Object that parses intenal data into the following statistics:
  - Average Heart Rate
  - Average Skin Response
  - Average Temperature
  - Max Heart Rate
  - Min Heart Rate
  - Session Type
  - Data points validated over expected data points
  - Session designation explanation

## Project Structure
4420Assignment1SmartFitness/<br>
|-main.py<br>
|-analyzer.py<br>
|-data_generator.py <-Instructor provided class that can generate random seeded signal data <br>
|-observation.py<br>
|-participant.py<br>
|-sample_data.py<br>
|-session.py<br>
|-plot_heart_rate.py   <- This is not to be considered in assessment it is simply a tool to visualize data matplotlib<br>

-----------------------------------------------------------------------------------------------------------------------

### main.py
The main entry point for the application.<br>

Responsibilities:<br>
&emsp;Collects the participant's name, duration, and scenario.<br>
&emsp;Generates the appropriate sample data.<br>
&emsp;Creates the required domain objects.<br>
&emsp;Calls the analyzer<br>

The application is started by running `python3 ./main.py`<br>

### observation.py
The data object that is responsible for housing the generated data.<br>

Responsibilities:<br>
&emsp;Stores a timestamp<br>
&emsp;Stores Heart Rate<br>
&emsp;Stores skin response<br>
&emsp;Stores temperature<br>
&emsp;Stores activity level<br>
&emsp;Stores signal quality<br>
&emsp;Validates that sensor values fall within acceptable ranges<br>

### session.py
The data object that is responsible for organizing observations into a single session.<br>

Responsibilities:<br>
&emsp;Validates observations before they are accepted.<br>
&emsp;Maintains valid observations.<br>
&emsp;Rejects sessions containing too much invalid data.<br>
&emsp;Checks average sensor signal quality.<br>
&emsp;Determines the first and last observations.<br>
&emsp;Sorts observations by timestamp.<br>
&emsp;Stores the session classification.<br>
&emsp;Provides access to the session classification.<br>

This class also Raises a custom `QualityError` to represent poor-quality sensor data, inheriting from Pythons built-in `Exception` class

### participant.py
The object representing the user and the owner of the fitness data being analyzed. In this current implementation, this acts as a container for one or more `Session` objects<br>

Responsibilities:<br>
&emsp;Stores the participant ID/name.<br>
&emsp;Stores baseline heart rate.<br>
&emsp;Stores baseline skin response.<br>
&emsp;Stores baseline temperature.<br>
&emsp;Maintains the participant's collection of workout sessions.<br>
&emsp;Provides add_session() for adding a session for future development needs<br>

### analyzer.py
This class is primarily responsible for performing the fitness session data analysis

Responsibilities:<br>
&emsp;Processes a participant's sessions.<br>
&emsp;Calculates session duration<br>
&emsp;calculates average Heart rate<br>
&emsp;Calculates Average Skin Response<br>
&emsp;Calculates Average Temperature<br>
&emsp;Finds maximum and minimum heart rate.<br>
&emsp;Detects heart-rate and activity-level trends.<br>
&emsp;Classifies the session.<br>
&emsp;Generates an explanation for the classification<br>
&emsp;Prints the analysis results.<br>

### sample_data.py
This module provides helper functions for the different required assessment scenarios

Examples:<br>
&emsp;`generate_valid_resting_participant_data()`<br>
&emsp;`generate_valid_recovery_participant_data()`<br>
&emsp;`generate_valid_moderate_participant_data()`<br>
&emsp;`generate_valid_high_participant_data()`<br>
&emsp;`generate_poor_participant_data()`<br>

These functions are created to ease assessment of this assignment

-----------------------------------------------------------------------------------------------------------------------

### Composition
Composition can be observed in the relationship between Observation, Session, and Participant Objects. 
A `Participant` contains a collection of `Session` Objects, which are in turn a collection of `Observation` Objects
This is a clear representation a 'Has-a' relationship.

### Encapsulation
Encapsulation can be seen in this program in the `Session` class's use of the private attribute `__classification`.
The reasoning behind this encapsulation of this specific attribute is that we determine its classification utilizing 
other data points and do not want to afford the user the ability to set it's classification to anything other than what it should be based on values

### Inheritance 
Inheritance can be seen with the use of the custom `QualityError` exception. 
`QualityError` inherits the functionality of Python's built-in Exception class while providing a specific exception type for poor-quality fitness-session data.
for ease of differentiating errors based on bad values and poor values

### Method Overriding 
Method Overriding can be seen in the use of the __repr__() method implemented in the `Observation`, `Session`, and `Participant` classes 
These allowed me to implement my own behavior for the string representation that is built in the Python's base Object class

-----------------------------------------------------------------------------------------------------------------------

## Assumptions
The Program makes the following assumptions:
  1. The time stamp values generated by instructor provided code is representative of minutes
  2. A session must last at least 1 minute with the understanding that the only sensor data collected could be faulty
  3. Heart Rate is measured in Beats per Minute (bpm)
  4. Lower value signal quality is less accurate
  5. the sample data is set to use fixed seeded random generators for testing purposes
  6. a Participant must enter a name
  7. At this point there are only 5 scenarios (Resting, Moderate, High, Recovery, and Poor)

-----------------------------------------------------------------------------------------------------------------------

## Classification Rules
This Program uses the following rules to determine a sessions classification:
  - Resting:
    - The participants heart rate is below 85 BPM OR
      if there is no clear heart rate/ activity level trend and the heart rate average is within 15 bpm of the users base line
  - Moderate:
    - The Average heart rate is measured between 85 and 109(inclusively) bpm
  - High:
    - The average Heart rate is measured above 110 bpm
  - Recovery:
    - The heart rate/ activity level trend must be decreasing and the average heart rate is approaching the participant's baseline
  - Poor Quality:
    - If sensor values fall outside of accepted ranges or if the signal quality is below .19 causing more than 20% of the
      session's observations to be invalid. Once a Poor scenario is reached in the main application it does not proceed with analysis.

-----------------------------------------------------------------------------------------------------------------------

## Installation
PreRequisites: 
  - Python 3.10 or newer due to the usage of match case syntax
  - No third-party packages needed as the only reference to matplotlib is commented out

### Steps:
  1. Clone the repository:
    - run `git clone https://github.com/kstro9605/4420Assignment1SmartFitne` in a terminal with git installed
  2. Enter the Project Directory
    - run `cd 4420Assignment1SmartFitness` in the same terminal window
  3. Verify Python
    - run `python3 --version` and verify you are running 3.10 or later
  4. Run the Application
    - run either `python3 main.py` or `python main.py`
  5. Follow the prompts given by the program
     
-----------------------------------------------------------------------------------------------------------------------

## Example Output

<img width="1523" height="526" alt="image" src="https://github.com/user-attachments/assets/4c432374-ab94-4666-a0a0-53c3bbd3de40" />

-----------------------------------------------------------------------------------------------------------------------

## Known Limitations
  1. Due to the nature of the sensor data being randomly generated it is not indicative of real heart rate values and as such making a determination of the trend of the heart rate is very generic
     and could lead to misclassification if random data points bounce around too much
  2. I have increased the range that sensor signal quality can be generated at and as such the duration cam be off by a minute or two for longer session durations
     
-----------------------------------------------------------------------------------------------------------------------
