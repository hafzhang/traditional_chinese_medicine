<script setup>
import { onLaunch, onShow, onHide } from '@dcloudio/uni-app'
import { ref, onMounted, onUnmounted } from 'vue'

const debugInfo = ref('')

onLaunch(() => {
  console.log('App Launch')
})

onShow(() => {
  console.log('App Show')
  // 启动调试信息轮询
  if (import.meta.env.DEV) {
    startDebugTimer()
  }
})

onHide(() => {
  console.log('App Hide')
  stopDebugTimer()
})

// 调试工具逻辑
let timer = null
function startDebugTimer() {
  if (timer) return
  timer = setInterval(() => {
    if (typeof window !== 'undefined') {
      const lastReq = window.__LAST_REQUEST__
      const lastErr = window.__LAST_ERROR__
      
      let info = '调试模式 (H5 Dev)\n'
      if (lastReq) {
        info += `Last Req: ${lastReq.method} ${lastReq.url}\n`
      }
      if (lastErr) {
        info += `Last Err: ${lastErr.msg}\nTime: ${lastErr.time}\n`
      }
      debugInfo.value = info
    }
  }, 1000)
}

function stopDebugTimer() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
}
</script>

<style lang="scss">
@import '@/styles/global.scss';

page {
  background-color: #f5f5f5;
  font-size: 16px;
  line-height: 1.6;
}

.debug-overlay {
  position: fixed;
  bottom: 120rpx;
  right: 20rpx;
  background: rgba(0, 0, 0, 0.7);
  color: #0f0;
  padding: 10rpx;
  border-radius: 8rpx;
  font-size: 20rpx;
  z-index: 9999;
  pointer-events: none;
  max-width: 80%;
  word-break: break-all;
}
</style>
