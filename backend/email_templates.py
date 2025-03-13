def get_daily_reminder_template(user_name, new_quizzes):
    return f"""
    <html>
        <body>
            <h2>Hello {user_name}!</h2>
            <p>We noticed you haven't visited recently. Here are some quizzes you might be interested in:</p>
            <ul>
                {''.join(f'<li>{quiz["subject_name"]} - {quiz["chapter_name"]}: {quiz["date_of_quiz"]}</li>' for quiz in new_quizzes)}
            </ul>
            <p>Visit the platform to attempt these quizzes!</p>
        </body>
    </html>
    """

def get_monthly_report_template(user_name, stats):
    return f"""
    <html>
        <body>
            <h2>Monthly Activity Report for {user_name}</h2>
            <h3>Summary</h3>
            <ul>
                <li>Total Quizzes Attempted: {stats['total_quizzes']}</li>
                <li>Average Score: {stats['average_score']}%</li>
                <li>Best Performance: {stats['highest_score']}%</li>
            </ul>
            <h3>Quiz Details</h3>
            <table border="1">
                <tr>
                    <th>Quiz</th>
                    <th>Score</th>
                    <th>Rank</th>
                    <th>Date</th>
                </tr>
                {''.join(f'''
                    <tr>
                        <td>{quiz['name']}</td>
                        <td>{quiz['score']}%</td>
                        <td>{quiz['rank']}</td>
                        <td>{quiz['date']}</td>
                    </tr>
                ''' for quiz in stats['quizzes'])}
            </table>
        </body>
    </html>
    """