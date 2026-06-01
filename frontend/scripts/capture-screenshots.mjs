import { chromium } from "playwright"
import { mkdir } from "fs/promises"
import path from "path"

const base = process.env.BASE_URL ?? "http://localhost:8080"
const outDir = path.resolve("screenshots")

const routes = [
  { name: "landing", path: "/", auth: false },
  { name: "dashboard", path: "/dashboard" },
  { name: "analytics", path: "/analytics" },
  { name: "portfolio", path: "/portfolio" },
  { name: "risk", path: "/risk" },
  { name: "training", path: "/training" },
  { name: "telemetry", path: "/telemetry" },
  { name: "observability", path: "/observability" },
  { name: "experiments", path: "/experiments" },
  { name: "strategies", path: "/strategies" },
  { name: "research", path: "/research" },
  { name: "benchmarks", path: "/benchmarks" },
  { name: "infra", path: "/infra" },
  { name: "health", path: "/health" }
]

async function login(page) {
  await page.goto(`${base}/`, { waitUntil: "networkidle", timeout: 60000 })
  await page.fill('input[name="email"]', "admin@rl-hedging.local")
  await page.fill('input[name="password"]', "admin12345")
  await page.click('button[type="submit"]')
  await page.waitForTimeout(2000)
}

async function main() {
  await mkdir(outDir, { recursive: true })
  const browser = await chromium.launch()
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } })
  await login(page)

  for (const route of routes) {
    await page.goto(`${base}${route.path}`, { waitUntil: "networkidle", timeout: 60000 })
    await page.waitForTimeout(1500)
    const file = path.join(outDir, `${route.name}.png`)
    await page.screenshot({ path: file, fullPage: true })
    console.log("saved", file)
  }

  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 } })
  await mobile.goto(`${base}/dashboard`, { waitUntil: "networkidle", timeout: 60000 })
  await mobile.waitForTimeout(1000)
  await mobile.screenshot({ path: path.join(outDir, "dashboard-mobile.png"), fullPage: true })
  console.log("saved", path.join(outDir, "dashboard-mobile.png"))

  await browser.close()
}

main().catch(err => {
  console.error(err)
  process.exit(1)
})
