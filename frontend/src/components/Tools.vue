<template>
  <div class="tools mx-10 my-5" position-relative>
    <div class="d-flex align-center justify-end">
      <VBtn v-if="false" class="mr-5" prepend-icon="mdi-cog" @click="onShowConfig()">
        <span>修改配置</span>
      </VBtn>
      <VBtn class="" prepend-icon="mdi-email" @click="onShowHistoryFile()">
        <span>历史文件</span>
        <VBadge
          v-if="cache_files_count > 0"
          class="ml-1 mb-2"
          color="primary"
          floating
          :content="cache_files_count"
        />
      </VBtn>
      <VBtn class="ml-5" prepend-icon="mdi-logout" @click="goToIndex()">
        <span>退出</span>
      </VBtn>
    </div>

    <div v-for="label in labels" :key="label" class="mb-10">
      <div class="mb-4">
        {{ labels_map[label] ?? label }}
      </div>
      <v-row>
        <v-col
          v-for="tool in filterTools(label)"
          :key="tool.uuid"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          xl="2"
        >
          <VCard variant="elevated" elevation="24" hover @click="onShowTool(tool)">
            <div class="d-flex flex-no-wrap align-center">
              <v-hover v-slot="{ isHovering, props }">
                <v-avatar rounded="0" size="80" v-bind="props">
                  <v-img
                    :src="
                      tool.thumbnail
                        ? `https://ai.hezi.com:16520${tool.thumbnail.replace('image', 'thumbnail')}`
                        : defaultImage
                    "
                  >
                    <v-expand-transition v-if="false">
                      <div
                        v-if="isHovering"
                        class="d-flex align-center justify-center"
                        style="height: 100%"
                      >
                        <VBtn
                          color="purple-darken-2"
                          icon="mdi-cloud-download"
                          size="small"
                          v-bind="props"
                          @click.stop="onDownloadTool(tool)"
                        />
                      </div>
                    </v-expand-transition>
                  </v-img>
                </v-avatar>
              </v-hover>

              <div class="tool-info d-flex flex-column">
                <VCardTitle class="tool-info-title">
                  {{ tool.name }}
                </VCardTitle>
                <VCard-subtitle class="tool-info-desc mb-2">
                  {{ tool.desc }}
                </VCard-subtitle>
              </div>
            </div>
          </VCard>
        </v-col>
      </v-row>
    </div>
  </div>

  <v-progress-circular
    v-if="download_process > 0"
    :model-value="download_process"
    :rotate="360"
    :size="100"
    :width="15"
    color="purple"
    class="text-center position-fixed bottom-0 right-0 mr-10 mb-10"
  >
    <template #default> {{ download_process }} % </template>
  </v-progress-circular>

  <VDialog v-model="dialog_selectfile" width="70%" height="70%" persistent>
    <VSheet max-height="10%" class="d-flex justify-space-between align-center" rounded="0">
      <div class="text-h5 text-medium-emphasis ps-4">选择处理文件</div>
      <VBtn icon="mdi-close" variant="text" @click="dialog_selectfile = false" />
    </VSheet>
    <VSheet rounded="0">
      <FileUpload @get-files="onGetFiles" />
    </VSheet>
    <VSheet max-height="10%" class="d-flex justify-center align-center" rounded="0">
      <VBtn
        prepend-icon="$loading"
        color="primary"
        rounded="lg"
        size="large"
        @click="onUploadAndHandle()"
      >
        <template #default> 处理文件 </template>
      </VBtn>
    </VSheet>
  </VDialog>

  <VDialog v-model="dialog_selectdir" width="70%" height="70%" persistent>
    <VCard rounded="lg">
      <VCardTitle class="d-flex justify-space-between align-center">
        <div class="text-h5 text-medium-emphasis ps-2">选择处理文件夹</div>

        <VBtn icon="mdi-close" variant="text" @click="dialog_selectdir = false" />
      </VCardTitle>

      <VDivider class="mb-10" />

      <v-file-input
        v-model="files"
        label="选择文件夹"
        multiple
        show-size
        class="ml-2 mr-4"
        counter
        width="400"
        webkitdirectory
        @change="onFilterSubFiles()"
      >
        <template #selection="{ fileNames }">
          <template v-for="(file, index) in files" :key="file.name">
            <v-chip v-if="index < 1" class="me-2" color="deep-purple-accent-1" size="medium" label>
              {{ fileNames[0] }}
            </v-chip>
            <span v-else-if="index === 1" class="text-overline mx-2">
              +{{ files.length - 1 }} File(s)
            </span>
          </template>
        </template>
      </v-file-input>

      <!-- <VCard-subtitle class="d-flex justify-center">仅处理一级子文件</VCard-subtitle> -->

      <!-- <VList lines="one">
        <VList-subheader v-if="files.length > 0">{{
          files[0].webkitRelativePath.split('/')[0]
        }}</VList-subheader>

        <VListItem v-for="file in files" :key="file.name" :title="file.name">
          <template v-slot:append>
            <VBtn icon @click="onRemoveDir(n)"> <VIcon>mdi-close</VIcon></VBtn>
          </template>
        </VListItem>
      </VList> -->

      <VCardActions class="my-2 d-flex justify-center">
        <VBtn
          prepend-icon="$loading"
          color="primary"
          rounded="lg"
          variant="flat"
          size="x-large"
          elevation="24"
          :loading="loading"
          @click="onHandleAndDownload()"
        >
          <template #default> 处理并下载 </template>
        </VBtn>
      </VCardActions>
    </VCard>
  </VDialog>

  <VDialog v-model="dialog_transfile" width="70%" height="70%" persistent>
    <VCard rounded="lg" position-relative>
      <VCardTitle class="d-flex justify-space-between align-center">
        <div class="text-h5 text-medium-emphasis ps-2">文件处理结果</div>

        <VBtn icon="mdi-close" variant="text" @click="dialog_transfile = false" />
      </VCardTitle>
      <VDivider class="mb-2" />
      <VList v-if="files.length > 0" lines="two" class="mb-12">
        <div class="d-flex justify-space-between ml-4 mr-4">
          <div>被处理文件</div>
          <div>处理结果</div>
        </div>
        <VListItem v-for="(file, index) in files" :key="index" :title="file.name">
          <template #prepend>
            <v-avatar
              :color="
                file.status === 'failure'
                  ? 'error'
                  : file.status === 'pending'
                    ? 'green'
                    : 'primary'
              "
            >
              <VIcon color="white"> mdi-folder </VIcon>
            </v-avatar>
          </template>
          <template #subtitle>
            <VRow>
              <VCol>
                {{
                  file.size / 1024 / 1024 < 1
                    ? Math.ceil(file.size / 1024) + 'KB'
                    : Math.ceil(file.size / 1024 / 1024) + 'MB'
                }}
              </VCol>
              <VCol>
                <div>
                  {{ file.tool_name ? file.tool_name : '执行中...' }}
                </div>
              </VCol>
              <VCol>
                {{
                  file.handle_timestamp
                    ? new Date(file.handle_timestamp).toLocaleString()
                    : '执行中...'
                }}
              </VCol>
            </VRow>
          </template>
          <template #append>
            <VDivider vertical class="ml-6 mr-2" />

            <div class="ml-6">
              <v-tooltip v-if="file.status === 'failure'" :text="file.message" location="top">
                <template #activator="{ props }">
                  <VBtn
                    color="grey-darken-1"
                    prepend-icon="mdi-alert-circle"
                    size="small"
                    v-bind="props"
                  >
                    失败
                  </VBtn>
                </template>
              </v-tooltip>
              <v-tooltip
                v-else
                :text="file.plugin_serve_ip + ':' + file.plugin_serve_port"
                location="right"
              >
                <template #activator="{ props }">
                  <VBtn
                    :loading="file.status === 'success' ? false : true"
                    color="primary"
                    prepend-icon="mdi-cloud-download"
                    size="small"
                    v-bind="props"
                    @click="downloadFile(file)"
                  >
                    下载
                  </VBtn>
                </template>
              </v-tooltip>
            </div>
          </template>
        </VListItem>
      </VList>
      <VSheet v-else class="d-flex align-center justify-center mb-10" height="100%">
        <VEmptyState
          icon="mdi-magnify"
          text="您未处理过任何文件,或处理文件已过期"
          title="暂无任何数据"
          class="text-center"
        />
      </VSheet>

      <VSheet class="position-absolute bottom-0 left-0 right-0">
        <VDivider class="mb-3" />
        <div class="d-flex justify-space-between align-center mx-4 mb-3">
          <div>结果保留24小时后自动清理</div>
          <VBtn
            :loading="loading_download_all"
            color="primary"
            prepend-icon="mdi-arrow-down"
            variant="flat"
            @click="downloadAllFiles()"
          >
            <template #default> 下载该服务全部成功文件 (zip) </template>
          </VBtn>
        </div>
      </VSheet>
    </VCard>
  </VDialog>

  <VDialog v-model="dialog_setting" width="70%" height="70%" persistent>
    <VCard>
      <VCardTitle class="d-flex justify-space-between align-center" prepend-icon="mdi-cog">
        <div class="text-h5 text-medium-emphasis ps-2">
          <VIcon class="pr-3"> mdi-cog </VIcon>服务配置
        </div>
        <VBtn icon="mdi-close" variant="text" @click="onCloseConfig()" />
      </VCardTitle>
      <v-form @submit.prevent="onSaveConfig()">
        <VCard-text>
          <v-row dense>
            <v-col cols="12" sm="6" md="6" lg="6" xl="6">
              <v-text-field
                v-model="new_form_config.ip"
                :rules="[form_config_rules.required, form_config_rules.ip]"
                hint="请输入服务器Ip"
                label="Ip*"
                placeholder="127.0.0.1"
                clearable
                variant="outlined"
              />
            </v-col>

            <v-col ols="12" sm="6" md="6" lg="6" xl="6">
              <v-text-field
                v-model="new_form_config.port"
                hint="请输入服务器端口"
                label="Port*"
                placeholder="80"
                required
                :rules="[form_config_rules.port]"
                clearable
                variant="outlined"
              />
            </v-col>

            <v-col cols="12" md="12" sm="12">
              <v-text-field
                v-model="new_form_config.tokenapi"
                hint="请输入服务器TokenApi"
                label="TokenApi*"
                required
                :rules="[form_config_rules.required]"
                clearable
                variant="outlined"
              />
            </v-col>

            <v-col cols="12" md="12" sm="12">
              <v-text-field
                v-model="new_form_config.tokenenv"
                hint="请输入服务器TokenEnv"
                label="TokenEnv*"
                :rules="[form_config_rules.required]"
                clearable
                variant="outlined"
                :disabled="showTokenEnv()"
              />
            </v-col>
          </v-row>

          <small class="text-caption text-medium-emphasis">*必填选项</small>
          <div>
            <small class="text-caption text-medium-emphasis"
              >修改设置只为临时设置,刷选页面即过期
            </small>
          </div>
        </VCard-text>
      </v-form>
      <VDivider />

      <VCard-actions>
        <v-spacer />
        <VBtn text="不保存" variant="plain" @click="onNoSaveConfig()" />
        <VBtn color="primary" text="保存" variant="tonal" @click="onSaveConfig()" />
      </VCard-actions>
    </VCard>
  </VDialog>

  <VDialog v-model="dialog_json" width="70%" height="70%" persistent>
    <VCard>
      <VCardTitle class="d-flex justify-space-between align-center" prepend-icon="mdi-cog">
        <div class="text-h5 text-medium-emphasis ps-2">
          <VIcon class="pr-3"> mdi-pencil </VIcon>JSON配置编辑
        </div>
        <VBtn icon="mdi-close" variant="text" @click="dialog_json = false" />
      </VCardTitle>
      <JsonEditor />

      <VCardActions class="my-3 d-flex justify-center align-center">
        <VBtn
          color="primary"
          rounded="lg"
          variant="flat"
          size="x-large"
          elevation="24"
          :loading="loading"
          @click="onExecJson()"
        >
          <template #default> 运行 </template>
        </VBtn>
      </VCardActions>
    </VCard>
  </VDialog>

  <VDialog v-model="dialog_execlogs" width="70%" height="70%" persistent>
    <VCard>
      <VCardTitle class="d-flex justify-space-between align-center" prepend-icon="mdi-cog">
        <div class="text-h5 text-medium-emphasis ps-2">
          <VIcon class="pr-3"> mdi-pencil </VIcon>执行日志
        </div>
        <VBtn icon="mdi-close" variant="text" @click="dialog_execlogs = false" />
      </VCardTitle>
      <v-table v-if="execlogs.length > 0">
        <thead>
          <tr>
            <th class="text-left">server</th>
            <th class="text-left">cmd</th>
            <th class="text-left">msg</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in execlogs" :key="index">
            <td>{{ item[0] }}</td>
            <td>{{ item[1] }}</td>
            <td>{{ item[2] }}</td>
          </tr>
        </tbody>
      </v-table>
      <VEmptyState
        v-else
        icon="mdi-magnify"
        text="您未处理过任何数据,或处理数据已过期"
        title="暂无任何数据"
      />
    </VCard>
  </VDialog>
