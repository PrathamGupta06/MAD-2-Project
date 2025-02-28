<template>
    <div class="container">
        <h2 class="mb-4">Admin Dashboard</h2>
    </div>
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="w-100">Subjects</h1>
            <button class="btn btn-primary" @click="openCreateSubjectModal">
                <i class="bi bi-plus-circle"></i> Add Subject
            </button>
        </div>
        <div v-if="loading.subjects">Loading subjects...</div>
        <div v-else-if="error.subjects" class="text-danger">{{ error.subjects }}</div>
        <div v-else-if="subjects.length === 0" class="text-muted">
            No subjects available.
        </div>
        <div v-else class="row">
            <div v-for="subject in subjects" :key="subject.id" class="col-md-6 mb-4">
                <div class="card h-100">
                    <div class="card-header bg-light d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">{{ subject.name }}</h5>
                        <div>
                            <button class="btn btn-sm btn-outline-success me-2" @click="openCreateChapterModal(subject)">
                                <i class="bi bi-plus-circle"></i> Add Chapter
                            </button>
                            <button class="btn btn-sm btn-outline-primary me-2" @click="openEditSubjectModal(subject)">
                                <i class="bi bi-pencil"></i> Edit
                            </button>
                            <button class="btn btn-sm btn-outline-danger" @click="confirmDeleteSubject(subject)">
                                <i class="bi bi-trash"></i> Delete
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <p class="card-text">{{ subject.description }}</p>
                        <h6 class="mt-3 mb-2">Chapters:</h6>
                        <div class="table-responsive">
                            <table class="table table-bordered table-hover">
                                <thead class="table-light">
                                    <tr>
                                        <th>Chapter Name</th>
                                        <th>Description</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="chapter in subject.chapters" :key="chapter.id">
                                        <td>{{ chapter.name }}</td>
                                        <td>{{ chapter.description }}</td>
                                        <td>
                                            <button class="btn btn-sm btn-outline-primary me-2" @click="openEditChapterModal(chapter, subject)">
                                                <i class="bi bi-pencil"></i> Edit
                                            </button>
                                            <button class="btn btn-sm btn-outline-danger" @click="confirmDeleteChapter(chapter, subject)">
                                                <i class="bi bi-trash"></i> Delete
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Create/Edit Subject Modal -->
    <div class="modal fade" id="subjectModal" tabindex="-1" aria-labelledby="subjectModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="subjectModalLabel">{{ isEditing ? 'Edit Subject' : 'Create Subject' }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="submitSubject">
                        <div class="mb-3">
                            <label for="subjectName" class="form-label">Subject Name</label>
                            <input type="text" class="form-control" id="subjectName" v-model="subjectForm.name" required>
                        </div>
                        <div class="mb-3">
                            <label for="subjectDescription" class="form-label">Description</label>
                            <textarea class="form-control" id="subjectDescription" v-model="subjectForm.description" rows="3" required></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" @click="submitSubject">{{ isEditing ? 'Update' : 'Create' }}</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div class="modal fade" id="deleteConfirmationModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Confirm Delete</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Are you sure you want to delete this subject? This action cannot be undone.
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger" @click="deleteSubject">Delete</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Create/Edit Chapter Modal -->
    <div class="modal fade" id="chapterModal" tabindex="-1" aria-labelledby="chapterModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="chapterModalLabel">{{ isEditingChapter ? 'Edit Chapter' : 'Create Chapter' }}</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="submitChapter">
                        <div class="mb-3">
                            <label for="chapterName" class="form-label">Chapter Name</label>
                            <input type="text" class="form-control" id="chapterName" v-model="chapterForm.name" required>
                        </div>
                        <div class="mb-3">
                            <label for="chapterDescription" class="form-label">Description</label>
                            <textarea class="form-control" id="chapterDescription" v-model="chapterForm.description" rows="3" required></textarea>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary" @click="submitChapter">{{ isEditingChapter ? 'Update' : 'Create' }}</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Delete Chapter Confirmation Modal -->
    <div class="modal fade" id="deleteChapterModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Confirm Delete Chapter</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Are you sure you want to delete this chapter? This action cannot be undone.
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-danger" @click="deleteChapter">Delete</button>
                </div>
            </div>
        </div>
    </div>
    <router-view />
</template>

<script>
import axios from 'axios';

