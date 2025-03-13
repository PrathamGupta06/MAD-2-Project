from celery import shared_task
from flask_mail import Message
from extensions import mail, excel
from models import User, Score, Quiz
from io import BytesIO
import os
from email_templates import get_daily_reminder_template, get_monthly_report_template
from sqlalchemy import func
from datetime import datetime, timedelta

@shared_task(ignore_results = False)
def generate_admin_report():
    try:
        users = User.query.all()
        user_data = [['User ID', 'UserName', 'Full Name', 'Qualification',  'Quizzes Taken', 'Average Score', 'Highest Score', 'Lowest Score']]

        for user in users:
            scores = Score.query.filter_by(user_id=user.id).all()
            total_quizzes = len(scores)
            
            if total_quizzes > 0:
                score_values = [score.total_score for score in scores]
                avg_score = sum(score_values) / total_quizzes
                highest_score = max(score_values)
                lowest_score = min(score_values)
            else:
                avg_score = 0
                highest_score = 0
                lowest_score = 0

            user_data.append([
                user.id,
                user.username,
                user.full_name,
                user.qualification,
                total_quizzes,
                round(avg_score, 2),
                highest_score,
                lowest_score
            ])
        csv_data = excel.make_response_from_array(user_data, "csv")
        csv_bytes = csv_data.data
        buffer = BytesIO(csv_bytes)

        msg = Message(
            'User Performance Report',
            recipients=[os.environ.get("ADMIN_EMAIL")]
        )
        msg.body = 'Please find attached the user performance report.'
        msg.attach(
            'user_report.csv',
            'text/csv',
            buffer.getvalue()
        )

        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return False

@shared_task
def send_daily_reminders():
    try:
        today = datetime.now().date()
        users = User.query.all()
        
        for user in users:
            # Get today's quizzes that user hasn't attempted
            todays_quizzes = Quiz.query\
                .filter(Quiz.date_of_quiz == today)\
                .filter(~Quiz.scores.any(Score.user_id == user.id))\
                .all()
            
            if todays_quizzes:
                quiz_data = [{
                    'subject_name': quiz.chapter.subject.name,
                    'chapter_name': quiz.chapter.name,
                    'date_of_quiz': quiz.date_of_quiz.strftime('%Y-%m-%d')
                } for quiz in todays_quizzes]
                
                msg = Message(
                    'Reminder: You have quizzes scheduled for today!',
                    recipients=[user.email],
                    html=get_daily_reminder_template(user.full_name, quiz_data)
                )
                mail.send(msg)
        
        return True
    except Exception as e:
        print(f"Error sending daily reminders: {str(e)}")
        return False


@shared_task
def send_monthly_reports():
    try:
        users = User.query.all()
        current_month = datetime.now()
        for user in users:
            # Get last month's scores
            monthly_scores = Score.query\
                .filter(Score.user_id == user.id)\
                .filter(func.extract('month', Score.time_stamp_of_attempt) == current_month.month)\
                .filter(func.extract('year', Score.time_stamp_of_attempt) == current_month.year)\
                .all()
            
            if monthly_scores:
                quiz_details = []
                for score in monthly_scores:

                    rank = Score.query\
                        .filter(Score.quiz_id == score.quiz_id)\
                        .filter(Score.total_score > score.total_score)\
                        .count() + 1
                    
                    quiz_details.append({
                        'name': f"{score.quiz.chapter.subject.name} - {score.quiz.chapter.name}",
                        'score': score.total_score,
                        'rank': rank,
                        'date': score.time_stamp_of_attempt.strftime('%Y-%m-%d')
                    })
                
                stats = {
                    'total_quizzes': len(monthly_scores),
                    'average_score': sum(s.total_score for s in monthly_scores) / len(monthly_scores),
                    'highest_score': max(s.total_score for s in monthly_scores),
                    'quizzes': quiz_details
                }
                
                msg = Message(
                    f'Monthly Activity Report - {current_month.strftime("%B %Y")}',
                    recipients=[user.email],
                    html=get_monthly_report_template(user.full_name, stats)
                )
                mail.send(msg)
        
        return True
    except Exception as e:
        print(f"Error sending monthly reports: {str(e)}")
        return False