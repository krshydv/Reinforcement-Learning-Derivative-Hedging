import { render, screen } from "@testing-library/react"
import Page from "../app/page"

Object.defineProperty(globalThis, "fetch", {
  value: vi.fn(() => Promise.resolve({ ok: true, json: () => Promise.resolve({ access_token: "test" }) }))
})

test("renders landing", () => {
  render(<Page />)
  expect(screen.getByText(/Reinforcement Learning Derivative Hedging/i)).toBeInTheDocument()
})
