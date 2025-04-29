<template>
    <br>
    <br>
    <br>
    <div id="footer">
        <p>© 2007 - {{ currentYear }} Jiayu Wang. All Rights Reserved.</p>
    </div>
</template>

<script>
    export default {
        name: 'BlogFooter',
        computed: {
            currentYear() {
                return new Date().getFullYear();
            }
        }
    }
</script>

<style scoped>
    #footer {
        position: fixed;
        left: 0;
        bottom: 0;
        height: 50px;
        width: 100%;
        background: whitesmoke;
        text-align: center;
        font-family: 'Lora', serif;
    }
</style>