from django.urls import path
from . import views
# 💡 IMPORT QUIZ VIEWS: Import the views file from your quiz application (e.g., 'myapp')
from myapp import views as quiz_views # Assuming your quiz app is named 'myapp'

app_name="Admin"

urlpatterns = [
    # --- Existing Admin Paths ---
    path('homepage/', views.HomePage, name="Homepage"),
    path('jobpost/', views.jobpost, name="jobpost"),
    path("deletedjobpost/<int:id>", views.deletedjobpost, name="deletedjobpost"),
    path('eligiblelist/<int:id>', views.eligiblelist, name="Eligiblelist"),
    path('viewcomplaint/', views.viewcomplaint, name="viewcomplaint"),
    path('reply/<int:id>', views.reply, name="reply"),

    # --- 💡 QUIZ MANAGEMENT PATHS (Linked from myapp) ---
    # 1. Main Quiz Dashboard (List of Quizzes to Manage)
    path('quiz-dashboard/', quiz_views.quiz_dashboard, name='quiz_dashboard_admin'),
    
    # 2. Add New Quiz/Setup
    path('quiz-setup/', quiz_views.quiz_setup, name='quiz_setup_admin'),

    # 3. Add Question to a NEWLY created quiz (session-based setup)
    path('add-question/', quiz_views.add_question, name='add_question_admin'),
    
    # 4. Add Question to an EXISTING quiz (via ID)
    path('add-question/<int:quiz_type_id>/', quiz_views.add_question, name='add_question_for_quiz_admin'),

    # 5. Edit Questions (list all for a quiz)
    path('edit-questions/<int:quiz_type_id>/', quiz_views.edit_questions, name='edit_questions_admin'),

    # 6. Edit a Specific Question
    path('edit-questions/<int:quiz_type_id>/<int:question_id>/edit/', quiz_views.edit_question, name='edit_question_admin'),
    
    # 7. Delete a Specific Question
    path('edit-questions/<int:quiz_type_id>/<int:question_id>/delete/', quiz_views.delete_question, name='delete_question_admin'),
]