</template>

<script setup>
import { onMounted, provide, ref, watch } from 'vue'
import JSZip from 'jszip'
import { saveAs } from 'file-saver'
import router from '@/router'

import defaultImage from '@/assets/default.png'
import * as apitools from '@/service/modules/tools'
import { localCache } from '@/utils/cache'
import { APP_TOKEN, CACHE_TOOLS_FILES } from '@/utils/constant'
import appSoner from '@/utils/appSonner'
import { pluginRequest } from '@/service'
import { useToolsStore } from '@/stores'
import JsonEditor from '@/components/JsonEditor.vue'
import FileUpload from './FileUpload.vue'

const toolsStore = useToolsStore()
const tools = ref([])
const files = ref([])

const form_config_rules = ref({
  required: (value) => !!value || '必填字段不能为空',
  ip: (value) => {
    const pattern =
      /^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/
    return pattern.test(value) || '不合法的IP地址'
  },
  port: (value) => {
    const pattern = /^([0-9]{1,5})$/
    const isValid = pattern.test(value) && parseInt(value, 10) <= 65525
    return isValid || '不合法的端口号'
  },
})
const json_data = ref({
  hosts: ['192.168.10.121', '192.168.10.122'],
  port: 16776,
  cmds: [
    'echo Hello, World!',
    'ipconfig',
    'reg add "HKCU\\Software\\TestKey1" /v TestValue /t REG_SZ /d "Hello, World!" /f',
    "reg add 'HKLM\\Software\\TestKey1' /v TestValue /t REG_SZ /d 'Hello, World!' /f",
    "powershell -c 'Get-ChildItem'",
    "powershell -c '$PSVersionTable.PSVersion'",
  ],
  timeout: 5,
  logfile: 'cmdexec.log',
  decode: 'gbk',
})
const new_form_config = ref({ ip: '', port: '', tokenapi: '', tokenenv: '' })
const form_config = ref({
  ip: toolsStore.plugin_base_url.split('//')[1].split(':')[0],
  port: toolsStore.plugin_base_url.split('//')[1].split(':')[1],
  tokenapi: toolsStore.ai_token,
  tokenenv: toolsStore.plugin_token,
})
const cur_tool = ref(null)
const labels = ref([''])
const labels_map = {
  other: '其他工具',
  image: '图片处理',
  audio: '音频转换',
  video: '视频转换',
}
const dialog_selectfile = ref(false)
const select_file_type = ref('*')
const select_file_type_map = {
  image: 'image/*',
  audio: 'audio/*',
  video: 'video/*',
}
const loading = ref(false)
const dialog_transfile = ref(false)
const dialog_selectdir = ref(false)
const dialog_setting = ref(false)
const dialog_json = ref(false)
const cache_files_count = ref(0)
const download_process = ref(0)
const execlogs = ref([])
const dialog_execlogs = ref(false)