export default {
    name: 'AdminDashboard',
    data() {
        return {
            quizzes: [],
            subjects: [],
            loading: {
                quizzes: true,
                subjects: true
            },
            error: {
                quizzes: null,
                subjects: null
            },
            subjectForm: {
                name: '',
                description: ''
            },
            chapterForm: {
                name: '',
                description: ''
            },
            isEditing: false,
            isEditingChapter: false,
            selectedSubject: null,
            selectedChapter: null,
            subjectModal: null,
            deleteModal: null,
            chapterModal: null,
            deleteChapterModal: null
        };
    },
    mounted() {
        this.fetchData();
        this.initializeModals();
    },
    methods: {
        initializeModals() {
            this.subjectModal = new bootstrap.Modal(document.getElementById('subjectModal'));
            this.deleteModal = new bootstrap.Modal(document.getElementById('deleteConfirmationModal'));
            this.chapterModal = new bootstrap.Modal(document.getElementById('chapterModal'));
            this.deleteChapterModal = new bootstrap.Modal(document.getElementById('deleteChapterModal'));
        },
        async fetchData() {
            try {
                const subjectsResponse = await axios.get('http://localhost:5000/api/subjects', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.subjects = subjectsResponse.data.subjects;
                this.error.subjects = null;
            } catch (error) {
                this.error.subjects = 'Failed to load subjects';
                console.error('Error fetching subjects:', error);
            } finally {
                this.loading.subjects = false;
            }
        },
        openCreateSubjectModal() {
            this.isEditing = false;
            this.subjectForm = { name: '', description: '' };
            this.subjectModal.show();
        },
        openEditSubjectModal(subject) {
            this.isEditing = true;
            this.selectedSubject = subject;
            this.subjectForm = {
                name: subject.name,
                description: subject.description
            };
            this.subjectModal.show();
        },
        async submitSubject() {
            try {
                const headers = {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                };

                if (this.isEditing && this.selectedSubject) {
                    await axios.put(`http://localhost:5000/api/subjects/${this.selectedSubject.id}`,
                        this.subjectForm,
                        { headers }
                    );
                } else {
                    await axios.post('http://localhost:5000/api/subjects',
                        this.subjectForm,
                        { headers }
                    );
                }

                this.subjectModal.hide();
                await this.fetchData();
            } catch (error) {
                console.error('Error submitting subject:', error);
                alert('Failed to save subject. Please try again.');
            }
        },
        confirmDeleteSubject(subject) {
            this.selectedSubject = subject;
            this.deleteModal.show();
        },
        async deleteSubject() {
            try {
                await axios.delete(`http://localhost:5000/api/subjects/${this.selectedSubject.id}`, {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                });
                this.deleteModal.hide();
                await this.fetchData();
            } catch (error) {
                console.error('Error deleting subject:', error);
                alert('Failed to delete subject. Please try again.');
            }
        },
    openCreateChapterModal(subject) {
        this.isEditingChapter = false;
        this.selectedSubject = subject;
        this.chapterForm = { name: '', description: '', subject_id: subject.id };
        this.chapterModal.show();
    },
    openEditChapterModal(chapter, subject) {
        this.isEditingChapter = true;
        this.selectedSubject = subject;
        this.selectedChapter = chapter;
        this.chapterForm = {
            name: chapter.name,
            description: chapter.description
        };
        this.chapterModal.show();
    },
    async submitChapter() {
        try {
            const headers = {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            };

            if (this.isEditingChapter && this.selectedChapter) {
                await axios.put(
                    `http://localhost:5000/api/chapters/${this.selectedChapter.id}`,
                    this.chapterForm,
                    { headers }
                );
            } else {
                await axios.post(
                    `http://localhost:5000/api/chapters`,
                    this.chapterForm,
                    { headers }
                );
            }

            this.chapterModal.hide();
            await this.fetchData();
        } catch (error) {
            console.error('Error submitting chapter:', error);
            alert('Failed to save chapter. Please try again.');
        }
    },
    confirmDeleteChapter(chapter, subject) {
        this.selectedChapter = chapter;
        this.selectedSubject = subject;
        this.deleteChapterModal.show();
    },
    async deleteChapter() {
        try {
            await axios.delete(
                `http://localhost:5000/api/chapters/${this.selectedChapter.id}`,
                {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                }
            );
            this.deleteChapterModal.hide();
            await this.fetchData();
        } catch (error) {
            console.error('Error deleting chapter:', error);
            alert('Failed to delete chapter. Please try again.');
        }
    }
    },
};
</script>