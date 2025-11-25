<template>
  <div class="flex flex-col min-h-screen">
    <nav class="sticky top-0 z-50 bg-white/80 backdrop-blur-lg shadow-sm border-b border-slate-200">
      <div class="container mx-auto px-6 py-3 flex justify-between items-center">
        <router-link to="/" class="text-2xl font-bold text-slate-800 tracking-tight">
          Gradly
        </router-link>

        <div v-if="currentUser.isAuthenticated" class="relative w-full max-w-md hidden md:block">
          <i class="fa fa-search absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"></i>
          <input
            v-model="searchQuery"
            @input="handleSearch"
            type="text"
            placeholder="Search for students or bodies..."
            class="w-full pl-12 pr-4 py-2 rounded-full bg-slate-100 border-transparent focus:outline-none focus:ring-2 focus:ring-sky-500 transition-all"
          />
          <div v-if="searchResults.length > 0 || noResults" class="absolute left-0 mt-2 w-full bg-white border border-slate-200 rounded-lg shadow-xl z-50 overflow-hidden">
             <div v-if="noResults" class="p-4 text-slate-500">No results found.</div>
             <a v-for="user in searchResults" :key="user.id" :href="user.url" class="block px-4 py-3 hover:bg-sky-50 transition-colors text-slate-700">
                {{ user.name }}
             </a>
          </div>
        </div>

        <div class="flex items-center space-x-5">
          <template v-if="currentUser.isAuthenticated">
            <router-link to="/dashboard" class="text-slate-600 hover:text-sky-500 font-medium transition-colors">Dashboard</router-link>
            <router-link to="/feed" class="text-slate-600 hover:text-emerald-500 font-medium transition-colors">Feed</router-link>
            <router-link to="/resources" class="text-slate-600 hover:text-sky-500 font-medium transition-colors">Resources</router-link>

            <!-- Profile Dropdown -->
            <div class="relative" ref="dropdownRef">
              <button @click="toggleDropdown" class="w-10 h-10 rounded-full overflow-hidden border-2 border-slate-300 focus:outline-none">
                <img :src="currentUser.profilePic || '/src/assets/default-profile.png'" alt="Profile Picture" class="w-full h-full object-cover">
              </button>

              <div v-show="dropdownOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-200 py-2 z-50">
                <router-link :to="'/profile/' + currentUser.id" class="block px-4 py-2 text-slate-700 hover:bg-slate-100" @click="dropdownOpen = false">View Profile</router-link>
                <router-link to="/messages" class="block px-4 py-2 text-slate-700 hover:bg-slate-100" @click="dropdownOpen = false">See Messages</router-link>
                <a href="#" @click.prevent="logout" class="block px-4 py-2 text-red-600 hover:bg-red-100">Logout</a>
              </div>
            </div>
          </template>
          <template v-else>
             <router-link to="/login" class="text-slate-600 hover:text-sky-500 font-medium transition-colors">Login</router-link>
             <router-link to="/register" class="bg-sky-500 text-white px-4 py-2 rounded-full text-sm font-semibold hover:bg-sky-600 transition-all duration-300">Register</router-link>
          </template>
        </div>
      </div>
    </nav>

    <div class="container mx-auto px-6 mt-6">
       <!-- Flash Messages Placeholder -->
       <div v-for="(msg, index) in messages" :key="index" :class="getFlashClass(msg.category)" class="p-4 mb-4 text-sm rounded-lg flex items-center gap-3">
          <i :class="getFlashIcon(msg.category)"></i>
          <span>{{ msg.text }}</span>
       </div>
    </div>

    <main class="container mx-auto px-6 py-8 flex-grow">
      <div class="content-fade-in">
        <router-view></router-view>
      </div>
    </main>

    <footer class="bg-white border-t border-slate-200 text-center py-6 mt-auto">
        <p class="text-slate-500">&copy; 2025 Gradly Portal · Built for IIM Amritsar</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const dropdownOpen = ref(false)
const dropdownRef = ref(null)

// Mock User Data - In real app, this comes from a store/auth service
const currentUser = reactive({
  isAuthenticated: true, // Set to false to see login/register
  id: 1,
  name: 'Test User',
  user_type: 'student',
  profilePic: null // will use default
})

// Search Logic
const searchQuery = ref('')
const searchResults = ref([])
const noResults = ref(false)
let debounceTimeout = null

const handleSearch = () => {
  clearTimeout(debounceTimeout)
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    noResults.value = false
    return
  }
  debounceTimeout = setTimeout(() => {
    // Mock search results
    if (searchQuery.value.toLowerCase().includes('test')) {
        searchResults.value = [{ id: 1, name: 'Test User', url: '/profile/1' }]
        noResults.value = false
    } else {
        searchResults.value = []
        noResults.value = true
    }
  }, 300)
}

// Dropdown Toggle
const toggleDropdown = () => {
  dropdownOpen.value = !dropdownOpen.value
}

const closeDropdown = (e) => {
    if (dropdownRef.value && !dropdownRef.value.contains(e.target)) {
        dropdownOpen.value = false
    }
}

// Flash Messages Mock
const messages = ref([
    // { category: 'success', text: 'Welcome to Gradly!' }
])

const getFlashClass = (category) => {
    if (category === 'success') return 'bg-green-100 text-green-800 border-l-4 border-green-500'
    if (category === 'danger') return 'bg-red-100 text-red-800 border-l-4 border-red-500'
    if (category === 'info') return 'bg-sky-100 text-sky-800 border-l-4 border-sky-500'
    return 'bg-slate-100 text-slate-800 border-l-4 border-slate-500'
}

const getFlashIcon = (category) => {
    if (category === 'success') return 'fa fa-check-circle'
    if (category === 'danger') return 'fa fa-exclamation-triangle'
    if (category === 'info') return 'fa fa-info-circle'
    return 'fa fa-comment-dots'
}

const logout = () => {
    currentUser.isAuthenticated = false
    router.push('/login')
}

onMounted(() => {
    document.addEventListener('click', closeDropdown)
})

onUnmounted(() => {
    document.removeEventListener('click', closeDropdown)
})
</script>

<style>
/* CSS from base.html */
</style>
