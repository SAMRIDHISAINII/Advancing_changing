<template>
  <section id="hero">
    <div class="container">
      <div class="row">
        <div class="col-lg-6 pt-5 pt-lg-0 order-2 order-lg-1 d-flex flex-column justify-content-center"
             data-aos="fade-up">
          <div>
            <h1>Landscape change smart tracker</h1>
            <h2>Machine learning-driven service for image comparison</h2>
            <a href="/upload" class="btn-get-started scrollto">Upload your image</a>
          </div>
        </div>
        <div class="col-lg-6 order-1 order-lg-2 hero-img">
          <img :src="this.logo" alt="">
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'home',
  data: function() {
    return {
      logo: require('../assets/hero.png')
    }
  }
}
</script>

<style lang="scss">

</style>
