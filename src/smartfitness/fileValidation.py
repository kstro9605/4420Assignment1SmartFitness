import csv
import re
from .participant import Participant

def isValidParticipantRow(row):
    if row.__len__() != 5:
        return False, "invalid number of columns"

    validity = True
    explanation = ""

    if "participant_id" in row:
        id = row['participant_id']
        if not re.fullmatch("^P\\d{3}$", id):
            validity = False 
            explanation += f"Participant ID : {id} is invalid "
    else:
        validity = False 
        explanation += "No Participant ID given "

    if "name" not in row:
        validity= False 
        explanation += "No Name given"

    if "baseline_heart_rate" in row:
        #this will make validation in my observation class redundant but that is fine
        try:
            heart_rate =  int(row['baseline_heart_rate'])
            if heart_rate < 35 or heart_rate > 205:
                validity = False 
                explanation += f"Invalid Baseline Heart Rate Value: {heart_rate} "
        except ValueError:
            validity = False 
            explanation += f"Non-numeric Baseline Heart Rate Value: {row['baseline_heart_rate']} "
    else:
        validity= False 
        explanation += "No Baseline Heart Rate given "
    if "baseline_skin_response" in row:
        try:
            skin_response =  float(row['baseline_skin_response'])
            if skin_response < 0:
                validity= False 
                explanation += f"Invalid Baseline Skin Response Value: {skin_response} "
        except ValueError:
            validity = False 
            explanation += f"Non-numeric Baseline Skin Response Value: {row['baseline_skin_response']} "
    else:
        validity= False 
        explanation += "No Baseline Skin Response given "
    if "baseline_temperature" in row:
        try:
            skin_temperature = float(row['baseline_temperature'])
            if skin_temperature < 25 or skin_temperature > 42:
                validity= False 
                explanation += f"Invalid Baseline Skin Temperature Value: {skin_temperature} "
        except ValueError:
            validity= False 
            explanation += f"Non-numeric Baseline Skin Temperature Value: {row['baseline_temperature']} "
    else:
        validity= False 
        explanation += "No Baseline Skin Temperature given "
    return validity, explanation

def isValidSessionRow(row, valid_user_ids):
    if row.__len__() != 8:
        return False, "invalid number of columns"

    validity = True
    explanation = ""

    if "session_id" in row:
        id = row["session_id"]
        if not re.fullmatch("^FIT-\\d{4}-\\d{3}$", id):
            validity = False
            explanation += f"Session ID {id} invalid "
    else:
        validity = False
        explanation += "No Session ID given "
    if "participant_id" in row:
        id = row['participant_id']
        if re.fullmatch("^P\\d{3}$", id):
            if id not in valid_user_ids:
                validity = False
                explanation += f"Participant ID {id} for Session not a valid user "
        else:
            validity = False 
            explanation += f"Participant ID : {id} is invalid "
    else:
        validity = False 
        explanation += "No Participant ID given "
    if "timestamp" in row:
        try: 
            timestamp = int(row['timestamp'])
            if timestamp < 0:
                validity= False 
                explanation += f"Timestamp {timestamp} is invalid"
        except ValueError:
            validity = False
            explanation += f"Non-numeric Value for timestamp {row['timestamp']}"
    else:
        validity = False
        explanation += "No Timestamp given "
    if "heart_rate" in row:
        #this will make validation in my observation class redundant but that is fine
        try:
            heart_rate =  int(row['heart_rate'])
            if heart_rate < 35 or heart_rate > 205:
                validity = False 
                explanation += f"Invalid Heart Rate Value: {heart_rate}"
        except ValueError:
            validity = False 
            explanation += f"Non-numeric Heart Rate Value: {row['heart_rate']}"
    else:
        validity= False 
        explanation += "No Heart Rate given "
    if "skin_response" in row:
        try:
            skin_response =  float(row['skin_response'])
            if skin_response < 0:
                validity= False 
                explanation += f"Invalid Skin Response Value: {skin_response}"
        except ValueError:
            validity = False 
            explanation += f"Non-numeric Skin Response Value: {row['skin_response']}"
    else:
        validity= False 
        explanation += "No Skin Response given "
    if "temperature" in row:
        try:
            skin_temperature = float(row['temperature'])
            if skin_temperature < 25 or skin_temperature > 42:
                validity= False 
                explanation += f"Invalid Temperature Value: {skin_temperature}"
        except ValueError:
            validity= False 
            explanation += f"Non-numeric Temperature Value: {row['temperature']}"
    else:
        validity= False 
        explanation += "No Temperature given "
    if "activity_level" in row:
        try:
            activity_level =  float(row['activity_level'])
            if activity_level < 0 or activity_level > 1:
                validity= False 
                explanation += f"Invalid Activity Level Value: {activity_level}"
        except ValueError:
            validity = False 
            explanation += f"Non-numeric Activity Level Value: {row['activity_level']}"
    else:
        validity= False 
        explanation += "No Activity Level given "
    if "signal_quality" in row:
        try:
            signal_quality =  float(row['signal_quality'])
            if signal_quality < 0 or signal_quality > 1:
                validity= False 
                explanation += f"Invalid Signal Quality Value: {signal_quality}"
        except ValueError:
            validity = False 
            explanation += f"Non-numeric Signal Quality Value: {row['signal_quality']}"
        except TypeError:
            validity = False 
            explanation += f"Non-numeric Signal Quality Value: {row['signal_quality']}"
    else:
        validity= False 
        explanation += "No Signal Quality given "
    return validity, explanation

def loadUsers(file):
    validUsers= dict()
    invalidUsers=dict()

    try:
        with open(file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                isValid, explanation = isValidParticipantRow(row)
                if not isValid:
                    invalidUsers[row]=explanation
                else:
                    user = Participant(row)
                    validUsers[user.participant_id] = user

        return validUsers, invalidUsers
    except FileNotFoundError:
        raise UserFileValidationError(f"User file '{file}' not found.")

def loadSessions(file, validUserIds):
    validSessions = []
    invalidSessions = dict()

    try:
        with open(file, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            rowNumber = 0
            for row in csv_reader:
                rowNumber += 1
                isValid, explanation = isValidSessionRow(row, validUserIds)
                if not isValid:
                    invalidSessions[rowNumber] = explanation
                else: 
                    validSessions.append(row)

        return validSessions, invalidSessions
    except FileNotFoundError:
        raise SessionFileValidationError(f"Session file '{file}' not found.")

class UserFileValidationError(FileNotFoundError):
    pass
class SessionFileValidationError(FileNotFoundError):
    pass