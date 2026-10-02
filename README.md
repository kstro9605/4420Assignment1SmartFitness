# Smart Fitness Session Analyzer
Python Programming Assignment (II) Option A
Kyle Strother 
Student Number: 416279

## Description
A fitness centre receives simulated measurements from wearable devices used during training sessions. It needs a Python
program that organizes participants and exercise sessions, validates measurements, compares measurements with personal
reference values, classifies session intensity and describes recovery after activity.

The program package will accept command line arguments pointing towards Data files for both known participants, and session data. It will then validate the data and associate the session data to its related participant and run an analysis on each users session. This will display relevant statistics as well as categorize the session and provide an explanation why it was summarized as such. These analyses as well as explanations as to why any data may have been rejected will be output into user readable files that can be configured to point to a directory of the users choice.

## Project Structure
4420Assignment1SmartFitness/<br>
SmartFitness/<br>
├── data/<br>
│   ├── participants.csv<br>
│   └── fitness_sessions.csv<br>
├── src/<br>
│   └── smartfitness/<br>
│       ├── \_\_init\_\_.py<br>
│       ├── \_\_main\_\_.py<br>
│       ├── main.py<br>
│       ├── analyzer.py<br>
│       ├── fileGeneration.py<br>
│       ├── fileValidation.py<br>
│       ├── observation.py<br>
│       ├── participant.py<br>
│       └── session.py<br>
└── pyproject.toml<br>

-----------------------------------------------------------------------------------------------------------------------

### main.py
The main entry point for the application.<br>

Responsibilities:<br>
&emsp;Validate and pull in participants and session data files<br>
&emsp;Make calls to FileValidation methods to ensure valid data is imported.<br>
&emsp;Associates Session and Observation data with specific users.<br>
&emsp;Calls the analyzer<br>

The application is started by running `py -m smartfitness --profiles <profile data source> --sessions <session data source> [--output <desired output directory](<- this is optional and without it it will default to output) `<br>
Or `py -m smartfitness --profiles <profile data source> --sessions <session data source> [--output <desired output directory](<- this is optional and without it it will default to output) --overwrite`

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

### fileGeneration.py
This module is responsible for generation of output files.

Responsibilities:<br>
&emsp;Given an Analysis summart it will output it to a file, either appending it to an existing file or generating a new one<br>
&emsp;Generate a quick analysis line for csv format give an analysis summary dictionary<br>
&emsp;Prints full user readable reports to an output file for all participants, and their session(s)<br>
&emsp;Processes a participant's sessions.<br>
&emsp;Reports why certain imported data may not have been accepted and where it lives<br>

### fileValidation.py
This module is responsible for loading and validating participant and session data

Responsibilities:<br>
&emsp;Processes a participants data file and catergorizes the data into valid and invalid input.<br>
&emsp;Processes a Session data file and catergorizes the data into valid and invalid input.<br>
&emsp;Validates the rows of a participants CSV file and either passes the row or rejects it and provides explanation as to why.<br>
&emsp;Validates the rows of a session CSV file and either passes the row or rejects it and provides explanation as to why.<br>
&emsp;Creates two custom exception calsses to handle when a data file is invalid<br>

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
  1. The time stamp values is representative of minutes
  2. A session must last at least 1 minute with the understanding that the only sensor data collected could be faulty
  3. Heart Rate is measured in Beats per Minute (bpm)
  4. Lower value signal quality is less accurate
  5. the session and participant data is provided by the user and data trend provided are realistic other wise the algorithm utilized to determine trends will be uneffective

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
  - Insufficient Data
    - If the session data is incomplete and a session is only a single observation in length, it can not calculate trends effectively and classify the session

-----------------------------------------------------------------------------------------------------------------------

## Installation
PreRequisites: 
  - Python 3.10 or newer due to the usage of match case syntax
  - No third-party packages needed as the only reference to matplotlib is commented out

### Steps:
  1. Clone the repository:
    - run `git clone https://github.com/kstro9605/4420Assignment1SmartFitness.git` in a terminal with git installed
  2. Enter the Project Directory
    - run `cd 4420Assignment1SmartFitness` in the same terminal window
  3. Verify Python
    - run `python3 --version` and verify you are running 3.10 or later
  6. run `python3 -m pip install -e .`
  4. Run the Application
    - run `python3 -m smartfitness --profiles <profile data source> --sessions <session data source> [--output <desired output directory](<- this is optional and without it it will default to output)`
      - if You wish to overwrite all output already generated instead of appending (in the case of running the application with the same data files) append `--overwrite` to the above command
  5. View output files in either a new `output` directory or whatever directory specified in the above command
     
-----------------------------------------------------------------------------------------------------------------------

## Example Output

### Valid Data output 

<img width="1839" height="955" alt="image" src="https://github.com/user-attachments/assets/8301840a-7009-4d93-8965-aa4e8442fe0d" />

### Invalid data source output

<img width="1846" height="674" alt="image" src="https://github.com/user-attachments/assets/c6e9962d-70c1-41b7-ad41-3aa4619f9c06" />

### Rejected Records output

<img width="1049" height="827" alt="image" src="https://github.com/user-attachments/assets/84a6212f-76ca-4c7b-9fee-d267c9af0769" />

-----------------------------------------------------------------------------------------------------------------------

## Known Limitations
  1. At this time the program will only accept one set of session and participant data at once, to process multiple files the command must be run several times given new files.
  2. Output to files is generic text and lacks beneficial graphs depicting trends and deviation from baseline values
     
-----------------------------------------------------------------------------------------------------------------------
