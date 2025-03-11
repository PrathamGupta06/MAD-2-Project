<template>
  <div class="container mt-4">
    <div v-if="loading" class="text-center">Loading quiz...</div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="quiz" class="quiz-container">
      <div class="timer-alert" :class="{ 'alert-warning': timeLeft > 10, 'alert-danger': timeLeft <= 10 }">
        Time Remaining: {{ formattedTime }}
      </div>

      <div class="question-header">
        <h5>Question {{ currentQuestionIndex + 1 }} of {{ quiz.questions.length }}</h5>
      </div>

      <div class="question-card" v-for="(question, index) in quiz.questions" :key="question.id" v-show="index === currentQuestionIndex">
        <h4 class="question-text">{{ question.question_statement }}</h4>
        <div class="options-container">
          <button 
            v-for="(option, optIndex) in question.options" 
            :key="optIndex"
            class="option-btn"
            :class="{ selected: answers[question.id] === optIndex + 1 }"
            @click="selectAnswer(question.id, optIndex + 1)"
          >
            {{ option }}
          </button>
        </div>
      </div>

      <div class="navigation-btns">
        <button 
          v-if="currentQuestionIndex < quiz.questions.length - 1"
          class="btn btn-primary"
          @click="nextQuestion"
          :disabled="!answers[quiz.questions[currentQuestionIndex].id]"
        >
          Next Question
        </button>
        <button 
          v-else
          class="btn btn-success"
          @click="submitAnswers"
          :disabled="!allQuestionsAnswered"
        >
          Submit Quiz
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserAttemptQuiz',
  data() {
    return {
      quiz: null,
      loading: false,
      error: '',
      currentQuestionIndex: 0,
      answers: {},
      timeLeft: 0,
      timerInterval: null
    };
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.timeLeft / 60);
      const seconds = this.timeLeft % 60;
      return `${minutes}:${seconds.toString().padStart(2, '0')}`;
    },
    allQuestionsAnswered() {
      return this.quiz.questions.every(q => this.answers.hasOwnProperty(q.id));
    }
  },
  methods: {
    async fetchQuiz() {
      this.loading = true;
      try {
        const response = await axios.get(`http://localhost:5000/api/user/quizQuestions/${this.$route.params.id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.quiz = response.data;
        this.timeLeft = this.quiz.time_duration * 60; // Convert minutes to seconds
        this.startTimer();
      } catch (error) {
        this.error = 'Failed to load quiz';
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
    startTimer() {
      this.timerInterval = setInterval(() => {
        if (this.timeLeft <= 0) {
          this.submitAnswers();
          return;
        }
        this.timeLeft--;
      }, 1000);
    },
    selectAnswer(questionId, optionNumber) {
      this.answers[questionId] = optionNumber;
    },
    nextQuestion() {
      if (!this.answers[this.quiz.questions[this.currentQuestionIndex].id]) {
        this.error = 'Please select an answer before proceeding';
        return;
      }
      this.error = '';
      this.currentQuestionIndex++;
    },
    async submitAnswers() {
      clearInterval(this.timerInterval);
      try {
        await axios.post('http://localhost:5000/api/submit-answers', {
          quiz_id: this.quiz.id,
          answers: Object.keys(this.answers).map(questionId => ({
            question_id: parseInt(questionId),
            selected_option: this.answers[questionId]
          }))
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.$router.push('/user/scores');
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.error = error.response.data.message;
        } else {
          this.error = 'Failed to submit answers';
        }
        console.error(error);
      }
    }
  },
  mounted() {
    this.fetchQuiz();
  },
  beforeUnmount() {
    clearInterval(this.timerInterval);
  }
};
</script>

<style scoped>
.quiz-container {
  max-width: 800px;
  margin: 0 auto;
}

.timer-alert {
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 5px;
  text-align: center;
  font-weight: bold;
}

.question-card {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.options-container {
  display: grid;
  gap: 10px;
  margin-top: 20px;
}

.option-btn {
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 5px;
  background: #f8f9fa;
  text-align: left;
  transition: all 0.2s;
}

.option-btn.selected {
  border-color: #0d6efd;
  background: #e7f1ff;
}

.navigation-btns {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>