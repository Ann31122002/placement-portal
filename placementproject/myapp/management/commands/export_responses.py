# export_responses.py
import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from myapp.models import UserResponse
from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials

class Command(BaseCommand):
    help = 'Export user responses to CSV + AUTO UPDATE GOOGLE SHEETS'

    def add_arguments(self, parser):
        parser.add_argument('--format', type=str, default='both', 
                          choices=['csv', 'sheets', 'both'],
                          help='Output format')

    def handle(self, *args, **kwargs):
        format_type = kwargs['format']
        
        # FETCH ALL RESPONSES
        responses = UserResponse.objects.all().select_related(
            'user', 'question', 'question__quiz_type', 'selected_answer'
        ).order_by('user', 'question__quiz_type', 'timestamp')

        if not responses.exists():
            self.stdout.write(self.style.WARNING('⚠️ No responses yet!'))
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = 'exports'
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'user_responses_{timestamp}.csv')

        # CALCULATE QUIZ TIMES
        quiz_times = {}
        for user in {r.user for r in responses}:
            for quiz_type in {r.question.quiz_type for r in responses if r.user == user}:
                user_quiz_responses = [r for r in responses if r.user == user and r.question.quiz_type == quiz_type]
                if user_quiz_responses:
                    start_time = min(r.timestamp for r in user_quiz_responses)
                    end_time = max(r.timestamp for r in user_quiz_responses)
                    total_seconds = (end_time - start_time).total_seconds()
                    quiz_times[(user.id, quiz_type.id)] = max(0, total_seconds)

        # WRITE CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'User', 'User_Email', 'Quiz_Type', 'Question_Number', 'Question_Text',
                'Selected_Answer', 'Correct_Answers', 'Is_Correct', 'Is_Incorrect',
                'Response_Timestamp', 'Time_Taken_Question_Seconds', 'Total_Quiz_Time_Seconds'
            ])

            previous_response = None
            for response in responses:
                correct_answers = ', '.join([a.text for a in response.question.answer_set.filter(correct=True)])
                
                # Time per question
                time_taken_question = 0
                if previous_response and previous_response.user == response.user and previous_response.question.quiz_type == response.question.quiz_type:
                    time_taken_question = (response.timestamp - previous_response.timestamp).total_seconds()
                else:
                    time_taken_question = response.question.quiz_type.time_per_question or 60
                time_taken_question = max(0, min(time_taken_question, response.question.quiz_type.time_per_question or 60))
                
                total_quiz_time = quiz_times.get((response.user.id, response.question.quiz_type.id), 0)

                writer.writerow([
                    response.user.username,
                    response.user.email,
                    response.question.quiz_type.name,
                    str(response.question.number),
                    response.question.text.replace('\n', ' '),
                    response.selected_answer.text,
                    correct_answers,
                    '1' if response.is_correct else '0',
                    '1' if not response.is_correct else '0',
                    response.timestamp.isoformat(),
                    str(round(time_taken_question, 2)),
                    str(round(total_quiz_time, 2))
                ])
                previous_response = response

        self.stdout.write(self.style.SUCCESS(f'✅ CSV saved: {output_file}'))

        # **AUTO UPDATE GOOGLE SHEETS**
        if format_type in ['sheets', 'both']:
            self.update_google_sheets(output_file)

    def update_google_sheets(self, csv_file):
        """AUTO UPDATE GOOGLE SHEETS - INSTANT!"""
        try:
            self.stdout.write('🔄 CONNECTING TO GOOGLE SHEETS...')
            
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
            client = authorize(creds)
            
            # **OPEN YOUR SHEET**
            sheet = client.open("QuizResponses_Live").sheet1
            
            # **CLEAR & UPDATE - INSTANT!**
            sheet.clear()
            
            # **UPLOAD CSV DATA**
            with open(csv_file, 'r', encoding='utf-8') as file:
                csv_data = list(csv.reader(file))
                sheet.update('A1', csv_data)
            
            rows_updated = len(csv_data)
            self.stdout.write(self.style.SUCCESS(f'🎉 GOOGLE SHEETS UPDATED! {rows_updated} rows'))
            self.stdout.write(self.style.SUCCESS('🚀 LOOKER STUDIO will refresh in 15 mins!'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('❌ credentials.json NOT FOUND!'))
            self.stdout.write(self.style.WARNING('📝 Put credentials.json in project root'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ SHEETS ERROR: {e}'))