const loading_download_all = ref(false)

provide('json_data', json_data)
provide('select_file_type', select_file_type)

const getTools = async () => {
  const res = await apitools.apiGetTools()
  if (res.code === 200) {
    tools.value = res.data.filter((tool) => tool.publish === true)
    labels.value = Array.from(
      new Set(tools.value.map((item) => item.label).filter((label) => label !== 'other')),
    )
  } else {
    appSoner.error('获取工具列表失败')
  }
}

const getCacheFiles = () => {
  let cache_files = localCache.getCache(CACHE_TOOLS_FILES) || []
  cache_files = cache_files.filter((file) => {
    return file.handle_timestamp + 24 * 60 * 60 * 1000 >= Date.now()
  })
  cache_files_count.value = cache_files.length
  return cache_files
}

const onShowConfig = () => {
  dialog_setting.value = true
  new_form_config.value = { ...form_config.value }
}

const onCloseConfig = () => {
  if (JSON.stringify(new_form_config.value) !== JSON.stringify(form_config.value)) {
    appSoner.error('服务配置有变更，请确认是否保存')
  } else {
    dialog_setting.value = false
  }
}

const onNoSaveConfig = () => {
  dialog_setting.value = false
}

const onSaveConfig = async () => {
  const rules = form_config_rules.value
  if (
    rules.ip(new_form_config.value.ip) !== true ||
    rules.required(new_form_config.value.ip) !== true
  ) {
    appSoner.error('IP地址格式错误')
    return
  }
  if (
    rules.port(new_form_config.value.port) !== true ||
    rules.required(new_form_config.value.ip) !== true
  ) {
    appSoner.error('端口号格式错误')
    return
  }

  if (
    rules.required(new_form_config.value.tokenapi) !== true ||
    (await apitools.apiValidApiToken(new_form_config.value.tokenapi)).code !== 200
  ) {
    appSoner.error('TokenApi校验失败')
    return
  }

  if (showTokenEnv() !== true && rules.required(new_form_config.value.tokenenv) !== true) {
    appSoner.error('TokenEnv必须填写')
    return
  }
  form_config.value = { ...new_form_config.value }
  appSoner.success('保存成功')
  dialog_setting.value = false
}

