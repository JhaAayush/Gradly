<template>
  <div>
    <!-- Hero Section -->
    <section class="text-center py-20">
      <h1 class="text-5xl md:text-7xl font-extrabold text-slate-800 mb-4 tracking-tighter">
        Welcome to Gradly
      </h1>
      <p class="text-lg md:text-xl text-slate-500 mb-8 max-w-2xl mx-auto">
        Your all-in-one portal for career management, academic tracking, and campus life at IIM Amritsar.
      </p>

      <!-- Next Deadline Card -->
      <div v-if="closestTask" class="bg-white/60 backdrop-blur-lg p-5 rounded-xl shadow-lg max-w-lg mx-auto mb-10 border border-slate-200">
        <h3 class="text-lg font-bold text-slate-800 flex items-center justify-center gap-2">
            <i class="fa fa-bell text-sky-500 animate-pulse"></i>
            <span>Your Next Deadline</span>
        </h3>
        <p class="text-slate-700 mt-2 text-lg">{{ closestTask.title }}</p>
        <p class="text-sm text-slate-500 font-mono">Due: {{ formattedDueDate }}</p>
      </div>

      <router-link to="/dashboard"
          class="inline-block bg-slate-800 text-white px-8 py-3 rounded-full font-semibold text-lg hover:bg-sky-500 transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-sky-200">
          Go to Dashboard <i class="fa fa-arrow-right ml-2"></i>
      </router-link>
    </section>

    <!-- Feature Cards Section -->
    <section class="grid md:grid-cols-3 gap-8 mt-16">
        <!-- Student Profiles -->
        <component :is="currentUser.isAuthenticated ? 'router-link' : 'router-link'"
           :to="currentUser.isAuthenticated ? '/profile/' + currentUser.id : '/login'"
           class="group block bg-white/70 backdrop-blur-lg p-8 rounded-2xl shadow-lg border border-slate-200 hover:border-sky-400 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 relative">
            <i class="fa fa-users text-3xl text-sky-500 mb-4"></i>
            <h3 class="text-xl font-bold mb-2 text-slate-800">Student Profiles</h3>
            <p class="text-slate-600">Manage your resume, CGPA, and contact details in one professional space.</p>
            <span
                class="absolute bottom-6 right-6 text-slate-300 group-hover:text-sky-500 transition-colors transform group-hover:translate-x-1 duration-300">
                <i class="fa fa-arrow-right"></i>
            </span>
        </component>

        <!-- To-Do Tracker -->
        <component :is="currentUser.isAuthenticated ? 'router-link' : 'router-link'"
           :to="currentUser.isAuthenticated ? '/dashboard' : '/login'"
           class="group block bg-white/70 backdrop-blur-lg p-8 rounded-2xl shadow-lg border border-slate-200 hover:border-sky-400 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 relative">
            <i class="fa fa-check-double text-3xl text-sky-500 mb-4"></i>
            <h3 class="text-xl font-bold mb-2 text-slate-800">To-Do Tracker</h3>
            <p class="text-slate-600">Stay on top of assignments, deadlines, and crucial career prep tasks.</p>
            <span
                class="absolute bottom-6 right-6 text-slate-300 group-hover:text-sky-500 transition-colors transform group-hover:translate-x-1 duration-300">
                <i class="fa fa-arrow-right"></i>
            </span>
        </component>

        <!-- Events & Committees -->
        <component :is="currentUser.isAuthenticated ? 'router-link' : 'router-link'"
           :to="currentUser.isAuthenticated ? '/events' : '/login'"
           class="group block bg-white/70 backdrop-blur-lg p-8 rounded-2xl shadow-lg border border-slate-200 hover:border-sky-400 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 relative">
            <i class="fa fa-calendar-days text-3xl text-sky-500 mb-4"></i>
            <h3 class="text-xl font-bold mb-2 text-slate-800">Events & Committees</h3>
            <p class="text-slate-600">Know what's happening around campus and never miss an important event.</p>
            <span
                class="absolute bottom-6 right-6 text-slate-300 group-hover:text-sky-500 transition-colors transform group-hover:translate-x-1 duration-300">
                <i class="fa fa-arrow-right"></i>
            </span>
        </component>
    </section>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'

// Mock User Data
const currentUser = reactive({
    isAuthenticated: true,
    id: 1
})

// Mock Task Data
const closestTask = reactive({
    title: 'Assignment 1 Submission',
    due_date: new Date(new Date().setDate(new Date().getDate() + 2)) // 2 days from now
})

const formattedDueDate = computed(() => {
    if (!closestTask.due_date) return ''
    const options = { weekday: 'long', year: 'numeric', month: 'short', day: 'numeric' }
    return closestTask.due_date.toLocaleDateString('en-GB', options)
})
</script>
