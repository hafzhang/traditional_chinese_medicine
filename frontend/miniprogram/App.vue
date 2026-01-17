<script>
export default {
  onLaunch: function() {
    console.log('App Launch')
  },
  onShow: function() {
    console.log('App Show')
  },
  onHide: function() {
    console.log('App Hide')
  }
}
</script>

<style>
/* 全局样式 */
page {
  background-color: #f8f8f8;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
}

.container {
  padding: 30rpx;
}

/* 体质标签样式 */
.tag {
  display: inline-block;
  padding: 10rpx 20rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
  margin: 0 10rpx 10rpx 0;
}

.tag-primary {
  background-color: #4CAF50;
  color: #fff;
}

.tag-secondary {
  background-color: #FFC107;
  color: #fff;
}

/* 卡片样式 */
.card {
  background-color: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.1);
}

.card-title {
  font-size: 32rpx;
  font-weight: bold;
  margin-bottom: 20rpx;
  color: #333;
}

.card-content {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
}

/* 按钮样式 */
.btn {
  width: 100%;
  height: 88rpx;
  border-radius: 44rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  margin-top: 30rpx;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.btn-outline {
  background-color: transparent;
  border: 2rpx solid #667eea;
  color: #667eea;
}
</style>
