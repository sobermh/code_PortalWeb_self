<script setup>
import { ref, onMounted } from 'vue'
import Cookies from 'js-cookie'
import router from '@/router'
import { aiRequest } from '@/service'
import appSonner from '@/utils/appSonner'

const m_agree = ref(true)
const m_secret = ref(false)
const m_loading = ref(false)

const m_name = ref(localStorage.getItem('app-name') || '')
const m_pwd = ref(localStorage.getItem('app-pwd') || '')

const on_login = async () => {
  try {
    m_loading.value = true
    if (!m_agree.value) {
      throw new Error('同意条款协议即可登录')
    }
    if (m_name.value.length < 1) {
      throw new Error('账号不能为空')
    }
    if (m_pwd.value.length < 1) {
      throw new Error('密码不能为空')
    }
    const param = {
      pid: 'd47c1348-3087-4867-b034-842e4a928cbe',
      name: m_name.value,
      pwd: m_pwd.value,
      address: '127.0.0.1',
      device: navigator.userAgent,
    }
    const rdata = await aiRequest.post({
      url: '/login',
      data: {
        args: param,
        func: 'post_kmoke_login',
      },
    })
    if (rdata.message == 'role vaild error') {
      appSonner.error('缺少访问权限')
      return
    }
    if (rdata.code != 200) {
      appSonner.error('登录验证失败')
      return
    }
    localStorage.setItem('app-name', m_name.value)
    localStorage.setItem('app-token', rdata.data.token)
    router.push('/app')
  } catch (error) {
    appSonner.error('登录失败,' + error.message)
  } finally {
    m_loading.value = false
  }
}

onMounted(async () => {
  const token = Cookies.get('app-token')
  if (token) {
    console.log('来自三方授权登录')
    const param = {
      pid: 'd47c1348-3087-4867-b034-842e4a928cbe',
      token: token,
      address: '127.0.0.1',
      device: navigator.userAgent,
    }
    const rdata = await aiRequest.post({
      url: '/login',
      data: {
        args: param,
        func: 'post_cookie_login',
      },
    })
    if (rdata.message == 'role vaild error') {
      appSonner.error('缺少访问权限')
      return
    }
    if (rdata.code != 200) {
      appSonner.error('登录验证失败')
      return
    }
    router.push('/app')
    Cookies.remove('app-token')
  }
})
</script>

<template>
  <div class="d-flex align-center justify-center bg-main">
    <VCard
      class="d-flex w-75 rounded-lg"
      color="#222"
      height="60%"
      max-width="1400"
      min-width="860"
    >
      <VImg class="w-50" src="@/assets/bgimg.png" cover />
      <VSheet class="w-50 text-center" color="transparent">
        <VContainer>
          <VRow>
            <VCol cols="12">
              <VImg class="mx-auto mt-2" src="@/assets/logo2.png" width="140" />
            </VCol>

            <VCol cols="12">
              <VCardTitle class="text-h4 font-weight-bold"> AIGC · 工具箱 </VCardTitle>
            </VCol>

            <VCol cols="12">
              <VTextField
                v-model="m_name"
                placeholder="请输入账号"
                type="email"
                persistent-placeholder
                variant="outlined"
              />
            </VCol>

            <VCol cols="12">
              <VTextField
                v-model="m_pwd"
                placeholder="请输入密码"
                :type="m_secret ? 'text' : 'password'"
                :append-inner-icon="m_secret ? 'mdi-show' : 'mdi-hide'"
                persistent-placeholder
                variant="outlined"
                @click:append-inner="m_secret = !m_secret"
                @keyup.enter="on_login"
              />
            </VCol>

            <VCol cols="12">
              <VCheckbox v-model="m_agree" class="text-body-2" hide-details>
                <template #label>
                  <div class="text-body-2">阅读并接受 《服务条款》和 《隐私政策》</div>
                </template>
              </VCheckbox>
            </VCol>

            <VCol cols="12">
              <VBtn :loading="m_loading" block size="x-large" color="primary" @click="on_login">
                登录
              </VBtn>
            </VCol>
          </VRow>
        </VContainer>
      </VSheet>
    </VCard>
  </div>
</template>

<style scoped>
.bg-main {
  height: 100vh;
  background: linear-gradient(to top right, rgba(172, 157, 21, 0.945), rgba(241, 196, 70, 0.8));
}
</style>
