<template>
  <div>
    <div class="mb-8">
      <h1 class="text-4xl font-extrabold text-slate-800">Welcome back, {{ currentUser.name.split(' ')[0] }}!</h1>
      <p id="current-date" class="text-slate-500 mt-1">{{ currentDateText }}</p>
    </div>

    <div class="grid md:grid-cols-3 gap-8">
      <!-- Profile Card -->
      <div class="flex flex-col bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-slate-200">
        <h2 class="text-xl font-bold text-slate-800 mb-4">Your Profile</h2>

        <div class="flex items-center space-x-4 mb-4">
            <div class="w-16 h-16 rounded-full overflow-hidden border-2 border-sky-200 shadow-md bg-slate-200">
                <img :src="currentUser.profilePic || '/src/assets/default-profile.png'" alt="Profile Picture" class="w-full h-full object-cover">
            </div>
            <div>
                <p class="font-bold text-slate-800">{{ currentUser.name }}</p>
                <p class="text-sm text-slate-500">{{ currentUser.id }}</p>
            </div>
        </div>

        <div class="mb-4">
            <div class="flex justify-between mb-1">
                <span class="text-sm font-medium text-slate-600">Profile Strength</span>
                <span class="text-sm font-medium text-sky-600">{{ profilePercentage }}%</span>
            </div>
            <div class="w-full bg-slate-200 rounded-full h-2.5">
                <div class="bg-sky-500 h-2.5 rounded-full transition-all duration-500" :style="{ width: profilePercentage + '%' }">
                </div>
            </div>
        </div>

        <div class="grid grid-cols-2 gap-4 text-center border-t border-slate-200 pt-4 mb-4">
            <div>
                <p class="text-2xl font-bold text-slate-800">{{ currentUser.skills.length }}</p>
                <p class="text-xs text-slate-500">Skills Listed</p>
            </div>
            <div>
                <p class="text-2xl font-bold text-slate-800">{{ currentUser.workExperiences.length + currentUser.internships.length }}</p>
                <p class="text-xs text-slate-500">Experiences</p>
            </div>
        </div>

        <div class="mt-auto flex gap-3">
            <router-link to="/profile/edit" class="w-1/2 text-center bg-slate-200 text-slate-700 px-4 py-2 rounded-lg font-semibold hover:bg-slate-300 transition-all text-sm">
                Edit
            </router-link>
            <router-link :to="'/profile/' + currentUser.id" class="w-1/2 text-center bg-slate-800 text-white px-4 py-2 rounded-lg font-semibold hover:bg-sky-500 transition-all text-sm">
                View Profile
            </router-link>
        </div>
      </div>

      <!-- Tasks Card -->
      <div class="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-slate-200">
        <h2 class="text-xl font-bold text-slate-800 mb-4">Your Tasks</h2>
        <ul class="space-y-3 mb-6 h-48 overflow-y-auto pr-2">
            <li v-for="task in tasks" :key="task.id" class="flex justify-between items-center bg-slate-50/80 p-3 rounded-lg">
                <div class="flex items-center space-x-3">
                    <button @click="toggleTask(task.id)" class="w-6 h-6 rounded-full border-2 border-slate-300 flex items-center justify-center transition-all duration-200" :class="task.isDone ? 'bg-green-500 border-green-500' : 'hover:border-sky-400'">
                        <i v-if="task.isDone" class="fa fa-check text-white text-xs"></i>
                    </button>
                    <div :class="task.isDone ? 'line-through text-slate-400' : 'text-slate-700'">
                        <p class="font-medium">{{ task.title }}</p>
                        <small class="text-xs" :class="task.isDone ? 'text-slate-400' : 'text-slate-500'">
                            Due: {{ task.dueDate ? formatDate(task.dueDate) : 'No deadline' }}
                        </small>
                    </div>
                </div>
                <div class="flex space-x-1 opacity-0 hover:opacity-100 transition-opacity">
                    <button class="h-7 w-7 flex items-center justify-center rounded-full text-slate-500 hover:bg-yellow-100 hover:text-yellow-600">
                        <i class="fa fa-pen text-xs"></i>
                    </button>
                    <button @click="deleteTask(task.id)" class="h-7 w-7 flex items-center justify-center rounded-full text-slate-500 hover:bg-red-100 hover:text-red-600">
                        <i class="fa fa-trash text-xs"></i>
                    </button>
                </div>
            </li>
            <p v-if="tasks.length === 0" class="text-slate-500 text-center py-10">You're all caught up!</p>
        </ul>
        <form @submit.prevent="addTask" class="mt-4 border-t border-slate-200 pt-4">
            <input v-model="newTask.title" class="w-full p-2 bg-slate-100 border-transparent rounded-lg mb-2 focus:ring-2 focus:ring-sky-500 transition" placeholder="Add a new task..." required>
            <input v-model="newTask.dueDate" class="w-full p-2 bg-slate-100 border-transparent rounded-lg mb-2 focus:ring-2 focus:ring-sky-500 transition text-slate-500" type="date">
            <button type="submit" class="mt-2 w-full bg-slate-800 text-white font-semibold py-2 rounded-lg hover:bg-sky-500 transition-all duration-300">Add Task</button>
        </form>
      </div>

      <!-- Upcoming Events Card -->
      <div class="bg-white/70 backdrop-blur-lg p-6 rounded-2xl shadow-lg border border-slate-200">
        <h2 class="text-xl font-bold text-slate-800 mb-4">Upcoming Events</h2>
        <ul class="space-y-3">
            <li v-for="event in events" :key="event.id" class="bg-slate-50/80 p-3 rounded-lg flex items-center space-x-4">
                <div class="flex-shrink-0 bg-sky-100 text-sky-600 h-10 w-10 rounded-lg flex flex-col items-center justify-center font-bold">
                    <span class="text-xs -mb-1">{{ formatMonth(event.date) }}</span>
                    <span class="text-lg">{{ formatDay(event.date) }}</span>
                </div>
                <div>
                    <p class="font-semibold text-slate-700">{{ event.title }}</p>
                    <small class="text-slate-500">{{ formatFullDate(event.date) }}</small>
                    <br>
                    <small class="text-slate-400 italic">Hosted by {{ event.bodyName }}</small>
                </div>
            </li>
            <p v-if="events.length === 0" class="text-slate-500">No upcoming events listed.</p>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'

