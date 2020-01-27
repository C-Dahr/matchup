<template>
    <nav class="navbar navbar-expand-sm" id="navbar-main">
        <!-- Brand -->
        <a class="navbar-brand" href="/"></a>

        <!-- Links -->
        <ul class="navbar-nav">
            <li class="nav-item">
            <a class="nav-link" href="/login">Login</a>
            </li>

            <!-- Dropdown -->
            <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbardrop" data-toggle="dropdown">
                Dropdown link
            </a>
            <div class="dropdown-menu">
                <a class="dropdown-item" href="#">Link 1</a>
                <a class="dropdown-item" href="#">Link 2</a>
                <a class="dropdown-item" href="#">Link 3</a>
            </div>
            </li>
        </ul>
    </nav>
</template>

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
