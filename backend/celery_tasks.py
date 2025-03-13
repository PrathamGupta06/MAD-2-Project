from celery import shared_task
from flask_mail import Message
from extensions import mail, excel
from models import User, Score
from io import BytesIO
import os

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
            'Quiz System - User Report',
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
