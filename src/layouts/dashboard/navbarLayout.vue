<template>
    <v-app-bar title="Log Analyzer" color="primary">
        <!-- <v-img
            class="mx-2"
            max-height="40"
            src="../../../public/logo-log-analyzer.png">
        </v-img> -->
        <div class="date-now">
            <h2 id="date"></h2>
        </div>
        <div>
            <v-btn prepend-icon="mdi-logout">
                Logout
            </v-btn>
        </div>
        
    </v-app-bar>
</template>

<script>
function updateTime() {
   let currentTime = new Date();
   let m = currentTime.getMonth();
   let d = currentTime.getDay()
   let s = currentTime.getSeconds();
   let y = currentTime.getFullYear();
   let h = currentTime.getHours();
   let mm = currentTime.getMinutes();
   let n = currentTime.toLocaleDateString()
   let fullTime = `${y}/${m}/${d} ${h}:${mm}:${s}`
   document.getElementById("date").innerHTML = fullTime
}

setInterval(updateTime, 1000); // Run updateTime() every second
</script>

<style>
.date-now {
    padding-right: 1rem;
}
</style>