// Mock User Data
const currentUser = reactive({
    name: 'Test User',
    id: 1,
    profilePic: null,
    resume: true,
    phone: true,
    cgpa: true,
    skills: ['Python', 'Vue'],
    workExperiences: [{}],
    internships: [{}],
    certifications: []
})

const profilePercentage = computed(() => {
    let completed = 0;
    if (currentUser.profilePic) completed++;
    if (currentUser.resume) completed++;
    if (currentUser.phone) completed++;
    if (currentUser.cgpa) completed++;
    if (currentUser.skills.length) completed++;
    if (currentUser.workExperiences.length) completed++;
    if (currentUser.internships.length) completed++;
    if (currentUser.certifications.length) completed++;
    return Math.round((completed / 8) * 100);
})

// Mock Tasks
const tasks = ref([
    { id: 1, title: 'Finish Project', isDone: false, dueDate: '2023-10-25' },
    { id: 2, title: 'Submit Report', isDone: true, dueDate: '2023-10-20' }
])

const newTask = reactive({ title: '', dueDate: '' })

const addTask = () => {
    tasks.value.push({
        id: Date.now(),
        title: newTask.title,
        dueDate: newTask.dueDate,
        isDone: false
    })
    newTask.title = ''
    newTask.dueDate = ''
}

const toggleTask = (id) => {
    const task = tasks.value.find(t => t.id === id)
    if (task) task.isDone = !task.isDone
}

const deleteTask = (id) => {
    tasks.value = tasks.value.filter(t => t.id !== id)
}

// Mock Events
const events = ref([
    { id: 1, title: 'Annual Tech Fest', date: '2023-11-15', bodyName: 'Tech Club' }
])

// Date Helpers
const currentDateText = ref('')
onMounted(() => {
    const today = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    currentDateText.value = `Here's your overview for today, ${today.toLocaleDateString('en-US', options)}.`;
})

const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}

const formatMonth = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', { month: 'short' })
}

const formatDay = (dateString) => {
    return new Date(dateString).getDate()
}

const formatFullDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
}

</script>
