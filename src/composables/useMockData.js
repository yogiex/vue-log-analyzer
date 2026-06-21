import { faker } from '@faker-js/faker'
import { shallowRef } from 'vue'
import { COLORS } from '@/theme/colors'

faker.seed(123)

const STATUSES = ['aman', 'terindikasi']
const SESSIONS = ['listening', 'grammar', 'reading']

function randomDate(start, end) {
  return faker.date.between({ from: start, to: end })
}

function randomStatus() {
  return faker.helpers.arrayElement(STATUSES)
}

const usersCache = shallowRef([])
const logsCache = shallowRef([])

function generateUsers(count = 50) {
  const users = []
  for (let i = 0; i < count; i++) {
    const timestart = randomDate(new Date('2025-01-01'), new Date('2026-06-21'))
    const timefinish = new Date(timestart.getTime() + faker.number.int({ min: 900, max: 7200 }) * 1000)
    users.push({
      id: i + 1,
      attempt_id: faker.number.int({ min: 1000, max: 9999 }),
      firstname: faker.person.firstName(),
      lastname: faker.person.lastName(),
      email: faker.internet.email(),
      quiz_name: faker.helpers.arrayElement(['EPrT Listening', 'EPrT Grammar', 'EPrT Reading']),
      timestart: timestart.toLocaleString('id-ID'),
      timefinish: timefinish.toLocaleString('id-ID'),
      diff_time_minute: Math.round((timefinish - timestart) / 60000),
      session: faker.helpers.arrayElement(SESSIONS),
      score: faker.number.int({ min: 200, max: 500 }),
      status: randomStatus(),
      track_progress: faker.helpers.arrayElement(['open', 'closed', 'on_progress']),
      userid: faker.number.int({ min: 10000, max: 99999 }),
    })
  }
  return users
}

function generateLogs(count = 100) {
  const logs = []
  for (let i = 0; i < count; i++) {
    logs.push({
      log_id: faker.string.alphanumeric(8).toUpperCase(),
      user_id: faker.number.int({ min: 1000, max: 9999 }),
      action: faker.helpers.arrayElement(['viewed', 'updated', 'created', 'deleted', 'submitted']),
      component: faker.helpers.arrayElement(['quiz', 'course', 'user', 'grade', 'log']),
      course_name: faker.helpers.arrayElement(['EPrT', 'Academic Writing', 'TOEFL Prep', 'Grammar Mastery']),
      ip: faker.internet.ip(),
      quiz_id: faker.number.int({ min: 1, max: 50 }),
      quiz_name: faker.helpers.arrayElement(['EPrT Listening', 'EPrT Grammar', 'EPrT Reading']),
      target: faker.number.int({ min: 100, max: 999 }),
      timecreated: randomDate(new Date('2026-01-01'), new Date('2026-06-21')).toLocaleString('id-ID'),
      user_firstname: faker.person.firstName(),
    })
  }
  return logs
}

export function useMockSummary() {
  const users = generateUsers()
  const logs = generateLogs()

  return {
    count_total_steps: faker.number.int({ min: 5000, max: 50000 }),
    count_directory: logs.length,
    count_users: users.length,
    count_mdl_standard_logs: faker.number.int({ min: 10000, max: 200000 }),
  }
}

export function useMockUsers(count = 50) {
  if (usersCache.value.length === 0) {
    usersCache.value = generateUsers(count)
  }
  return usersCache
}

export function useMockLogs(count = 100) {
  if (logsCache.value.length === 0) {
    logsCache.value = generateLogs(count)
  }
  return logsCache
}

export function useMockAlerts(count = 20) {
  return generateUsers(count).map(u => ({
    ...u,
    timedate: u.timestart,
    time_taken: u.diff_time_minute,
  }))
}

export function useMockFindings(count = 15) {
  return generateUsers(count).map((u, i) => ({
    ...u,
    timedate: u.timestart,
    time_taken: u.diff_time_minute,
    status: i % 3 === 0 ? -1 : 1,
  }))
}

export function useMockMonitoringUsers(count = 20) {
  const badReasons = [
    'Multiple failed login attempts detected',
    'Access from unusual geographic location',
    'Suspicious rapid-fire request pattern',
    'Multiple concurrent sessions detected',
    'Unusual activity outside normal hours',
    'Known malicious IP address range',
    'Abnormal navigation pattern detected',
  ]
  const goodReasons = [
    'Normal activity pattern within session',
    'Consistent access from registered IP',
    'Regular engagement with course materials',
    'No anomalous behavior detected',
    'Standard access pattern within limits',
    'Verified user session with stable connection',
  ]
  return Array.from({ length: count }, () => {
    const session = faker.helpers.arrayElement(SESSIONS)
    const isBad = faker.helpers.arrayElement([true, false])
    return {
      nama: faker.person.firstName(),
      ip_address: faker.internet.ip(),
      img: '/user_456141.png',
      status: isBad ? 'bad' : 'good',
      reason: isBad
        ? faker.helpers.arrayElement(badReasons)
        : faker.helpers.arrayElement(goodReasons),
      session,
    }
  })
}

export function useMockThresholds() {
  return [
    { title: 'Listening Threshold', key: 'listening', value: '', min: 0, max: 100 },
    { title: 'Grammar Threshold', key: 'grammar', value: '', min: 0, max: 100 },
    { title: 'Reading Threshold', key: 'reading', value: '', min: 0, max: 100 },
    { title: 'Writing Threshold', key: 'writing', value: '', min: 0, max: 100 },
    { title: 'Speaking Threshold', key: 'speaking', value: '', min: 0, max: 100 },
    { title: 'Overall Threshold', key: 'overall', value: '', min: 0, max: 100 },
  ]
}

export function useMockChartData() {
  const aman = faker.number.int({ min: 60, max: 85 })
  const terindikasi = 100 - aman

  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  const lineData = months.map(() => faker.number.int({ min: 5, max: 30 }))

  return {
    donutLabels: ['Aman', 'Terindikasi'],
    donutData: [aman, terindikasi],
    donutColors: [COLORS.chart.positive, COLORS.chart.negative],
    lineLabels: months,
    lineData: lineData,
    lineLabel: 'Kasus per Bulan',
  }
}

export function useMockCalendarEvents(count = 10) {
  const events = []
  const names = ['EPrT Schedule', 'Maintenance', 'Report Due', 'Sync Backup', 'System Check']
  const colors = ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey-darken-1']
  for (let i = 0; i < count; i++) {
    const start = randomDate(new Date('2026-06-01'), new Date('2026-07-31'))
    const end = new Date(start.getTime() + faker.number.int({ min: 1, max: 3 }) * 86400000)
    events.push({
      name: faker.helpers.arrayElement(names),
      start: start.toISOString().split('T')[0],
      end: end.toISOString().split('T')[0],
      color: faker.helpers.arrayElement(colors),
    })
  }
  return events
}

export function useMockBackupFiles(count = 8) {
  return Array.from({ length: count }, () => ({
    title: `backup-${faker.date.recent({ days: 30 }).toISOString().split('T')[0]}.sql`,
    url: '#',
    date: faker.date.recent({ days: 30 }).toISOString(),
    size: faker.number.int({ min: 10, max: 500 }) + 'MB',
  }))
}