const onShowHistoryFile = () => {
  dialog_transfile.value = true
  files.value = getCacheFiles()
}

const onShowTool = (tool) => {
  const Tools = {
    Tool1: '#file',
    Tool2: '#dir',
    Tool3: '#json',
  }
  const desc_part = tool.desc.match(/#[a-zA-Z]+/)?.[0]
  switch (desc_part) {
    case Tools.Tool1:
      files.value = []
      dialog_selectfile.value = true
      select_file_type.value = select_file_type_map[tool.label] || '*'
      cur_tool.value = tool
      break
    case Tools.Tool2:
      files.value = []
      dialog_selectdir.value = true
      cur_tool.value = tool
      break
    case Tools.Tool3:
      dialog_json.value = true
      break
    default:
      appSoner.warning('暂未开放在线处理')
      break
  }
}

const onDownloadTool = async (tool) => {
  const saveFile = (data, filename) => {
    const url = window.URL.createObjectURL(data)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    link.click()
    window.URL.revokeObjectURL(url)
  }

  let isDownloadFailed = false

  const res = await apitools.apiGetDownloadUrl(tool.fileurl || '')
  if (res.code === 200) {
    try {
      const download_res = await apitools.apiDownloadTool(res.data, (percent) => {
        if (!isDownloadFailed) {
          download_process.value = Math.floor((percent * 100) / 100)
        }
      })
      saveFile(download_res, tool.fileurl?.replace(/\\/g, '/')?.split('/')?.pop() || 'unknown')
      appSoner.success('下载成功')
    } catch (e) {
      isDownloadFailed = true
      appSoner.error(`下载失败，请重试${e}`)
    } finally {
      download_process.value = 0
    }
  } else {
    appSoner.error('获取下载地址失败')
  }
}

const onUploadAndHandle = async () => {
  dialog_transfile.value = files.value.length > 0 ? true : false
  dialog_selectfile.value = dialog_transfile.value ? false : dialog_selectfile.value
  loading_download_all.value = true

  if (dialog_transfile.value) {
    for (let i = 0; i < files.value.length; i++) {
      const file = files.value[i]
      const reader = new FileReader()
      reader.onload = async (event) => {
        const base64Content = event.target.result.split(',')[1]
        const res = await apitools.apiUploadBinary(base64Content, file.name)
        if (res.code === 200) {
          file.remote_path = 'cache/file_upload/Sharing_Storage/mobile' + '/' + res.data
          file.status = 'pending'
          await handleFile(file)
        } else {
          file.status = 'failure'
          file.message = res.message || '上传失败'
          files.value = [...files.value]
        }
        const allFilesProcessed = files.value.every((f) => f.status !== 'pending')
        if (allFilesProcessed) {
          loading_download_all.value = false
        }
      }
      reader.readAsDataURL(file)
    }
  } else {
    appSoner.warning('请先选择文件')
  }
}

const onRemoveFile = (file) => {
  const index = files.value.findIndex((item) => item === file)
  files.value.splice(index, 1)
}

const onFilterSubFiles = () => {
  if (files.value.length > 0) {
    files.value = Array.from(files.value).filter((file) => {
      const relativePath = file.webkitRelativePath
      const level = (relativePath.match(/\//g) || []).length
      return level === 1
    })
  }
  return files.value
}

const onHandleAndDownload = async () => {
  const typeMapping = {
    图片: { type: 'image', defaultExt: '.png' },
    音频: { type: 'audio', defaultExt: '.mp3' },
    视频: { type: 'video', defaultExt: '.mp4' },
  }

  const matchedKey = Object.keys(typeMapping).find((key) => cur_tool.value?.name.includes(key))

  const filename = matchedKey ? typeMapping[matchedKey].type : 'default'
  const default_ext = matchedKey ? typeMapping[matchedKey].defaultExt.toLowerCase() : ''

  const zip = new JSZip()
  const sortedFiles = files.value.sort((a, b) => a.lastModified - b.lastModified)
  loading.value = true

  try {
    await Promise.all(
      sortedFiles.map((file, index) => {
        return new Promise((resolve, reject) => {
          const newFileName = `${filename}_${(index + 1).toString().padStart(sortedFiles.length.toString().length, '0')}${default_ext}`

          const fileReader = new FileReader()
          fileReader.onload = (event) => {
            try {
              zip.file(newFileName, event.target.result)
              resolve()
            } catch (error) {
              reject(error)
            }
          }
          fileReader.onerror = () => reject(fileReader.error)
          fileReader.readAsArrayBuffer(file)
        })
      }),
    )
    const content = await zip.generateAsync({ type: 'blob' })
    const link = transBlob2Link(content, 'result.zip')
    link.click()
  } catch (error) {
    appSoner.error(`处理文件失败: ${error}`)
  }
  loading.value = false
}

const onExecJson = async () => {
  const pingServer = async (host, port) => {
    const url = `http://${host}:${port}`
    const timeout = 5000

    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error('无法连接到服务器，超时')), timeout),
    )

    try {
      const res = await Promise.race([fetch(url, { method: 'GET' }), timeoutPromise])
      if (res && res.status === 200) {
        return [true, null]
      } else {
        return [false, '无法连接到服务器']
      }
    } catch (e) {
      if (e instanceof Error) {
        return [false, `无法连接到服务器，错误信息：${e.message}`]
      }
      return [false, '未知错误']
    }
  }

  const execCmd = async (hosts, port, cmds, timeout, decode) => {
    for (const host of hosts) {
      const [f, msg] = await pingServer(host, port)
      if (!f) {
        execlogs.value.push([host.toString() + ':' + port.toString(), 'ping', msg])
        return false
      }

      for (const cmd of cmds) {
        try {
          const params = { cmd: cmd, timeout: timeout, decode: decode }
          const res = await fetch(`http://${host}:${port}/api/exec_cmds`, {
            method: 'POST',
            body: JSON.stringify(params),
            headers: { 'Content-Type': 'application/json' },
          })
          if (res.status === 200) {
            const res_json = await res.json()
            if (res_json.data.error !== '') {
              execlogs.value.push([
                host.toString() + ':' + port.toString(),
                cmd,
                `error: ${res_json.data.error}`,
              ])
              return false
            } else {
              execlogs.value.push([host, cmd, res_json.data.output])
            }
          } else {
            execlogs.value.push([
              host.toString() + ':' + port.toString(),
              cmd,
              `error: ${await res.text()}`,
            ])
            return false
          }
        } catch (e) {
          execlogs.value.push([host.toString() + ':' + port.toString(), cmd, e])
          return false
        }
      }
    }
    return true
  }

  const main = async () => {
    const hosts = json_data.value.hosts
    const cmds = json_data.value.cmds
    const timeout = json_data.value.timeout
    const port = json_data.value.port
    const decode = json_data.value.decode
    loading.value = true
    const flag = await execCmd(hosts, port, cmds, timeout, decode)
    loading.value = false
    if (flag) {
      appSoner.success('执行成功')
    } else {
      appSoner.error('执行失败')
    }
    dialog_execlogs.value = true
  }
  main()
}

