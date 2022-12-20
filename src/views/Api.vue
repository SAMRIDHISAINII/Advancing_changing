<template>
  <section id="upload" class="upload mt-5">
    <div class="about container my-3">
      <div class="row">
        <div class="col-12 text-center">
          <h1 class="mb-3">Upload Images</h1>
        </div>
      </div>
      <div class="row mb-5">
        <div class="col-12 text-center">Changes are detected by using UNET++ neural network. Unchanged regions are marked red.</div>
      </div>
      <div class="row mb-3">
        <div class="col-md-3 offset-md-1">
          <h5>Before</h5>
          <form>
            <div class="form-group">
              <label for="my-file-first">Select Image</label>
              <input type="file" accept="image/*" @change="previewFirstImage" class="form-control-file"
                     id="my-file-first">
              <div class="border p-2 mt-3">
                <p>Preview Here:</p>
                <template v-if="firstPreview">
                  <img :src="firstPreview" class="img-fluid"/>
                  <p class="mb-0">file name: {{ firstImage.name }}</p>
                  <p class="mb-0">size: {{ firstImage.size / 1024 }}KB</p>
                </template>
              </div>
            </div>
          </form>
        </div>
        <div class="col-md-3 offset-md-1">
          <h5>After</h5>
          <form>
            <div class="form-group">
              <label for="my-file-second">Select Image</label>
              <input type="file" accept="image/*" @change="previewSecondImage" class="form-control-file"
                     id="my-file-second">
              <div class="border p-2 mt-3">
                <p>Preview Here:</p>
                <template v-if="secondPreview">
                  <img :src="secondPreview" class="img-fluid"/>
                  <p class="mb-0">file name: {{ secondImage.name }}</p>
                  <p class="mb-0">size: {{ secondImage.size / 1024 }}KB</p>
                </template>
              </div>
            </div>
          </form>
        </div>
        <div class="col-md-3 offset-md-1">
          <h5>Result</h5>
          <form>
            <div class="form-group">
              <label for="my-file-second">Of the detection</label><br>
              <a download="result.png" class="btn btn-primary" :href="'data:image/png;base64,'+this.resultImage">Download</a>
              <div class="border p-2 mt-3">
                <p>Preview Here:</p>
                <template v-if="resultImage">
                  <img width="240" height="240" :src="'data:image/png;base64,'+this.resultImage"/>
                </template>
              </div>
            </div>
          </form>
        </div>
        <div class="w-100"></div>
        <div class="col-12 mt-3 text-center">
          <button class="btn btn-primary mr-3" @click="uploadImages">Upload</button>
          <button class="btn btn-primary" @click="reset">Clear All</button>
        </div>
      </div>
    </div>
  </section>
</template>
<script>

import axios from 'axios'
import 'core-js/es6'

export default {
  name: 'about',
  data() {
    return {
      firstImage: null,
      firstPreview: null,
      resultImage: null,
      secondImage: null,
      secondPreview: null,
      progressInfos: []
    }
  },
  methods: {
    previewFirstImage: function (event) {
      let input = event.target
      if (input.files) {
        let reader = new FileReader()
        reader.onload = (e) => {
          this.firstPreview = e.target.result
        }
        this.firstImage = input.files[0]
        reader.readAsDataURL(input.files[0])
      }
    },
    previewSecondImage: function (event) {
      let input = event.target
      if (input.files) {
        let reader = new FileReader()
        reader.onload = (e) => {
          this.secondPreview = e.target.result
        }
        this.secondImage = input.files[0]
        reader.readAsDataURL(input.files[0])
      }
    },
    async uploadImages() {
      const json = JSON.stringify({before: this.firstPreview, after: this.secondPreview})
      console.log('sending images to flask: ' + json)
      await axios.post('http://localhost:5000/predict', json, {
        headers: {'Content-Type': 'application/json'}
      }).then((response) => {
        this.resultImage = response.data.image.substring(1).replace(/'/g, '')
      })
    },
    reset: function () {
      this.firstImage = null
      this.firstPreview = null
      this.secondImage = null
      this.resultImage = null
      this.secondPreview = null
    }
  }
}

</script>

<style lang="scss">
</style>
