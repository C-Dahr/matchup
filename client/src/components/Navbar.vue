<template>
    <nav class="navbar navbar-expand-sm" id="navbar-main">
        <!-- Brand -->
        <a class="navbar-brand" href="/"></a>

        <!-- Links -->
        <ul class="navbar-nav">
            <li class="nav-item">
            <a class="nav-link" href="/">Login</a>
            </li>

        </ul>
    </nav>
</template>

<script>

export default {
  name: 'Navbar',
};

</script>

<style>

.navbar-brand {
    position: relative;
    background: url(../assets/matchuplogo_outline.png);
    width: 170px;
    left: 15px;
    background-size: contain;
}

#navbar-main {
    background-color: #0066FF;
}

.nav-link {
    color: white;
}
</style>