const onGetFiles = (value) => {
  files.value = value
}

const showTokenEnv = () => new_form_config.value.ip === '127.0.0.1'

const filterTools = (label) => {
  return tools.value.filter((tool) => tool.label === label)
}

const handleFile = async (file) => {
  const map = {
    image转换: apitools.apiTransi2i,
    image移除图片背景: apitools.apiRemoveBgi,
    image移除图片前景: apitools.apiRemoveFgi,
    video转换: apitools.apiTransv2v,
    audio转换: apitools.apiTransa2a,
  }
  let toolapi = async () => {
    throw new Error('No matching key found in map')
  }
  for (const key in map) {
    if (((cur_tool.value?.label ?? '') + (cur_tool.value?.name ?? '')).includes(key)) {
      toolapi = map[key]
      break
    }
  }

  const res = await toolapi(
    file.remote_path,
    '.' + cur_tool.value?.name.match(/[a-z0-9]+/gi)?.join(''),
  )
  if (res.code === 200) {
    file.status = 'success'
    file.remote_tar_path = res.data
    file.plugin_serve_ip = form_config.value?.ip
    file.plugin_serve_port = form_config.value?.port
    file.handle_timestamp = Date.now()
    file.tool_name = cur_tool.value?.name
    files.value = [...files.value]
    setFile2Cache(file)
  } else {
    file.status = 'failure'
    file.tool_name = cur_tool.value?.name
    file.handle_timestamp = Date.now()
    file.message = res.message || '处理文件失败'
    files.value = [...files.value]
  }
}

