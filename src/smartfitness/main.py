
import argparse
import os
import shutil

from .observation import Observation
from .session import Session
from .analyzer import Analyzer
from .fileValidation import loadUsers, loadSessions, UserFileValidationError, SessionFileValidationError
from .fileGeneration import write_analysis_to_file, print_analysis_results,invalid_users_file_explanation, invalid_sessions_file_explanation


def main():
    parser = argparse.ArgumentParser(description="Analyze fitness session data.")
    parser.add_argument("--profiles", required=True, help="Path to the participants CSV")
    parser.add_argument("--sessions", required=True, help="Path to the fitness sessions CSV")
    parser.add_argument("--output", default="output", help="Directory for the analysis report")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing output files")
    args = parser.parse_args()

    if args.overwrite:
        if os.path.exists(args.output):
            shutil.rmtree(args.output)
    try:
        validUsers, invalidUsers = loadUsers(args.profiles)
        validUserIds = validUsers.keys()
        validSessions, invalidSessions = loadSessions(args.sessions, validUserIds)

        if len(invalidUsers) > 0:
            invalid_users_file_explanation(args.output, args.profiles, invalidUsers)
        if len(invalidSessions) > 0:
            invalid_sessions_file_explanation(args.output, args.sessions, invalidSessions)

        for obs in validSessions:
            obs_participant = obs["participant_id"]
            obs_session_id = obs["session_id"]
            observation = Observation(obs)
            participant = validUsers[obs_participant]
            
            targeted_session = participant.get_session(obs_session_id)

            if targeted_session is None:
                newSession = Session([observation], obs_session_id)
                participant.add_session(newSession)
            else:
                pass
                targeted_session.add_observation(observation)

        analyzer = Analyzer()

        for user in validUsers.values():
            analysis_results = analyzer.analyze_sessions(user)
            for session_analysis in analysis_results:
                write_analysis_to_file(args.output, session_analysis)
                print_analysis_results(args.output, analyzer, user, analysis_results)
    except (UserFileValidationError, SessionFileValidationError) as e:
        print(f"Error importing data: {e}")

if __name__ == "__main__":
    main()

