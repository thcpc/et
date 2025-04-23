import FingerprintJS2 from 'fingerprintjs2'

export function dateFormat(dt) {
  return new Intl.DateTimeFormat(navigator.language, {
    timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).format(new Date(dt))
}

function getFingerprint() {
  return new Promise((resolve) => {
    const options = {
      excludes: {
        userAgent: true, // 排除用户代理
        language: true, // 排除语言设置
        localStorage: true, // 排除
      },
      preprocessor: (key, value) => {
        // 对特定组件进行预处理
        if (key === 'canvas') {
          return value.substring(0, 100) // 只取前100字符
        }
        return value
      },
    }
    FingerprintJS2.get(options, (components) => {
      const values = components.map((c) => c.value)
      const fingerprint = FingerprintJS2.x64hash128(values.join(''), 31)
      resolve(fingerprint)
    })
  })
}

export async function fingerPrint() {
  return await getFingerprint()
}