const downloadFile = async (file) => {
  const remote_tar_name = file.remote_tar_path?.split(/[/\\]/)?.slice(-2).join('/')
  const extension = file.remote_tar_path?.match(/\.[0-9a-z]+$/i)?.join('')
  if (
    'https://' + file.plugin_serve_ip + ':' + file.plugin_serve_port !==
    toolsStore.plugin_base_url
  ) {
    appSoner.error('不是该服务的文件')
    return
  }
  const res = await apitools.apiDownloadBinary(remote_tar_name || '')
  if (res.code === 200) {
    const bytes_data = transBase642Bytes(res.data)
    const link = transBlob2Link(
      new Blob([bytes_data.buffer]),
      file.name.replace(/\.[^]+$/, extension || 'unknown'),
    )
    link.click()
    appSoner.success('下载成功')
  } else {
    appSoner.error(res.message || '下载失败')
  }
}

const downloadAllFiles = async () => {
  const zip = new JSZip()
  const successfulFiles = files.value
    .filter((file) => file.status === 'success')
    .filter(
      (file) =>
        'https://' + file.plugin_serve_ip + ':' + file.plugin_serve_port ===
        toolsStore.plugin_base_url,
    )
  if (successfulFiles.length === 0) {
    appSoner.info('没有成功处理的文件')
    return
  }
  const fileNameCounts = {}

  const filePromises = successfulFiles.map(async (file) => {
    const remote_tar_name = file.remote_tar_path?.split(/[/\\]/)?.slice(-2).join('/')
    const res = await apitools.apiDownloadBinary(remote_tar_name || '')
    if (res.code === 200) {
      const bytes = transBase642Bytes(res.data)
      const baseName = file.name.replace(/\.[^.]+$/, '')
      const extension = file.remote_tar_path?.match(/\.[0-9a-z]+$/i)?.join('')
      let finalName = baseName
      if (baseName in fileNameCounts) {
        fileNameCounts[baseName]++
        finalName = `${baseName}(${fileNameCounts[baseName]})`
      } else {
        fileNameCounts[baseName] = 0
      }
      finalName += extension
      zip.file(finalName, bytes.buffer)
      appSoner.success('下载成功')
    } else {
      appSoner.error(res.message || '下载失败')
    }
  })

  await Promise.all(filePromises)

  zip.generateAsync({ type: 'blob' }).then(function (content) {
    saveAs(content, 'tools.zip')
  })
}

