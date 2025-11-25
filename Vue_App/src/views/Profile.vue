<template>
  <div>
    <div class="relative bg-gradient-to-br from-slate-900 to-sky-800 rounded-3xl shadow-2xl mb-12 text-white overflow-hidden">
        <div class="absolute inset-0 bg-grid-slate-700/20 [mask-image:linear-gradient(to_bottom,white,transparent)]"></div>
        <div class="flex flex-col md:flex-row items-center p-8 md:p-12 relative z-10">
            <div class="relative flex-shrink-0">
                <div class="w-36 h-36 rounded-full overflow-hidden border-4 border-slate-600 shadow-lg bg-slate-700 ring-4 ring-sky-500/50">
                    <img :src="user.profilePic || '/src/assets/default-profile.png'" alt="Profile Picture" class="w-full h-full object-cover">
                </div>
            </div>
            <div class="mt-6 md:mt-0 md:ml-8 text-center md:text-left">
                <h1 class="text-4xl font-extrabold">{{ user.name }}</h1>
                <p class="text-lg text-sky-300 opacity-90 font-mono">{{ user.id }}</p>
                <p v-if="user.cgpa && user.showCgpa" class="mt-3 text-sm bg-sky-500/20 text-sky-200 px-4 py-1 inline-block rounded-full font-semibold">
                    CGPA: {{ user.cgpa }}
                </p>

                <div v-if="currentUser.id !== user.id" class="mt-5">
                    <button class="bg-sky-500 text-white font-semibold px-6 py-2 rounded-full hover:bg-sky-600 transition-all duration-300 shadow-lg">
                        <i class="fa fa-paper-plane mr-2"></i> Send Message
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
        <div class="md:col-span-1 space-y-8">
            <div class="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-slate-200">
                <h2 class="text-xl font-bold text-slate-800 mb-4">Personal Information</h2>
                <div class="space-y-3 text-slate-600">
                    <p v-if="user.showEmail" class="flex items-center gap-3">
                        <i class="fa fa-envelope w-4 text-center text-sky-500"></i>
                        <a :href="'mailto:' + user.email" class="hover:text-sky-600 hover:underline">{{ user.email }}</a>
                    </p>
                    <p v-if="user.showPhone" class="flex items-center gap-3">
                        <i class="fa fa-phone w-4 text-center text-sky-500"></i>
                        <span>{{ user.phone || 'Not Provided' }}</span>
                    </p>
                    <p v-if="user.linkedinUrl" class="flex items-center gap-3">
                        <i class="fab fa-linkedin w-4 text-center text-sky-600"></i>
                        <a :href="user.linkedinUrl" target="_blank" class="hover:text-sky-600 hover:underline">LinkedIn</a>
                    </p>
                    <p v-if="user.dob" class="flex items-center gap-3">
                        <i class="fa fa-calendar w-4 text-center text-sky-500"></i>
                        <span>DOB: {{ formatDate(user.dob) }}</span>
                    </p>
                </div>
            </div>

            <div class="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-slate-200">
                <h2 class="text-xl font-bold text-slate-800 mb-4">Academic Info</h2>
                <div class="space-y-3 text-slate-600">
                    <p class="flex items-center gap-3"><i class="fa fa-id-card w-4 text-center text-sky-500"></i> <span>{{ user.id }}</span></p>
                    <p class="flex items-center gap-3"><i class="fa fa-graduation-cap w-4 text-center text-sky-500"></i>
                        <span>CGPA: {{ user.cgpa || 'Not Provided' }}</span></p>
                    <p v-if="user.resume" class="flex items-center gap-3">
                        <i class="fa fa-file-arrow-down w-4 text-center text-sky-500"></i>
                        <a href="#" class="hover:text-sky-600 hover:underline">Download Resume</a>
                    </p>
                </div>
            </div>
        </div>

        <div class="md:col-span-2 space-y-8">
            <div class="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-slate-200">
                <h2 class="text-xl font-bold text-slate-800 mb-6">Professional Experience</h2>
                <div class="relative pl-6 border-l-2 border-slate-200 space-y-8">
                    <div v-for="exp in user.workExperiences" :key="exp.id" class="relative">
                        <div class="absolute -left-[34px] top-1 h-4 w-4 rounded-full bg-sky-500 ring-8 ring-white"></div>
                        <p class="font-bold text-slate-700">{{ exp.role }}</p>
                        <p class="text-sm font-medium text-sky-600">{{ exp.organization }}</p>
                        <p class="text-xs text-slate-500 mt-1">
                            {{ formatDateMonth(exp.startDate) }} – {{ exp.endDate ? formatDateMonth(exp.endDate) : 'Present' }}
                        </p>
                    </div>
                    <div v-for="intern in user.internships" :key="intern.id" class="relative">
                        <div class="absolute -left-[34px] top-1 h-4 w-4 rounded-full bg-slate-400 ring-8 ring-white"></div>
                        <p class="font-bold text-slate-700">{{ intern.role }} <span class="text-sm font-normal text-slate-500">(Internship)</span></p>
                        <p class="text-sm font-medium text-sky-600">{{ intern.organization }}</p>
                        <p class="text-xs text-slate-500 mt-1">
                            {{ formatDateMonth(intern.startDate) }} – {{ intern.endDate ? formatDateMonth(intern.endDate) : 'Present' }}
                        </p>
                    </div>
                    <p v-if="!user.workExperiences.length && !user.internships.length" class="text-slate-500">No professional experience listed.</p>
                </div>
            </div>

            <div class="grid md:grid-cols-2 gap-8">
                <div class="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-slate-200">
                    <h2 class="text-xl font-bold text-slate-800 mb-4">Skills</h2>
                    <div class="flex flex-wrap gap-2">
                        <span v-for="s in user.skills" :key="s" class="bg-sky-100 text-sky-800 px-3 py-1 rounded-full text-sm font-medium transition transform hover:scale-105">{{ s }}</span>
                        <p v-if="!user.skills.length" class="text-slate-500 text-sm">No skills listed.</p>
                    </div>
                </div>
                <div class="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-slate-200">
                    <h2 class="text-xl font-bold text-slate-800 mb-4">Hobbies</h2>
                    <div class="flex flex-wrap gap-2">
                        <span v-for="h in user.hobbies" :key="h" class="bg-slate-100 text-slate-800 px-3 py-1 rounded-full text-sm font-medium">{{ h }}</span>
                        <p v-if="!user.hobbies.length" class="text-slate-500 text-sm">No hobbies listed.</p>
                    </div>
                </div>
            </div>
            <div class="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-slate-200">
                <h2 class="text-xl font-bold text-slate-800 mb-4">Certifications</h2>
                <ul v-if="user.certifications.length" class="space-y-2">
                    <li v-for="c in user.certifications" :key="c" class="flex items-center gap-3 text-slate-700"><i class="fa fa-award text-yellow-500"></i>{{ c }}</li>
                </ul>
                <p v-else class="text-slate-500">No certifications listed.</p>
            </div>
        </div>

        <div v-if="currentUser.id === user.id" class="md:col-span-3 text-center mt-4">
            <router-link to="/profile/edit" class="inline-block bg-slate-800 text-white px-8 py-3 rounded-full font-semibold hover:bg-sky-500 transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-sky-200">
                <i class="fa fa-pencil mr-2"></i> Edit Your Profile
            </router-link>
        </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// Mock Current User
const currentUser = reactive({
    id: 1
})

// Mock Profile User Data
const user = reactive({
    id: 1,
    name: 'Test User',
    email: 'test@example.com',
    profilePic: null,
    cgpa: 9.5,
    showCgpa: true,
    showEmail: true,
    showPhone: true,
    phone: '1234567890',
    linkedinUrl: '#',
    dob: '2000-01-01',
    resume: true,
    workExperiences: [
        { id: 1, role: 'Software Engineer', organization: 'Tech Corp', startDate: '2022-06-01', endDate: null }
    ],
    internships: [
        { id: 1, role: 'Intern', organization: 'Startup Inc', startDate: '2021-05-01', endDate: '2021-08-01' }
    ],
    skills: ['Python', 'Vue.js', 'Flask'],
    hobbies: ['Reading', 'Coding'],
    certifications: ['AWS Certified Cloud Practitioner']
})

onMounted(() => {
    // In a real app, fetch user data based on route.params.userId
    // if (route.params.userId) { ... }
    console.log('Viewing profile for user:', route.params.userId || 'Current User')
})

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}

const formatDateMonth = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
}

</script>
