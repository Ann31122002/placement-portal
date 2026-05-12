from rest_framework import serializers
from .models import Question, TestCase, Submission

class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id','input_data','expected_output']

class QuestionSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id','title','description','difficulty','test_cases']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id','question','code','language','created_at','status']



class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['id', 'input_data', 'expected_output']

class QuestionSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'title', 'description', 'difficulty', 'test_cases']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'question', 'code', 'language', 'submitted_at', 'result']