const setFile2Cache = (file) => {
  const cache_file_value = {
    name: file.name,
    size: file.size,
    remote_tar_path: file.remote_tar_path,
    plugin_serve_ip: form_config.value?.ip,
    plugin_serve_port: form_config.value?.port,
    status: file.status,
    handle_timestamp: Date.now(),
    type: file.type,
    tool_name: file.tool_name,
  }
  const cache_files = getCacheFiles()
  localCache.setCache(CACHE_TOOLS_FILES, [...cache_files, cache_file_value])
}

const transBase642Bytes = (base64String) => {
  const binaryString = window.atob(base64String)
  const len = binaryString.length
  const bytes = new Uint8Array(len)
  for (let i = 0; i < len; i++) {
    bytes[i] = binaryString.charCodeAt(i)
  }
  return bytes
}

const transBlob2Link = (blob, filename) => {
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', filename)
  document.body.appendChild(link)
  return link
}

const goToIndex = () => {
  localStorage.removeItem('app-token')
  router.push({ path: '/' })
}

watch(
  form_config,
  (newConfig, oldConfig) => {
    if (newConfig.ip !== oldConfig.ip || newConfig.port !== oldConfig.port) {
      toolsStore.plugin_base_url = 'https://' + newConfig.ip + ':' + newConfig.port
      pluginRequest.setBaseURL(toolsStore.plugin_base_url)
    }
    if (newConfig.tokenapi !== oldConfig.tokenapi) {
      toolsStore.ai_token = newConfig.tokenapi
    }
    if (newConfig.tokenenv !== oldConfig.tokenenv) {
      toolsStore.plugin_token = newConfig.tokenenv
    }
  },
  { deep: true },
)

onMounted(() => {
  // setToken()
  getTools()
  getCacheFiles()
})
</script>

<style scoped lang="scss">
.tools {
  font-size: 1.25rem;

  .tool-info {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;

    .tool-info-title {
      font-size: 1rem;
    }

    .tool-info-desc {
      font-size: 0.75rem;
    }
  }
}
</style>
